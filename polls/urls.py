from django.urls import path
from django.urls import reverse_lazy
from . import views


urlpatterns = [
    path(
        "",
        views.MyQuestionsView.as_view(
            template_name=("polls/questions.html"),
            success_url=reverse_lazy("questions"),
        ),
        name="questions",
    ),
    path("answers/", views.MyQuestionsListView.as_view(), name="answers"),
    path("answers/<int:pk>", views.MyAnswersView.as_view(), name="answers_detail"),
    path(
        "answers/<int:pk>/delete",
        views.MyAnswerDeleteView.as_view(),
        name="answers_delete",
    ),
]
