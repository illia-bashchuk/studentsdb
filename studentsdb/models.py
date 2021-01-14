from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class StProfile(models.Model):

    """To keep extra user data"""
    # user mapping
    user = models.OneToOneField(User)

    class Meta(object):
        verbose_name = _(u"User Profile")
    # extra user data
    mobile_phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=_(u"Mobile Phone"),
        default='')
    home_phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=_(u"Home Phone"),
        default='')
    photo = models.ImageField(
        blank=True,
        verbose_name=_(u"Photo"),
        null=True)

    def __unicode__(self):
        return self.user.username
