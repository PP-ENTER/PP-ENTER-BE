from django.contrib.auth.views import (
    LoginView,
)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = (
        True  # 이미 인증된 사용자는 success_url로 리디렉션합니다.
    )

    def get_success_url(self):
        # return reverse_lazy('post_list')  # 'user_profile'은 로그인 성공 후 리디렉션할 URL 이름입니다.
        pass


user_login = UserLoginView.as_view()
