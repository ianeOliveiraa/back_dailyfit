from rest_framework import routers

from core import viewsets

router = routers.DefaultRouter()

router.register('userprofile', viewsets.UserProfileViewSet)
router.register('muscleGroup', viewsets.MuscleGroupViewSet)
router.register('exercise', viewsets.ExerciseViewSet)
router.register('training', viewsets.TrainingViewSet)
router.register('training-exercise', viewsets.TrainingExerciseViewSet)
router.register('meal', viewsets.MealViewSet)
router.register('meal-food', viewsets.MealFoodViewSet)
router.register('food', viewsets.FoodViewSet)


urlpatterns = router.urls
