from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # validate를 항목할 앞에 clean_을 꼭 붙여야함!
    # clean만 있는 method의 경우에는,
    # Error가 광범위하게 나오기 때문에 별도로 Error위치를 지정해줘야함
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                # clean을 사용해서 data를 validate했다면
                # cleaned_data로 return해야함
                return self.cleaned_data
            else:
                # Error 위치 지정하기 위해서
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            # Error 위치 지정하기 위해서
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=83)
    last_name = forms.CharField(max_length=83)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User already exists")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
