from django.urls import path
from .views import (ListPostView)

urlpatterns = [
    path('', ListPostView.as_view()),
    # path('create', createPostView.as_view())
]
