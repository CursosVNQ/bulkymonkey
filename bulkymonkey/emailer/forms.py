# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils.translation import ugettext_lazy as _

import floppyforms as forms

from .models import Campaign, Sector


class DeleteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Delete')))
        super(DeleteForm, self).__init__(*args, **kwargs)


class CampaignForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))
        super(CampaignForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Campaign
        fields = ('title', 'html_mail')


class SectorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))
        super(SectorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Sector
        fields = ('name',)
