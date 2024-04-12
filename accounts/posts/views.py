from django.views.generic import (
    ListView,
)
# from .models import Post

class PostListView(ListView):
    # model = Post
    template_name = "posts/post_list.html"

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        pass

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_query = self.request.GET.get("q", "")
    #     if search_query:
    #         queryset = queryset.filter(
    #             Q(title__icontains=search_query)
    #             | Q(contents__icontains=search_query)
    #             | Q(category__icontains=search_query)
    #             | Q(tags__name__icontains=search_query)
    #         ).distinct().order_by("-createDate")
    #     else:
    #         queryset = Post.objects.all().order_by("-createDate")
    #     return queryset

    # # context의 값을 지정하기 위한 오버라이딩
    # def get_context_data(self, **kwargs):
    #     # 기존 컨텍스트 데이터를 가져오기
    #     context = super().get_context_data(**kwargs)
    #     # 10번 반복을 위한 범위 추가
    #     context["repeat_times"] = range(10)

    #     search_query = self.request.GET.get("q", "")
    #     context["search_query"] = search_query  # 검색어를 저장합니다.
    #     # context['object_list']는 get_queryset 메서드에 의해 이미 설정되었습니다.

    #     if self.request.user.is_authenticated:
    #         # 현재 사용자의 포스트만 필터링
    #         user_posts = self.get_queryset().filter(author=self.request.user)
    #         context["user_posts"] = user_posts

    #         # 현재 사용자의 즐겨찾기 목록을 가져옵니다.
    #         favorites = Favorite.objects.filter(user=self.request.user).values_list('post_id', flat=True)
    #         context['favorites'] = favorites

    #     return context


post_list = PostListView.as_view()