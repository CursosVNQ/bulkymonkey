# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Campaign.title'
        db.alter_column(u'emailer_campaign', 'title', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'Campaign.title'
        db.alter_column(u'emailer_campaign', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        u'emailer.campaign': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Campaign', '_ormbases': [u'emailer.TimeAwareModel']},
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'html_mail': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'timeawaremodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['emailer.TimeAwareModel']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'emailer.email': {
            'Meta': {'object_name': 'Email', '_ormbases': [u'emailer.TimeAwareModel']},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'sectors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['emailer.Sector']", 'null': 'True', 'symmetrical': 'False'}),
            u'timeawaremodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['emailer.TimeAwareModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'emailer.sector': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sector', '_ormbases': [u'emailer.TimeAwareModel']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'timeawaremodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['emailer.TimeAwareModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'emailer.sentcampaignlog': {
            'Meta': {'ordering': "('-created_on',)", 'object_name': 'SentCampaignLog', '_ormbases': [u'emailer.TimeAwareModel']},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emailer.Campaign']"}),
            'is_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'num_emails': ('django.db.models.fields.IntegerField', [], {}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emailer.Sector']"}),
            u'timeawaremodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['emailer.TimeAwareModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'emailer.timeawaremodel': {
            'Meta': {'object_name': 'TimeAwareModel'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['emailer']