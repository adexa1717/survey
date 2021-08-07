import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from survey.polls.models import Poll, Question, Answer


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]
        db_table = "user_db"

    is_admin = models.BooleanField(default=False)
    poll = models.ManyToManyField(Poll, null=True)


class UserAnswerQuestion(models.Model):
    class Meta:
        verbose_name = "Ответ пользователя на вопрос"
        verbose_name_plural = "Ответы пользователя нв вопрос"
        ordering = ["id"]
        db_table = "user_answer_question_db"
        constraints = [
            models.CheckConstraint(
                check=(
                              Q(answer__isnull=False) &
                              Q(new_answer__isnull=True)
                      ) | (
                              Q(answer__isnull=True) &
                              Q(new_answer__isnull=False)
                      ),
                name="only_one_answer",
            )
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    new_answer = models.TextField(verbose_name="текст своего ответа")
