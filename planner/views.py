from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import TravelProject, ProjectPlace
from .serializers import TravelProjectSerializer, ProjectPlaceSerializer

class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all()
    serializer_class = TravelProjectSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'name']

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        
        # Чи є відвідані місця (тоді не можна видаляти)
        if project.places.filter(is_visited=True).exists():
            return Response(
                {"error": "Cannot delete project with visited places."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return super().destroy(request, *args, **kwargs)

class ProjectPlaceViewSet(viewsets.ModelViewSet):
    queryset = ProjectPlace.objects.all()
    serializer_class = ProjectPlaceSerializer
    ordering_fields = ['is_visited']

    def get_queryset(self):
        queryset = super().get_queryset()
        project_id = self.request.query_params.get('project_id')
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)
            
        return queryset