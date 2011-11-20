# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Pixel.url'
        db.add_column('pixel_pixel', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Pixel.url'
        db.delete_column('pixel_pixel', 'url')


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
            'user_image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pixel.UserImage']"}),
            'x': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['pixel']
