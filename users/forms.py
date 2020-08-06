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


class SignUpForm(forms.ModelForm):
    # 기존 Model과여 연결성을 위해서
    # ModelForm을 사용

    class Meta:
        # 어떤 model을 연결시킬 건지 지정
        model = models.User
        # 어떤 항목들을 Form에 사용할건지 지정
        fields = ("first_name", "last_name", "email")

    # 새로만들 내역이기 때문에 별도로 지정해줘야함
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # clean_passwod1은 우리가 직접확인해야해서 유지
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # 기본설정된 save를 override
    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # commit=False는 Database에 저장하지 말라는 뜻
        user = super().save(commit=False)
        user.username = email
        user.set_password(password)
        user.save()

