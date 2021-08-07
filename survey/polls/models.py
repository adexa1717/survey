from django.db import models

from survey.polls.consts import QuestionTypes, TEXT


class Poll(models.Model):
    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"
        ordering = ["id"]
        db_table = "polls_db"

    name = models.CharField(max_length=150, verbose_name="название")
    start_date = models.DateTimeField(editable=False, verbose_name="дата старта")
    end_date = models.DateTimeField(verbose_name="дата окончания")
    description = models.TextField(verbose_name="описание")


class Question(models.Model):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["id"]
        db_table = "question_db"

    text = models.TextField(verbose_name="текст вопроса")
    type = models.CharField(max_length=30, choices=QuestionTypes, default=TEXT)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='question')


class Answer(models.Model):
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ["id"]
        db_table = "answer_db"

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    text = models.TextField(verbose_name="текст ответа")
