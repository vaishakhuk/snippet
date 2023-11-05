from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from .models import TextSnippet, Tag
from .serializers import (
    SnippetListSerializer,
    SnippetCreateSerializer,
    TextSnippetdetailSerializer,
    TextSnippetUpdateSerializer,
    TagListSerializer,
    )


class OffsetPagination(LimitOffsetPagination):
    default_limit = 10 

class SnippetListAPIView(ListAPIView):
    """
        Api for listing available snippet
        Author:Vaishakh UK
        Date:05-11-2023
    """
    permission_classes = [IsAuthenticated]
    queryset = TextSnippet.objects.only("id", "title")
    serializer_class = SnippetListSerializer


class SnippetCreateView(CreateAPIView):
    """
        Api for create snippet
        Author:Vaishakh UK
        Date:05-11-2023
    """
    permission_classes = [IsAuthenticated]
    queryset = TextSnippet.objects.all()
    serializer_class = SnippetCreateSerializer

    def perform_create(self, serializer):
        data  = {}
        try:
            if serializer.is_valid():
                snippet = serializer.save(created_by=self.request.user)
                tags = self.request.data.get("tags")
                tag_objects = []
                for title in list(tags):
                    tag, created = Tag.objects.get_or_create(title=title)
                    tag_objects.append(tag)
                
                snippet.tags.set(tag_objects)
                data["message"] = "SuccessfullyCreate Snippet"
                data["status"] = "success"
                data["code"] = 200
            else:
                data["message"] = "failed to Create Snippet"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data["code"] = 422
        except Exception as exception:
            data["status"] = "failed"
            data["message"] = exception
            data["code"] = 500
        print(data)
        return data
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        http_code = data.pop("code", None)
        headers = self.get_success_headers(serializer.data)
        return Response(data=data, status=http_code)


class SnippetRetrieveView(RetrieveAPIView):
    """
        Api for get details of snippet
        Author:Vaishakh UK
        Date:05-11-2023
    """
    permission_classes = [IsAuthenticated]
    queryset = TextSnippet.objects.all()
    serializer_class = TextSnippetdetailSerializer


class SnippetUpdateView(UpdateAPIView):
    """
        Api for update snippet
        Author:Vaishakh UK
        Date:05-11-2023
    """
    permission_classes = [IsAuthenticated]
    queryset = TextSnippet.objects.all()
    serializer_class = TextSnippetUpdateSerializer
    def perform_update(self, serializer):
        snippet = serializer.save()
        tags = self.request.data.get("tags")
        tag_objects = []
        tag_title = []
        for title in list(tags):
            tag, created = Tag.objects.get_or_create(title=title)
            tag_objects.append(tag)
            tag_title.append(tag.title)
            snippet.tags.set(tag_objects)
    

class SnippetDeleteView(DestroyAPIView):
    """
        Api for delete snippets
        Author:Vaishakh UK
        Date:05-11-2023
    """
    permission_classes = [IsAuthenticated]
    queryset = TextSnippet.objects.all()
    serializer_class = TextSnippetdetailSerializer

    def destroy(self, request, *args, **kwargs):
        snippet_ids = request.data.get('snippet_ids', [])

        if not isinstance(snippet_ids, list):
            snippet_ids = [snippet_ids]

        deleted_snippets = []

        for snippet_id in snippet_ids:
            try:
                snippet = TextSnippet.objects.get(pk=snippet_id)
                serializer = self.get_serializer(snippet)
                deleted_snippets.append(serializer.data)
                snippet.delete()
            except TextSnippet.DoesNotExist:
                pass  # Handle not found snippets

        response_data = {
            'message':f"Selected snippets are successfully deleted",
            'deleted_snippets': deleted_snippets,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class TagListAPIView(ListAPIView):
    """
        Api for listing tags snippet
        Author:Vaishakh UK
        Date:05-11-2023
    """
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.only("id", "title")
    serializer_class = TagListSerializer


class TagLDetailListAPIView(ListAPIView):
    """
        Api for listing snippet of perticuler tags
        Author:Vaishakh UK
        Date:05-11-2023
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TextSnippetdetailSerializer
    def get_queryset(self):
        tag_id = self.kwargs.get('pk')
        queryset = TextSnippet.objects.filter(tags=tag_id)
        return queryset
        
    