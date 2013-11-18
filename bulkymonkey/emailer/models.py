from django.db import models
from django.db.models import permalink
from django.db.models.signals import post_delete
from django.db.models.fields.files import FileField
from django.utils.translation import ugettext_lazy as _
from .utils import get_filename_function

# Create your models here.


def delete_files_handler(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, FileField):
            f = getattr(instance, field.name)
            if f:
                f.delete(save=False)


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
    sectors = models.ManyToManyField('Sector', null=True)

    objects = EmailManager()

    def __str__(self):
        return self.address


class SentCampaignLog(TimeAwareModel):
    class Meta:
        ordering = ('-created_on',)

    campaign = models.ForeignKey('Campaign', verbose_name=_('Campaign'))
    sector = models.ForeignKey('Sector', verbose_name=_('Sector'))
    is_sent = models.BooleanField(_('Sent'), default=False)
    num_emails = models.IntegerField(_('Num of sent emails'))


class Sector(TimeAwareModel):
    class Meta:
        ordering = ['name']
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')

    name = models.CharField(_('Sector name'), max_length=50)

    @property
    def num_emails(self):
        return self.email_set.count()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('bulkymonkey:sector-detail', (), {'pk': self.id})

    @permalink
    def get_delete_url(self):
        return ('bulkymonkey:sector-delete', (), {'pk': self.id})


class Campaign(TimeAwareModel):
    class Meta:
        ordering = ['-created_on']
        verbose_name = _('Campaign')
        verbose_name_plural = _('Campaigns')

    title = models.CharField(_('Title'), max_length=50)
    html_mail = models.FileField(upload_to=get_filename_function('campaigns'))
    from_name = models.CharField(_('From (name)'), max_length=50)
    from_email = models.CharField(_('From (email)'), max_length=50)
    tags = models.CharField(_('Tags'), max_length=50, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('bulkymonkey:campaign-detail', (), {'pk': self.id})

    @permalink
    def get_delete_url(self):
        return ('bulkymonkey:campaign-delete', (), {'pk': self.id})

    def get_tags(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


post_delete.connect(delete_files_handler, Campaign)
