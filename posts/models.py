from django.db import models
from authentication.models import StudentProfile, TeacherProfile
from custom_settings.models import BaseModel
from grade_and_subject.models import Grade
# Create your models here.


class Post(BaseModel):
    teacher=models.ForeignKey(TeacherProfile,on_delete=models.CASCADE,related_name='teacher_post')
    grade=models.ForeignKey(Grade,on_delete=models.CASCADE)
    content=models.TextField()

    def __str__(self):
        return f'{self.teacher.user.username}|{self.content}'


# class CommentManager(models.Manager):
#     def all(self):
#         qs=super(CommentManager,self).filter(parent=None)
#         return qs


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',null=True,blank=True)
    comment_by = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=255)
    #parent = models.ForeignKey(TeacherProfile, null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    #responsed_by = models.ForeignKey(TeacherProfile, null=True, blank=True, on_delete=models.CASCADE)
    #objects=CommentManager()

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        #try:
            return f'Comment by {self.comment_by.user.username} on {self.post}'
        # except:
        #     return f'comment by {self.parent.user.username} on {self.post}'

    # def children(self):
    #     return Comment.objects.filter(parent=self)

    # @property
    # def is_parent(self):
    #     if self.parent is not None:
    #         return False
    #     return True
    
class CommentReplies(BaseModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply_comments',null=True,blank=True)
    respond_by = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(max_length=255)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f'responsed by {self.respond_by.user.username} on {self.comment}'
        