import requests
from rest_framework import serializers
from .models import TravelProject, ProjectPlace
from django.db import transaction
from django.core.cache import cache

# Базовий серіалізатор (містить логіку валідації)
class BasePlaceSerializer(serializers.ModelSerializer):
    def validate_external_id(self, value):
        # перевіряємо кеш
        cache_key = f"artic_place_{value}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return value

        url = f"https://api.artic.edu/api/v1/artworks/{value}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                raise serializers.ValidationError(f"Place with ID {value} not found in Art Institute API.")
            
            # Зберігаємо в кеш на 1 годину
            cache.set(cache_key, True, timeout=3600)
            
        except requests.RequestException:
            raise serializers.ValidationError("External API is unavailable.")
        
        return value

# Для окремого створення місця
class ProjectPlaceSerializer(BasePlaceSerializer):
    class Meta:
        model = ProjectPlace
        fields = ['id', 'project', 'external_id', 'notes', 'is_visited']

# Для вкладеного створення (БЕЗ поля project)
class ProjectPlaceNestedSerializer(BasePlaceSerializer):
    class Meta:
        model = ProjectPlace
        fields = ['id', 'external_id', 'notes', 'is_visited']

# Серіалізатор проєкту
class TravelProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceNestedSerializer(many=True, required=False)
    
    is_completed = serializers.BooleanField(read_only=True)

    class Meta:
        model = TravelProject
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'places']

    def validate_places(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("A project cannot have more than 10 places.")
        return value

    def create(self, validated_data):
        places_data = validated_data.pop('places', [])
        
        with transaction.atomic():
            project = TravelProject.objects.create(**validated_data)
            
            for place_data in places_data:
                ProjectPlace.objects.create(project=project, **place_data)
                
        return project