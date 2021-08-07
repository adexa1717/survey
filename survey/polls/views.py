from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from survey.polls.models import Poll, Question, Answer
from survey.polls.serializers import PollSerializer, PollWithQuestionsSerializer, QuestionSerializer, \
    QuestionCreateSerializer, QuestionWithPollSerializer, AnswerSerializer, AnswerCreateSerializer, GiveAnswerSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_admin and self.action == 'list':
            queryset = self.queryset.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())
        else:
            queryset = self.queryset

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PollWithQuestionsSerializer
        return self.serializer_class


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionWithPollSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return QuestionCreateSerializer
        if self.action == 'retrieve':
            return QuestionSerializer
        if self.action == 'give_answer':
            return GiveAnswerSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True)
    def give_answer(self, request, pk):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.give_answer(data=serializer.validated_data, pk=pk, user=request.user)
        return Response('or')


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return AnswerCreateSerializer
        return self.serializer_class
