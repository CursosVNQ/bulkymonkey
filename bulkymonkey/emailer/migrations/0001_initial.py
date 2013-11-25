# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TimeAwareModel'
        db.create_table(u'emailer_timeawaremodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'emailer', ['TimeAwareModel'])

        # Adding model 'Email'
        db.create_table(u'emailer_email', (
            (u'timeawaremodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['emailer.TimeAwareModel'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'emailer', ['Email'])

        # Adding M2M table for field sectors on 'Email'
        m2m_table_name = db.shorten_name(u'emailer_email_sectors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('email', models.ForeignKey(orm[u'emailer.email'], null=False)),
            ('sector', models.ForeignKey(orm[u'emailer.sector'], null=False))
        ))
        db.create_unique(m2m_table_name, ['email_id', 'sector_id'])

        # Adding model 'SentCampaignLog'
        db.create_table(u'emailer_sentcampaignlog', (
            (u'timeawaremodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['emailer.TimeAwareModel'], unique=True, primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emailer.Campaign'])),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emailer.Sector'])),
            ('is_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('num_emails', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'emailer', ['SentCampaignLog'])

        # Adding model 'Sector'
        db.create_table(u'emailer_sector', (
            (u'timeawaremodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['emailer.TimeAwareModel'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'emailer', ['Sector'])

        # Adding model 'Campaign'
        db.create_table(u'emailer_campaign', (
            (u'timeawaremodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['emailer.TimeAwareModel'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('html_mail', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('from_email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'emailer', ['Campaign'])


    def backwards(self, orm):
        # Deleting model 'TimeAwareModel'
        db.delete_table(u'emailer_timeawaremodel')

        # Deleting model 'Email'
        db.delete_table(u'emailer_email')

        # Removing M2M table for field sectors on 'Email'
        db.delete_table(db.shorten_name(u'emailer_email_sectors'))

        # Deleting model 'SentCampaignLog'
        db.delete_table(u'emailer_sentcampaignlog')

        # Deleting model 'Sector'
        db.delete_table(u'emailer_sector')

        # Deleting model 'Campaign'
        db.delete_table(u'emailer_campaign')


    models = {
        u'emailer.campaign': {
            'Meta': {'ordering': "['-created_on']", 'object_name': 'Campaign', '_ormbases': [u'emailer.TimeAwareModel']},
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'html_mail': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'timeawaremodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['emailer.TimeAwareModel']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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