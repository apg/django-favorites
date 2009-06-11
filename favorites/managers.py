from django.db import models
from django.contrib.contenttypes.models import ContentType

from models import Favorite

class FavoritesManagerMixin(object):
    """ A Mixin to add a `favorite__favorite` column via extra 
    """
    def with_favorite_for(self, user, all=True):
        """ Adds a column favorite__favorite to the returned object, which
        indicates whether or not this item is a favorite for a user
        """
        content_type = ContentType.objects.get_for_model(self.model)
        pk_field = "%s.%s" % (self.model._meta.db_table,
                              self.model._meta.pk.column)

        favorite_sql = """(SELECT 1 FROM %(favorites_db_table)s 
WHERE %(favorites_db_table)s.object_id = %(pk_field)s and
      %(favorites_db_table)s.content_type_id = %(content_type)d and
      %(favorites_db_table)s.user_id = %(user_id)d)
""" % {'pk_field': pk_field, \
           'db_table': self.model._meta.db_table, \
           'favorites_db_table': Favorite._meta.db_table, \
           'user_id': user.pk, \
           'content_type': content_type.id, \
           }

        extras = {
            'select': {'favorite__favorite': favorite_sql},
            }

        if not all:
            extras['where'] = ['favorite__favorite == 1']

        return self.extra(**extras)
