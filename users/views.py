import os
import requests
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# 가공되지 않은 Byte로 이루어진 정보를 파일로 만들 수 있음
from django.core.files.base import ContentFile
from . import forms, models


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    # config.urls.py가 불려오기 전에 불려오는 것을 방지하기위해서
    # reverse_lazy를 사용함
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            messages.success(self.request, f"Welcom back {user.first_name}")
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    messages.info(request, f"See you again {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    # config.urls.py가 불려오기 전에 불려오는 것을 방지하기위해서
    # reverse_lazy를 사용함
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        # form 이 유효하면 form을 저장할것
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        # Models.py에 만든 veryfy_email method를 사용
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: Have to put an error message
        pass

    return redirect(reverse("core:home"))


def github_login(request):
    # 사용자르 Github로 redirect 시켜서 로그인하게 만드는 것
    # enironnment에 저장된 나의 Github ID를 가져옴
    client_id = os.environ.get("GH_ID")
    # 사용자가 Github에 로그인하고 돌아올 URL을 지정해줘야함(Setting을 미리 해놔야함)
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    # Scope / allow_signup 등등 필요한 내역을 redirect에 포함 해놓아야함
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user&scope=user:email"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            # 위에서 받아온 Github Code로 Access toke을 받아와야함
            # 보기 편하게 JSON 형식으로 요청
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            # JSON으로 변환
            token_json = token_request.json()
            # ACCESS TOKE 수령 ERROR 발생시, Login으로 되돌리기
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get the access token.")
            else:
                # result_json에 확인가능한 access_token 읽어서
                access_token = token_json.get("access_token")
                # access_toke으로 API request를 보내서, 사용자 data 가져오기
                # Authorization을 access_token으로 하고
                # JSON으로 데이터 받아오기
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    if name is None:
                        name = profile_json.get("login")

                    email = profile_json.get("email")
                    if email is None:
                        email_request = requests.get(
                            "https://api.github.com/user/emails",
                            headers={
                                "Authorization": f"token {access_token}",
                                "Accept": "application/vnd.github.v3+json",
                            },
                        )
                        email_json = email_request.json()
                        email = email_json[0].get("email")
                    bio = profile_json.get("bio")
                    if bio is None:
                        bio = ""

                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        # 사용할 수 없는 user 비밀번호를 생성함
                        user.set_unusable_password()
                        # 위에 method가 저장을 지원하지 않아서 추가로 저장 필요
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile from Github.")
        else:
            raise GithubException("Can't get your profile")

    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoExepction(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoExepction("Can't get the authorization code.")
        else:
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email", None)
            if email is None:
                raise KakaoExepction("Please provide us your email.")
            properties = profile_json.get("properties")
            nickname = properties.get("nickname")
            profile_image = properties.get("profile_image")
            try:
                user = models.User.objects.get(email=email)
                if user.login_method != models.User.LOGIN_KAKAO:
                    raise KakaoExepction(f"Please log in with: {user.login_method}")
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    email=email,
                    first_name=nickname,
                    username=email,
                    login_method=models.User.LOGIN_KAKAO,
                    email_verified=True,
                )
                user.set_unusable_password()
                user.save()
                if profile_image is not None:
                    photo_reqeust = requests.get(profile_image)
                    # 사진URL을 파일로 가져옴
                    # ContentFile 로 변환을 해줘야함
                    # 가공되지 않은 Byte로 이루어진 정보를 파일로 만들 수 있음
                    user.avatar.save(
                        f"{nickname}-avatar", ContentFile(photo_reqeust.content)
                    )
            messages.success(request, f"Welcome back {user.first_name}")
            login(request, user)
            return redirect(reverse("core:home"))
    except KakaoExepction as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"

    # 추가로 context가 필요할 때
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["hello"] = "Hello!"
    #     return context


class UpdateProfileView(UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = {
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    }

    def get_object(self, querySet=None):
        return self.request.user
