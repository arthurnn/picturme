# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'UserTiles.y'
        db.delete_column('pixel_usertiles', 'y')

        # Deleting field 'UserTiles.x'
        db.delete_column('pixel_usertiles', 'x')


    def backwards(self, orm):
        
        # Adding field 'UserTiles.y'
        db.add_column('pixel_usertiles', 'y', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'UserTiles.x'
        db.add_column('pixel_usertiles', 'x', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    models = {
        'pixel.pixel': {
            'Meta': {'object_name': 'Pixel'},
            'b': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'g': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'qb': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'qg': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'qr': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'r': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'pixel.userimage': {
            'Meta': {'object_name': 'UserImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pixels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pixel.Pixel']", 'through': "orm['pixel.UserTiles']", 'symmetrical': 'False'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'pixel.usertiles': {
            'Meta': {'object_name': 'UserTiles'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pixel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pixel.Pixel']"}),
            'user_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pixel.UserImage']"})
        }
    }

    complete_apps = ['pixel']
