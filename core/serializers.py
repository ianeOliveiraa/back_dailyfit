from rest_framework import serializers
from core import models
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from core.models import MealFood


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

# Este serializer é responsável por serializar os dados do modelo padrão User (do Django).
# Ele expõe os campos username, first_name e last_name para leitura.


class UserProfileSerializer(serializers.ModelSerializer):
    login = LoginSerializer(many=False)

    class Meta:
        model = models.UserProfile
        exclude = ['created_at']

# Serializa os dados do modelo UserProfile (perfil do usuário).
# Inclui os dados do LoginSerializer como um campo aninhado chamado login.
# Exclui o campo created_at do modelo.
# Permite a exibição de informações completas do perfil do usuário, incluindo os dados básicos (nome, sobrenome e username)
# por meio do campo aninhado login.


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MuscleGroup
        exclude = ['created_at']

# Serializa os dados do modelo MuscleGroup, excluindo o campo created_at.
# Usado para expor os dados do grupo muscular em formato JSON, ignorando o campo created_at.


class ExerciseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Exercise
        exclude = ['created_at']
        extra_kwargs = {
            'id': {'read_only': False}
        }

# Serializa os dados do modelo Exercise (exercício).
# Configura o campo id como editável ao sobrescrever extra_kwargs.
#Permite o uso de um ID customizado durante operações como criação ou atualização.


class TrainingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = LoginSerializer(many=False, required=False, read_only=True)

    class Meta:
        model = models.Training
        exclude = ['created_at']
        extra_kwargs = {
            'id': {'read_only': False}
        }

# serializa os dados do modelo Training (treino).
# Inclui os dados do usuário (LoginSerializer) de forma aninhada.
# Permite o uso de um ID customizado para operações específicas.


class TrainingExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(many=False, read_only=True)
    training = TrainingSerializer(many=False, read_only=True)

    class Meta:
        model = models.TrainingExercise
        exclude = ['created_at']

# Serializa os dados do modelo TrainingExercise (relação entre treino e exercício).
# Inclui os dados do exercício e do treino de forma aninhada.

    def create(self, validated_data):
        exercise = models.Exercise.objects.get(id=validated_data.pop('exercise').get("id"))
        training = models.Training.objects.get(id=validated_data.pop('training').get("id"))

        return models.TrainingExercise.objects.create(
            exercise=exercise, training=training, **validated_data
        )

    # create:
    # Recebe os IDs de exercise e training no corpo da requisição.
    # Recupera os objetos correspondentes no banco e cria um TrainingExercise.

    def update(self, instance, validated_data):
        instance.exercise = models.Exercise.objects.get(id=validated_data.pop('exercise').get("id"))
        instance.training = models.Training.objects.get(id=validated_data.pop('training').get("id"))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    # update:
    # Atualiza um TrainingExercise existente com base nos IDs fornecidos.

    def to_internal_value(self, data):
        exercise_data = data.get('exercise')
        training_data = data.get('training')

        if not exercise_data or 'id' not in exercise_data:
            raise serializers.ValidationError({"exercise": "ID do exercício é obrigatório."})
        if not training_data or 'id' not in training_data:
            raise serializers.ValidationError({"training": "ID do treino é obrigatório."})

        internal_data = super().to_internal_value(data)
        internal_data['exercise'] = exercise_data
        internal_data['training'] = training_data
        return internal_data

    # to_internal_value:
    # Valida se os dados aninhados de exercise e training contêm os IDs necessários.
    # Converte os dados JSON recebidos para um formato interno utilizado pelo serializer.


class MealSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    total_calories = serializers.SerializerMethodField()

    class Meta:
        model = models.Meal
        exclude = ['created_at', 'user']
        extra_kwargs = {
            'id': {'read_only': False}
        }

# Serializa os dados do modelo Meal (refeição).
# Os campos created_at e user não serão incluídos nem no JSON de saída, nem no JSON de entrada.
# Isso é útil para ocultar informações que não precisam ser manipuladas diretamente pela API.
# Calcula as calorias totais de uma refeição com base nos alimentos associados.

    def get_total_calories(self, obj):
        meal_foods = MealFood.objects.filter(meal=obj)
        resultado = 0

        for meal_food in meal_foods:
            if meal_food.value <= 0 or meal_food.food.value <= 0:
                continue
            total_food = (meal_food.value / meal_food.food.value) * meal_food.food.total_kcal
            resultado += total_food

        return resultado


class FoodSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Food
        exclude = ['created_at']
        extra_kwargs = {
            'id': {'read_only': False}
        }

#Serializa os dados do modelo Food (alimento).


class MealFoodSerializer(serializers.ModelSerializer):
    meal = MealSerializer(many=False, read_only=True)
    food = FoodSerializer(many=False, read_only=True)

    class Meta:
        model = models.MealFood
        exclude = ['created_at']

# Serializa a relação entre Meal e Food.

    def create(self, validated_data):
        meal = models.Meal.objects.get(id=validated_data.pop('meal').get("id"))
        food = models.Food.objects.get(id=validated_data.pop('food').get("id"))

        return models.MealFood.objects.create(
            meal=meal, food=food, **validated_data
        )

    def update(self, instance, validated_data):
        instance.meal = models.Meal.objects.get(id=validated_data.pop('meal').get("id"))
        instance.food = models.Food.objects.get(id=validated_data.pop('food').get("id"))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_internal_value(self, data):
        meal_data = data.get('meal')
        food_data = data.get('food')

        if not meal_data or 'id' not in meal_data:
            raise serializers.ValidationError({"meal": "ID do meal é obrigatório."})
        if not food_data or 'id' not in food_data:
            raise serializers.ValidationError({"food": "ID do food é obrigatório."})

        internal_data = super().to_internal_value(data)
        internal_data['meal'] = meal_data
        internal_data['food'] = food_data
        return internal_data

# create e update:
# Recuperam os objetos Meal e Food e criam/atualizam a relação.

# to_internal_value:
# Valida se os IDs de meal e food foram fornecidos corretamente.


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True)

# Serializa dados para registrar um novo usuário.

    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

# create:
# Cria um novo usuário no banco de dados, definindo a senha de forma segura com set_password.