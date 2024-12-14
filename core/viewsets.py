from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.serializers import RegisterSerializer
from core import models, serializers, filters
from core.models import UserProfile

# UserProfileViewSet: classe que gerencia a lógica de visualização (views) para o modelo UserProfile,
# implementando métodos personalizados para manipular os perfis de usuário.

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
        except UserProfile.DoesNotExist:
            profile = UserProfile()
            profile.weight = weight
            profile.age = age
            profile.height = height
            profile.login = user
            profile.login.first_name = first_name
            profile.login.last_name = last_name
            profile.login.save()
            self.save = profile.save()
        return Response({}, status=status.HTTP_200_OK)

    # Este método permite que o usuário autenticado atualize seu próprio perfil.
    #  A atualização é feita com base nos dados enviados no corpo da requisição (request.data).

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

# Este método retorna os dados do perfil do usuário autenticado.


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

# get_queryset: Este método personaliza o comportamento padrão do conjunto de dados (queryset).
# Em vez de retornar todos os objetos, ele filtra os treinamentos apenas para o usuário autenticado (request.user).
# Usado na listagem de treinos

# perform_create: ste método é chamado automaticamente ao criar um novo treinamento (POST /trainings/).
# Ele associa o usuário autenticado ao treinamento criado.


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

# Este método sobrescreve o comportamento padrão para ajustar o conjunto de dados com base no contexto da requisição.
# Se training for especificado: Lista exercícios apenas daquele treino.
# Se não for especificado: Lista exercícios dos treinos pertencentes ao usuário autenticado.


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

# get_queryset: Filtra os objetos Meal para incluir apenas as refeições associadas ao usuário autenticado (self.request.user).
# perform_create: garante que a refeição criada seja automaticamente associada ao usuário autenticado.


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

# Personaliza o conjunto de dados retornado pela API com base nos parâmetros da URL e no contexto do usuário autenticado.



class UserLogIn(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username
        })


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



# As classes UserLogIn e RegisterView são implementações específicas para gerenciar autenticação e registro de usuários

# class UserLogIn(ObtainAuthToken):

# O que é ObtainAuthToken?
# ObtainAuthToken é uma view genérica do DRF usada para autenticar usuários e gerar tokens para autenticação via TokenAuthentication.
# Ele usa um serializer padrão para validar as credenciais do usuário (username e password) e retornar um token de autenticação.

# O que faz a classe UserLogIn?
# Sobrescreve o método post da classe base para personalizar o comportamento ao fazer login.
# Quando o usuário envia as credenciais (username e password), o sistema:
# Valida as credenciais usando o serializer padrão da classe base.
# Recupera o usuário associado às credenciais.
# Cria ou recupera um token para esse usuário.
# Retorna uma resposta contendo:
# token: O token de autenticação gerado.
# id: O ID do usuário autenticado.
# username: O nome de usuário do usuário autenticado.

#-----------------------------------------------
# class RegisterView(generics.CreateAPIView):

# O que é CreateAPIView?
# CreateAPIView é uma view genérica do DRF que fornece uma implementação padrão para criar novos objetos no banco de dados.

# O que faz a classe RegisterView?
# Permite que novos usuários sejam registrados.
# Usa um serializer (RegisterSerializer) para validar os dados de entrada e criar um novo usuário.