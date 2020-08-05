from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "abc@defgh.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # forms.py에서 데이터를 clean 후
            # clean된 data를 돌려줌
            # form.cleaned_data
            print(form.cleaned_data)

        return render(request, "users/login.html", {"form": form})
