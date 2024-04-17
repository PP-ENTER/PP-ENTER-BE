from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 수정 및 삭제 권한은 게시글의 작성자에게만 허용
        return obj.user == request.user
