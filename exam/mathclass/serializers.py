from rest_framework import serializers
from .models import Question, Option, Answer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class OptionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('detail', 'correct')


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('detail', 'question', 'correct')


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('detail', 'difficulties', 'options')


class QuestionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('detail', 'difficulties')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'options')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        user.is_active = False
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']

        users_group = Group.objects.get(name='Student')
        user.groups.add(users_group)

        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'options')
        depth=1
