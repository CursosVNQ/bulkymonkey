from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class TimeAwareModel(models.Model):
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True)
    modified_on = models.DateTimeField(_('Modified on'), auto_now=True)


class EmailManager(models.Manager):

    def by_sector(self, sector):
        """
        Returns a queryset filtered by sector
        """

        return self.get_queryset().filter(sector__name=sector)


class Email(TimeAwareModel):
    class Meta:
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')

    address = models.EmailField(_('Email address'), unique=True)
    sector = models.ForeignKey('Sector', null=True)

    objects = EmailManager()

    def __str__(self):
        return self.address


class Sector(TimeAwareModel):
    class Meta:
        ordering = ['name']
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')

    name = models.CharField(_('Sector name'), max_length=50)

    @property
    def num_emails(self):
        return Email.objects.filter(sector=self).count()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
