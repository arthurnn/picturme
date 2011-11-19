# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Pixel.image3'
        db.delete_column('pixel_pixel', 'image3')

        # Deleting field 'Pixel.image2'
        db.delete_column('pixel_pixel', 'image2')

        # Adding field 'Pixel.r'
        db.add_column('pixel_pixel', 'r', self.gf('django.db.models.fields.PositiveIntegerField')(default=255), keep_default=False)

        # Adding field 'Pixel.g'
        db.add_column('pixel_pixel', 'g', self.gf('django.db.models.fields.PositiveIntegerField')(default=255), keep_default=False)

        # Adding field 'Pixel.b'
        db.add_column('pixel_pixel', 'b', self.gf('django.db.models.fields.PositiveIntegerField')(default=255), keep_default=False)

        # Adding field 'Pixel.pos'
        db.add_column('pixel_pixel', 'pos', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Pixel.image3'
        db.add_column('pixel_pixel', 'image3', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Adding field 'Pixel.image2'
        db.add_column('pixel_pixel', 'image2', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Deleting field 'Pixel.r'
        db.delete_column('pixel_pixel', 'r')

        # Deleting field 'Pixel.g'
        db.delete_column('pixel_pixel', 'g')

        # Deleting field 'Pixel.b'
        db.delete_column('pixel_pixel', 'b')

        # Deleting field 'Pixel.pos'
        db.delete_column('pixel_pixel', 'pos')


    models = {
        'pixel.pixel': {
            'Meta': {'object_name': 'Pixel'},
            'b': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'g': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pos': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'r': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'pixel.userimage': {
            'Meta': {'object_name': 'UserImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pixels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pixel.Pixel']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['pixel']
