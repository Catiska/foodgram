# from django.core.exceptions import ValidationError
# from django.shortcuts import get_object_or_404
# from recipes.models import Ingredient, Tag
#

# def validate_ingredients(ingredients):
#     if not ingredients:
#         raise ValidationError({
#             'ingredients': 'Из воздуха каши не сваришь, добавьте ингредиенты'})
#     valid_ingredients = []
#     for item in ingredients:
#         ingredient = get_object_or_404(Ingredient, id=item['id'])
#         if ingredient in valid_ingredients:
#             raise ValidationError({
#                 'ingredients': 'Ингредиенты не должны дублироваться'})
#         valid_ingredients.append(ingredient)
#         if int(item['amount']) < 1:
#             raise ValidationError({
#                 'ingredients': 'Добавьте корректное количество ингредиента, '
#                                'значение должно быть больше 0'
#             })
#     return ingredients
#
#
# def validate_tags(tags):
#     if not tags:
#         raise ValidationError({
#             'tags': 'Нужно выбрать хотя бы оин тэг'
#         })
#     valid_tags = []
#     for tag in tags:
#         if not Tag.objects.filter(id__in=tags).exists():
#             raise ValidationError({
#                 'tags': 'Такой тэг пока не добавили, обратитесь к админу :)'
#             })
#         if tag in valid_tags:
#             raise ValidationError({
#                 'tags': 'Вы уже добавили этот тэг, проверьте :)'
#             })
#         valid_tags.append(tag)
#     return tags
#
#
# def validate_cooking_time(cooking_time):
#     if int(cooking_time) < 1:
#         raise ValidationError({
#             'cooking_time': 'Введите корректное время готовки, оно должно '
#                             'быть больше 1'
#         })
#     return cooking_time
