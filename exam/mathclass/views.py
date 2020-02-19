from rest_framework import status
from .models import Question, Option, Answer
from .serializers import QuestionSerializer, QuestionAddSerializer, OptionAddSerializer, OptionSerializer, AnswerSerializer, UserSerializer, ResultSerializer
from django.http import JsonResponse, Http404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from django.core.mail import send_mail

class QuestionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        serializer = QuestionAddSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return JsonResponse(serializer.data)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        question.delete()
        return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)


class OptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Option.objects.filter(question=id)
        except Option.DoesNotExist:
            raise Http404

    def get(self, request, question_id, format=None):
        options = self.get_object(question_id)
        serializer = OptionSerializer(options, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, question_id, format=None):
        serializer = OptionAddSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(question_id=question_id)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        option = self.get_object(pk)
        serializer = OptionSerializer(option)
        option.delete()
        return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)


class AnswerView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        #if Group.objects.get(name='Student').user_set.filter(id=self.request.user.id).exists():
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)


class ResultView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, id):
        try:
            return Answer.objects.filter(user_id=id)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pupil_id, format=None):
        answers = self.get_object(pupil_id)
        serializer = ResultSerializer(answers, many=True)
        ans_data = self.check_ans(serializer.data)

        # Send email
        send_mail(
            'Test Score',
            'Result: '+ans_data['result']+", Percentage: "+str(ans_data['percent'])+"%",
            'from@wsp.com',
            [self.request.user.email],
            fail_silently=False,
        )

        return JsonResponse(
            {
                "result": ans_data['result'],
                "percent": str(ans_data['percent'])+"%",
                "answers": serializer.data
            })

    def check_ans(self, data):
        res = {}
        res['percent'] = ""
        res['result'] = "Pass"
        correct = 0
        for d in data:
            selected_options = d['options'].split(",") # 2,3
            selected_options = [int(i) for i in selected_options]
            selected_options.sort()

            correct_options_obj = Option.objects.filter(question=d['question']['id'], correct=1) #[2,3,4]
            correct_options = []
            for opt in correct_options_obj:
                correct_options.append(opt.id)
            correct_options.sort()

            if correct_options == selected_options:
                correct += 1

        res['percent'] = per=float(correct/len(data))*100

        if res['percent'] < settings.MIN_TO_PASS:
            res['result'] = "Fail"

        return res