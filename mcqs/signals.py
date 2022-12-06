from django.db.models.signals import pre_save

from django.dispatch import receiver
from rest_framework.serializers import ValidationError
from mcqs.models import Questions, Quiz


@receiver(pre_save,sender = Quiz)
def check_num_of_questions(sender,instance,**kwargs):
    c = Questions.objects.filter(quiz__id = instance.id).count()
    if instance.total_question < c:
        raise ValidationError("Total question number exceded" )