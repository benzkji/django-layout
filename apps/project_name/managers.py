from django.conf import settings
from django.db import models


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def site(self):
        return self.filter(site=settings.SITE_ID)


# http://stackoverflow.com/questions/19703975/django-sort-by-distance
class NearbyQuerySet(PublishedQuerySet):
    def nearby(self, lat, lng, proximity):
        """
        Return all object which distance to specified coordinates
        is less than proximity given in kilometers
        """
        # Great circle distance formula
        gcd = """
              6371 * acos(
               cos(radians(%s)) * cos(radians(lat))
               * cos(radians(lng) - radians(%s)) +
               sin(radians(%s)) * sin(radians(lat))
              )
              """
        gcd_lt = "{} < %s".format(gcd)
        return self.exclude(lat=None)\
                   .exclude(lng=None)\
                   .extra(
                       select={'distance': gcd},
                       select_params=[lat, lng, lat],
                       where=[gcd_lt],
                       params=[lat, lng, lat, proximity],
                       order_by=['distance', ]
                   )
