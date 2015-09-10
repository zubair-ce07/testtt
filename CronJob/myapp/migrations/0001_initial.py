# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DateTimeModel'
        db.create_table(u'myapp_datetimemodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('now', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'myapp', ['DateTimeModel'])


    def backwards(self, orm):
        # Deleting model 'DateTimeModel'
        db.delete_table(u'myapp_datetimemodel')


    models = {
        u'myapp.datetimemodel': {
            'Meta': {'object_name': 'DateTimeModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'now': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['myapp']