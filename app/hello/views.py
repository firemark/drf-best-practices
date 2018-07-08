from rest_framework.viewsets import (
    ReadOnlyModelViewSet, ModelViewSet, GenericViewSet,
)
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from django.db.models.aggregates import Count

from hello.models import Page, Notification, User, Category
from hello.permissions import PagePermission
from hello.serializers import (
    PageSerializer,
    MyUserSerializer,
    NotificationSerializer,
    UserReportSerializer,
    SimpleCategorySerializer,
    CategorySerializer,
)


class PagesViewSet(ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class MyPagesViewSet(ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_admin:
            return queryset
        return queryset.filter(user=self.request.user)


class MyUserViewSet(
        UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = MyUserSerializer

    def get_object(self, queryset=None):
        return self.request.user


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_emails(instance, on='create')

    def perform_update(self, serializer):
        instance = serializer.save()
        self.send_emails(instance, on='update')

    def send_emails(self, instance, on):
        print(f'HI {instance}!, on={on}')


class PagesSpecialViewSet(ReadOnlyModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_param.get('title', '').strip()
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleCategorySerializer
        return CategorySerializer


class UserReportViewSet(ReadOnlyModelViewSet):
    queryset = (
        User.objects
        .annotate(count_pages=Count('pages'))
        .all()
    )
    serializer_class = UserReportSerializer


class RealPagesViewSet(ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    permission_classes = [IsAuthenticated, PagePermission]
