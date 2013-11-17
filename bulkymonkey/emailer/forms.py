# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, Field
from crispy_forms.bootstrap import FormActions
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
        super(CampaignForm, self).__init__(*args, **kwargs)

        self.fields['title'].help_text = _('This title will be the subject of the email')
        self.fields['from_email'].help_text = _('The campaign will be sent from this email account')
        self.fields['html_mail'].help_text = _('HTML file with the content that will be sent to the users')
        self.fields['tags'].help_text = _('List of comma separated tags that can be used to identify emails in Mandrill (Optional)')

        # Crispy form
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Field('from_email'),
            Field('html_mail'),
            Field('tags'),
            FormActions(
                Button('cancel', _('Cancel'), onclick='history.go(-1);'),
                Submit('submit', _('Create')),
            )
        )

    class Meta:
        model = Campaign
        fields = ('title', 'from_email', 'html_mail', 'tags')


class SectorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SectorForm, self).__init__(*args, **kwargs)

        # Crispy form
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'),
            FormActions(
                Button('cancel', _('Cancel'), onclick='history.go(-1);'),
                Submit('submit', _('Create')),
            )
        )

    class Meta:
        model = Sector
        fields = ('name',)
