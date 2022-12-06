from pyexpat import model
from attr import fields
from rest_framework import serializers
from .models import CommentReplies, Post,Comment


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields=('teacher','grade','content')




class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields=('id','teacher','grade','content')


class PostDetailSerializer(serializers.ModelSerializer):
    comments=  serializers.SerializerMethodField()  
    comment_count=serializers.SerializerMethodField()    
    teacher=serializers.StringRelatedField()
    class Meta:
        model = Post
        fields=('id','teacher','grade','content','comment_count','comments','created_at')
        # depth=1
    
    def get_comments(self,obj): 
        return Comment.objects.filter(post=obj.id).values('id','comment_by__user__username','content','created_at')    

    def get_comment_count(self,obj):
        return Comment.objects.filter(post=obj.id).values('id','comment_by__user__username','content','created_at').count()   


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('post','comment_by','content',)


# class CommentListSerializer(serializers.ModelSerializer):
#     comment_by=serializers.StringRelatedField()
#     class Meta:
#         model=Comment
#         fields=('id','post','comment_by','content',)

class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=('id','post','comment_by','content',)


class ReplyCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentReplies
        fields=('comment','respond_by','content',)


class ReplyCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentReplies
        fields=('id','comment','respond_by','content',)


class CommentRepliesListSerializer(serializers.ModelSerializer):
    respond_by=serializers.StringRelatedField()
    class Meta:
        model=CommentReplies
        fields=('id','comment','respond_by','content','created_at')


class CommentListSerializer(serializers.ModelSerializer):
    reply_comments=  serializers.SerializerMethodField()  
    reply_comments_count=serializers.SerializerMethodField() 
    comment_by=serializers.StringRelatedField()   
    class Meta:
        model = Comment
        fields=('id','post','comment_by','content','reply_comments','reply_comments_count','created_at')
        #depth=1
    
    def get_reply_comments(self,obj): 
        return CommentReplies.objects.filter(comment=obj.id).values('id','respond_by__user__username','content','created_at')    


    def get_reply_comments_count(self,obj):
        return CommentReplies.objects.filter(comment=obj.id).values('id','respond_by__user__username','content','created_at').count() 


class CommentDetailSerializer(serializers.ModelSerializer):
    reply_comments=  serializers.SerializerMethodField()  
    reply_comments_count=serializers.SerializerMethodField()
    comment_by=serializers.StringRelatedField() 
    class Meta:
        model = Comment
        fields=('id','post','comment_by','content','reply_comments','reply_comments_count','created_at')
        # depth=1
    
    def get_reply_comments(self,obj): 
        return CommentReplies.objects.filter(comment=obj.id).values('id','respond_by__user__username','content','created_at')    


    def get_reply_comments_count(self,obj):
        return CommentReplies.objects.filter(comment=obj.id).values('id','respond_by__user__username','content','created_at').count() 


# class CommentSerializer(serializers.ModelSerializer):
#     comment_reply_count=serializers.SerializerMethodField()
#     comment_by=serializers.StringRelatedField()
#     class Meta:
#         model=Comment
#         fields=('post','comment_by','content','created_at','reply_count',)

#     def get_comment_reply(self,obj): 
#         return Comment.objects.filter(post=obj.id).values('id','comment_by','content','created_at')    


#     def get_comment_reply_count(self,obj):
#         return Comment.objects.filter(post=obj.id).values('id','comment_by','content','created_at').count()
        
class PostlistSerializer(serializers.ModelSerializer):
    teacher=serializers.StringRelatedField()
    grade=serializers.StringRelatedField()
    comments=  CommentListSerializer(read_only=True,many=True)
    comments_count=  serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields=('id','teacher','grade','content', 'comments','comments_count','created_at')
        depth = 2
    
    # def get_comments(self,obj):
    #     return Comment.objects.filter(post=obj.id).values('id','comment_by__user__username','content','created_at') 

    def get_comments_count(self,obj):
        return Comment.objects.filter(post=obj.id).values('id','comment_by__user__username','content','created_at').count() 
