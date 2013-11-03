# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Show'
        db.create_table('core_show', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tvdbid', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['Show'])

        # Adding model 'Season'
        db.create_table('core_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('show', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Show'])),
        ))
        db.send_create_signal('core', ['Season'])

        # Adding model 'Episode'
        db.create_table('core_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Season'])),
        ))
        db.send_create_signal('core', ['Episode'])


    def backwards(self, orm):
        
        # Deleting model 'Show'
        db.delete_table('core_show')

        # Deleting model 'Season'
        db.delete_table('core_season')

        # Deleting model 'Episode'
        db.delete_table('core_episode')


    models = {
        'core.episode': {
            'Meta': {'object_name': 'Episode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Season']"})
        },
        'core.season': {
            'Meta': {'object_name': 'Season'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Show']"})
        },
        'core.show': {
            'Meta': {'object_name': 'Show'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'tvdbid': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['core']
