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
            self.add_eorr("email", forms.ValidationError("User does not exist"))
