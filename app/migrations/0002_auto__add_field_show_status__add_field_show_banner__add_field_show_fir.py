# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Show.status'
        db.add_column('app_show', 'status', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Show.banner'
        db.add_column('app_show', 'banner', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Show.first_aired'
        db.add_column('app_show', 'first_aired', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)

        # Adding field 'Show.imdb'
        db.add_column('app_show', 'imdb', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Show.status'
        db.delete_column('app_show', 'status')

        # Deleting field 'Show.banner'
        db.delete_column('app_show', 'banner')

        # Deleting field 'Show.first_aired'
        db.delete_column('app_show', 'first_aired')

        # Deleting field 'Show.imdb'
        db.delete_column('app_show', 'imdb')


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
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Show']"})
        },
        'app.show': {
            'Meta': {'object_name': 'Show'},
            'banner': ('django.db.models.fields.TextField', [], {}),
            'first_aired': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.TextField', [], {}),
            'tvdbid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['app']
