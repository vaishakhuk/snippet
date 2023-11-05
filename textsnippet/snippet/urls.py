from django.urls import path
from . import views

urlpatterns = [
    path('api/snippet-list/', views.SnippetListAPIView.as_view(), name='snippet-list'),
    path('api/snippet-create/', views.SnippetCreateView.as_view(), name='create-snippet'),
    path('api/snippets/<int:pk>/', views.SnippetRetrieveView.as_view(), name='retrieve-snippet'),
    path('api/snippets/<int:pk>/update/', views.SnippetUpdateView.as_view(), name='update-snippet'),
    path('api/snippets/delete/', views.SnippetDeleteView.as_view(), name='delete-snippets'),
    path('api/tag-list/', views.TagListAPIView.as_view(), name='tag-list'),
    path('api/tag-detail/<int:pk>/', views.TagLDetailListAPIView.as_view(), name='tag-detail'),
]