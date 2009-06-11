from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class FavoriteManager(models.Manager):
    """ A Manager for Favorites
    """
    def favorites_for_user(self, user):
        """ Returns Favorites for a specific user
        """
        return self.get_query_set().filter(user=user)
    
    def favorites_for_model(self, model):
        """ Returns Favorites for a specific model
        """
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content_type=content_type)

    def favorites_for_object(self, obj):
        """ Returns Favorites for a specific object
        """
        content_type = ContentType.objects.get_for_model(type(obj))
        return self.filter(content_type=content_type, object_id=obj.pk)

    @classmethod
    def create_favorite(cls, user, content_object):
        content_type = ContentType.objects.get_for_model(type(content_object))
        favorite = Favorite(
            user=user,
            content_type=content_type,
            object_id=content_object.pk,
            content_object=content_object
            )
        favorite.save()
        return favorite

class Favorite(models.Model):
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    created_on = models.DateTimeField(auto_now_add=True)
    
    objects = FavoriteManager()

    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')
        unique_together = (('user', 'content_type', 'object_id'),)
    
    def __unicode__(self):
        return "%s likes %s" % (self.user, self.content_object)



