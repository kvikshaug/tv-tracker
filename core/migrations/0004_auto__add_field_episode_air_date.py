# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Episode.air_date'
        db.add_column('core_episode', 'air_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 30, 23, 23, 45, 171142)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Episode.air_date'
        db.delete_column('core_episode', 'air_date')


    models = {
        'core.episode': {
            'Meta': {'object_name': 'Episode'},
            'air_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['core.Season']"})
        },
        'core.season': {
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seasons'", 'to': "orm['core.Show']"})
        },
        'core.show': {
            'Meta': {'object_name': 'Show'},
            'banner': ('django.db.models.fields.TextField', [], {}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'first_aired': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb': ('django.db.models.fields.TextField', [], {}),
            'last_seen': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.TextField', [], {}),
            'tvdbid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['core']
