from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StaffProfile, StudentProfile, TeacherProfile, SchoolProfile, LibrarianProfile


@receiver(post_save, sender=User)
def create_users(sender, instance, created, **kwargs):
    """
    This signal is used for automatically determining whether the created user is staff
    or is student or is teacher or is school and saves users information in Staffprofile or Studentprofile or Teacherprofile or Teacherprofile.
    """
    if created:
        if instance.user_type == 'TE':
            TeacherProfile.objects.create(user=instance)
        # if instance.user_type == 'ST':
        #     print('std')
        #     StudentProfile.objects.create(user=instance)
