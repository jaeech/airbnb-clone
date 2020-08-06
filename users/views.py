from django.views import View
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

