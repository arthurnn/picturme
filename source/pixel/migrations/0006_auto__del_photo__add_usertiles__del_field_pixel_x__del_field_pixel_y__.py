# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Photo'
        db.delete_table('pixel_photo')

        # Adding model 'UserTiles'
        db.create_table('pixel_usertiles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pixel.UserImage'])),
            ('pixel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pixel.Pixel'])),
            ('x', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('y', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('pixel', ['UserTiles'])

        # Deleting field 'Pixel.x'
        db.delete_column('pixel_pixel', 'x')

        # Deleting field 'Pixel.y'
        db.delete_column('pixel_pixel', 'y')

        # Deleting field 'Pixel.photo'
        db.delete_column('pixel_pixel', 'photo_id')

        # Deleting field 'Pixel.pos'
        db.delete_column('pixel_pixel', 'pos')

        # Adding field 'Pixel.image1'
        db.add_column('pixel_pixel', 'image1', self.gf('django.db.models.fields.files.ImageField')(default=0, max_length=100), keep_default=False)

        # Adding field 'Pixel.qr'
        db.add_column('pixel_pixel', 'qr', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Pixel.qg'
        db.add_column('pixel_pixel', 'qg', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Pixel.qb'
        db.add_column('pixel_pixel', 'qb', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'UserImage.thumbnail'
        db.add_column('pixel_userimage', 'thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100), keep_default=False)

        # Removing M2M table for field pixels on 'UserImage'
        db.delete_table('pixel_userimage_pixels')


    def backwards(self, orm):
        
        # Adding model 'Photo'
        db.create_table('pixel_photo', (
            ('image1', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('pixel', ['Photo'])

        # Deleting model 'UserTiles'
        db.delete_table('pixel_usertiles')

        # Adding field 'Pixel.x'
        db.add_column('pixel_pixel', 'x', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Pixel.y'
        db.add_column('pixel_pixel', 'y', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Pixel.photo'
        db.add_column('pixel_pixel', 'photo', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['pixel.Photo']), keep_default=False)

        # Adding field 'Pixel.pos'
        db.add_column('pixel_pixel', 'pos', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Deleting field 'Pixel.image1'
        db.delete_column('pixel_pixel', 'image1')

        # Deleting field 'Pixel.qr'
        db.delete_column('pixel_pixel', 'qr')

        # Deleting field 'Pixel.qg'
        db.delete_column('pixel_pixel', 'qg')

        # Deleting field 'Pixel.qb'
        db.delete_column('pixel_pixel', 'qb')

        # Deleting field 'UserImage.thumbnail'
        db.delete_column('pixel_userimage', 'thumbnail')

        # Adding M2M table for field pixels on 'UserImage'
        db.create_table('pixel_userimage_pixels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userimage', models.ForeignKey(orm['pixel.userimage'], null=False)),
            ('pixel', models.ForeignKey(orm['pixel.pixel'], null=False))
        ))
        db.create_unique('pixel_userimage_pixels', ['userimage_id', 'pixel_id'])


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
            'r': ('django.db.models.fields.PositiveIntegerField', [], {})
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
