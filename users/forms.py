from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):
    # Django를 통해서, HTML을 추가해주는 방법 atrrs (Attribute 추가 방식)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

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


class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        # USerCreation Form을 사용했을때, 각 필드에 대한 placeholder 지정 및
        # Form 입력방식 설정
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password1

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        user.username = email
        user.set_password(password)
        user.save()
