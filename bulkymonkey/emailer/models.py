from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class EmailManager(models.Manager):

    def by_kind(self, kind):
        """
        Returns a queryset with translated strings
        """

        return self.get_queryset().filter(kind=kind)


class Email(models.Model):
    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')

    address = models.EmailField(_('Email address'))
    kind = models.CharField(_('Kind'), max_length=50)
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True)
    modified_on = models.DateTimeField(_('Modified on'), auto_now=True)

    objects = EmailManager()

    def __str__(self):
        return self.address
