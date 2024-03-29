"""survey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from survey.polls.views import PollViewSet, QuestionViewSet, AnswerViewSet
from survey.users.views import AuthToken

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='polls list')
router.register(r'questions', QuestionViewSet, basename='questions list')
router.register(r'answers', AnswerViewSet, basename='answers list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='api/v1/', view=include(router.urls)),
    path(route='api-token-auth/', view=AuthToken.as_view()),
]
