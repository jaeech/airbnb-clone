from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


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

    #### function based view ####
    # def get(self, request):
    #     form = forms.LoginForm(initial={"email": "jaeech@naver.com"})
    #     return render(request, "users/login.html", {"form": form})

    # def post(self, request):
    #     form = forms.LoginForm(request.POST)
    #     if form.is_valid():
    #         # forms.py에서 데이터를 clean 후
    #         # clean된 data를 돌려줌
    #         # form.cleaned_data
    #         email = form.cleaned_data.get("email")
    #         password = form.cleaned_data.get("password")
    #         user = authenticate(request, username=email, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect(reverse("core:home"))

    #     return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
