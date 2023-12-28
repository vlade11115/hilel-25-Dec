from django.urls import path
from rest_framework import routers
import rest_framework.authtoken.views
from . import views

router = routers.DefaultRouter()
router.register("book-types", views.BookTypeViewSet)
router.register("books", views.BookViewSet)
router.register("authors", views.AuthorsList)
router.register("authors", views.AuthorsDetail)
router.register("orders", views.OrderViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("api-token-auth/", rest_framework.authtoken.views.obtain_auth_token),
    path("webhook-mono/", views.MonoAcquiringWebhookReceiver.as_view(), name="webhook-mono"),
]
