# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Photo'
        db.create_table('pixel_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image1', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('pixel', ['Photo'])

        # Deleting field 'Pixel.image1'
        db.delete_column('pixel_pixel', 'image1')

        # Adding field 'Pixel.photo'
        db.add_column('pixel_pixel', 'photo', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['pixel.Photo']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Photo'
        db.delete_table('pixel_photo')

        # Adding field 'Pixel.image1'
        db.add_column('pixel_pixel', 'image1', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Deleting field 'Pixel.photo'
        db.delete_column('pixel_pixel', 'photo_id')


    models = {
        'pixel.photo': {
            'Meta': {'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'pixel.pixel': {
            'Meta': {'object_name': 'Pixel'},
            'b': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'g': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pixel.Photo']"}),
            'pos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'r': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'x': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'y': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'pixel.userimage': {
            'Meta': {'object_name': 'UserImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'pixels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pixel.Pixel']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['pixel']
