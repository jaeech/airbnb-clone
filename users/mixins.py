from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# 각각의 Mixin을 불러와서 테스트를 거치는 것


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Access denied")
        return redirect(reverse("core:home"))


# User가 Logout 된 상황인치 확인 후, Logout 된 상황이 아니면
# Access denied를 표시해줌
class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Access denied")
        return redirect(reverse("core:home"))


# User가 Login 된 상황인치 확인 후, Login 된 상황이 아니면
# Access denied를 표시해줌
class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
