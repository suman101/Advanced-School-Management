from .models import Mailboxes
from rest_framework import serializers


class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mailboxes
        fields=('sender','subject','send_to','body','file','draft','created_at')


class MailboxListSerializer(serializers.ModelSerializer):   
    class Meta:
        model=Mailboxes
        fields=('id','sender','subject','send_to','body','important','is_seen','file','created_at')


class MailboxUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Mailboxes
        fields=('id','sender','subject','send_to','body','file','draft')


class MailboxDetailSerializer(serializers.ModelSerializer):  
    class Meta:
        model=Mailboxes
        fields=('id','sender','subject','send_to','body','file', 'draft','created_at')


class MailSeenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailboxes
        fields = (
            "is_seen",
        )
        ReadOnlyField = ('id','sender','send_to','subject','body','file', 'draft')


class MailImportantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailboxes
        fields = (
            "important",
        )
        ReadOnlyField = ('id','sender','subject','send_to','body','file', 'draft')
