import os
import requests
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    # config.urls.py가 불려오기 전에 불려오는 것을 방지하기위해서
    # reverse_lazy를 사용함
    success_url = reverse_lazy("core:home")
    initial = {"email": "jaeech@naver.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
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
        password = form.cleaned_data.get("password")
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
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
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
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&code={code}&client_secret={client_secret}",
                headers={"Accept": "application/json"},
            )
            # JSON으로 변환
            token_json = result.json()
            print(result_json)
            # ACCESS TOKE 수령 ERROR 발생시, Login으로 되돌리기
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException()
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
                print(profile_json)
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        # 사용할 수 없는 user 비밀번호를 생성함
                        user.set_unusable_password()
                        # 위에 method가 저장을 지원하지 않아서 추가로 저장 필요
                        user.save()
                        login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()

    except GithubException:
        return redirect(reverse("user:login"))
