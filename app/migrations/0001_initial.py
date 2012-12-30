# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Series'
        db.create_table('app_series', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('app', ['Series'])

        # Adding model 'Season'
        db.create_table('app_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Series'])),
        ))
        db.send_create_signal('app', ['Season'])

        # Adding model 'Episode'
        db.create_table('app_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Season'])),
        ))
        db.send_create_signal('app', ['Episode'])


    def backwards(self, orm):
        
        # Deleting model 'Series'
        db.delete_table('app_series')

        # Deleting model 'Season'
        db.delete_table('app_season')

        # Deleting model 'Episode'
        db.delete_table('app_episode')


    models = {
        'app.episode': {
            'Meta': {'object_name': 'Episode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Season']"})
        },
        'app.season': {
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Series']"})
        },
        'app.series': {
            'Meta': {'object_name': 'Series'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['app']
