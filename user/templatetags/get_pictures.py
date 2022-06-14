from atexit import register
from django import template
from user.models import PreviousExprience, PreviousExprienceImages
register= template.Library()
@register.filter(name='get_pictures')
def get_pictures(id):
    PreviousExprience_obj = PreviousExprience.objects.get(id=id)

    PreviousExprienceImages_obj = PreviousExprienceImages.objects.filter(influencer=PreviousExprience_obj)
    return PreviousExprienceImages_obj[0].image.url