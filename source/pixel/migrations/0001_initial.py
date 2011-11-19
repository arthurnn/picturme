# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Pixel'
        db.create_table('pixel_pixel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image1', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image2', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image3', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('pixel', ['Pixel'])

        # Adding model 'UserImage'
        db.create_table('pixel_userimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('pixel', ['UserImage'])

        # Adding M2M table for field pixels on 'UserImage'
        db.create_table('pixel_userimage_pixels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userimage', models.ForeignKey(orm['pixel.userimage'], null=False)),
            ('pixel', models.ForeignKey(orm['pixel.pixel'], null=False))
        ))
        db.create_unique('pixel_userimage_pixels', ['userimage_id', 'pixel_id'])


    def backwards(self, orm):
        
        # Deleting model 'Pixel'
        db.delete_table('pixel_pixel')

        # Deleting model 'UserImage'
        db.delete_table('pixel_userimage')

        # Removing M2M table for field pixels on 'UserImage'
        db.delete_table('pixel_userimage_pixels')


    models = {
        'pixel.pixel': {
            'Meta': {'object_name': 'Pixel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        'pixel.userimage': {
            'Meta': {'object_name': 'UserImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pixels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pixel.Pixel']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['pixel']
