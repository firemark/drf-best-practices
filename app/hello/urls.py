from rest_framework.routers import SimpleRouter, Route

from hello import views


class DummyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'retrieve', 'put': 'update'},
            name='{basename}',
            detail=False,
            initkwargs={'suffix': 'Detail'}
        ),
    ]


router = SimpleRouter(trailing_slash=False)
dummy_router = DummyRouter()
router.register(r'pages', views.PagesViewSet)
router.register(r'my-pages', views.MyPagesViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'user-report', views.UserReportViewSet)
router.register(r'real-pages', views.RealPagesViewSet)
dummy_router.register(r'my-user', views.MyUserViewSet)
urlpatterns = router.urls + dummy_router.urls
