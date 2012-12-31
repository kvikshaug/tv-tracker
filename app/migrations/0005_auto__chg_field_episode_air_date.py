# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Episode.air_date'
        db.alter_column('app_episode', 'air_date', self.gf('django.db.models.fields.DateTimeField')(null=True))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Episode.air_date'
        raise RuntimeError("Cannot reverse this migration. 'Episode.air_date' and its values cannot be restored.")


    models = {
        'app.episode': {
            'Meta': {'object_name': 'Episode'},
            'air_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['app.Season']"})
        },
        'app.season': {
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seasons'", 'to': "orm['app.Show']"})
        },
        'app.show': {
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

    complete_apps = ['app']
