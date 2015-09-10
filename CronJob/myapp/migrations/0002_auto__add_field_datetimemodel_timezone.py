# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DateTimeModel.timezone'
        db.add_column(u'myapp_datetimemodel', 'timezone',
                      self.gf('django.db.models.fields.TextField')(default='America/Los_Angeles', max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DateTimeModel.timezone'
        db.delete_column(u'myapp_datetimemodel', 'timezone')


    models = {
        u'myapp.datetimemodel': {
            'Meta': {'object_name': 'DateTimeModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'now': ('django.db.models.fields.DateTimeField', [], {}),
            'timezone': ('django.db.models.fields.TextField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['myapp']