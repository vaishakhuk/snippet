from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from rest_framework.reverse import reverse
from .models import TextSnippet, Tag



class SnippetListSerializer(ModelSerializer):
    """
        Serializer for list snippet
    """
    link = SerializerMethodField(read_only=True)
    def get_link(self,obj):
        try:
            request = self.context.get('request')
            link = reverse(
                'retrieve-snippet',
                kwargs={'pk': obj.id },
                request=request
            )
            return link
        except:
            return None
        
    class Meta:
        model = TextSnippet
        fields = [
            "title","id", "link"
        ]


class SnippetCreateSerializer(ModelSerializer):
    """
        Serializer for create snippet
    """
    class Meta:
        model = TextSnippet
        fields = [
            'id',
            'title',
            'created_by',
            'content',
        ]


class TextSnippetdetailSerializer(ModelSerializer):
    """
        Serializer for get detail of snippet
    """
    class Meta:
        model = TextSnippet
        fields = [
            'id',
            'title',
            'created_by',
            'content',
            'timestamp'
        ]


class TextSnippetUpdateSerializer(ModelSerializer):
    """
        Serializer for update snippet
    """
    class Meta:
        model = TextSnippet
        fields = [
            'id',
            'title',
            'created_by',
            'content',
            'timestamp',
        ]

class TagListSerializer(ModelSerializer):
    """
        Serializer for list tag
    """
    class Meta:
        model = Tag
        fields = [
            "title","id"
        ]
