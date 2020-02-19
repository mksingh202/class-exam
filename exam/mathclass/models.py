from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    difficulties_options = (
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
    )
    detail = models.TextField()
    difficulties = models.IntegerField(choices=difficulties_options, default=1)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __unicode__(self):
        return '%s %s' % (self.detail, self.difficulties)


class Option(models.Model):
    detail = models.TextField()
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"

    def __unicode__(self):
        return '%s %s %s' % (self.detail, self.question, self.correct)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
