from rest_framework import serializers

from survey.polls.consts import TEXT
from survey.polls.models import Poll, Question, Answer
from survey.users.models import UserAnswerQuestion


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'name', 'start_date', 'end_date', 'description')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text', 'id')


class AnswerCreateSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.exclude(type=TEXT))

    class Meta:
        model = Answer
        fields = ('text', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'answers')


class PollWithQuestionsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('start_date').read_only = True

    class Meta:
        model = Poll
        fields = ('id', 'name', 'start_date', 'end_date', 'description', "questions")


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('text', 'type', 'poll')


class QuestionWithPollSerializer(serializers.ModelSerializer):
    poll = PollSerializer()

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'poll')


class GiveAnswerSerializer(serializers.ModelSerializer):
    new_answer = serializers.CharField(allow_null=True)

    class Meta:
        model = Question
        fields = ('answers', 'new_answer')

    def validate(self, attrs):
        if ('answer' in attrs and (attrs['answer'] is not None or attrs['answer'] is not '')) and (
                'new_answer' in attrs and (attrs['new_answer'] is not None or not attrs['new_answer'] is not '')):
            raise serializers.ValidationError("must be only one answer")
        return attrs

    def give_answer(self, data, pk, user):
        if 'answers' in data:
            for answer in data['answers']:
                UserAnswerQuestion.objects.create(user=user, question=Question.objects.get(id=pk), answer=answer)
        elif 'new_answer' in data:
            UserAnswerQuestion.objects.create(user=user, question=Question.objects.get(id=pk),
                                              answer=data['new_answer'])
        else:
            raise serializers.ValidationError("no answer")
