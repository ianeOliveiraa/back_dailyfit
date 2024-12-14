from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import models, serializers, filters
from core.models import UserProfile


class UserProfileViewSet(viewsets.ViewSet):
    queryset = models.UserProfile.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user = request.user
        first_name = request.data['login']['first_name']
        last_name = request.data['login']['last_name']
        age = request.data['age']
        weight = request.data['weight']
        height = request.data['height']

        try:
            profile = UserProfile.objects.get(login=user)
            profile.weight = weight
            profile.age = age
            profile.height = height
            profile.login.first_name = first_name
            profile.login.last_name = last_name
            profile.login.save()
            profile.save()
            print("Perfil no bloco try")
        except UserProfile.DoesNotExist:
            print("Entrou no bloco except")
            profile = UserProfile()
            profile.weight = weight
            profile.age = age
            profile.height = height
            profile.login = user
            profile.login.first_name = first_name
            profile.login.last_name = last_name
            profile.login.save()
            profile.save()
            print("Novo perfil")
        return Response({}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user

        try:
            profile = UserProfile.objects.get(login=user)
            serializer = serializers.UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            profile = UserProfile()
            profile.login = user
            serializer = serializers.UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)


class MuscleGroupViewSet(viewsets.ModelViewSet):
    queryset = models.MuscleGroup.objects.all()
    serializer_class = serializers.MuscleGroupSerializer
    filter_backends = [DjangoFilterBackend]


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = models.Exercise.objects.all()
    serializer_class = serializers.ExerciseSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = models.Training.objects.all()
    serializer_class = serializers.TrainingSerializer
    filterset_class = filters.TrainingFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return models.Training.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TrainingExerciseViewSet(viewsets.ModelViewSet):
    queryset = models.TrainingExercise.objects.all()
    serializer_class = serializers.TrainingExerciseSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        training_id = self.request.query_params.get('training')
        if training_id:
            return models.TrainingExercise.objects.filter(training__id=training_id)
        return models.TrainingExercise.objects.select_related('training').filter(training__user=self.request.user).all()


class MealViewSet(viewsets.ModelViewSet):
    queryset = models.Meal.objects.all()
    serializer_class = serializers.MealSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return models.Meal.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = models.Food.objects.all()
    serializer_class = serializers.FoodSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]


class MealFoodViewSet(viewsets.ModelViewSet):
    queryset = models.MealFood.objects.all()
    serializer_class = serializers.MealFoodSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        meal_id = self.request.query_params.get('diet')
        if meal_id:
            return models.MealFood.objects.filter(meal__id=meal_id)
        return models.MealFood.objects.select_related('meal').filter(meal__user=self.request.user).all()


