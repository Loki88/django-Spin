# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'spin_base_userprofile', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('spin_base', ['UserProfile'])

        # Adding M2M table for field blocked on 'UserProfile'
        db.create_table(u'spin_base_userprofile_blocked', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm['spin_base.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm['spin_base.userprofile'], null=False))
        ))
        db.create_unique(u'spin_base_userprofile_blocked', ['from_userprofile_id', 'to_userprofile_id'])

        # Adding model 'Relationship'
        db.create_table(u'spin_base_relationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('follower', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_following', to=orm['spin_base.UserProfile'])),
            ('followed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_followed', to=orm['spin_base.UserProfile'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('spin_base', ['Relationship'])

        # Adding model 'Spin'
        db.create_table(u'spin_base_spin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='spinned', to=orm['spin_base.UserProfile'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('respinned', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='respins', null=True, to=orm['spin_base.Spin'])),
        ))
        db.send_create_signal('spin_base', ['Spin'])

        # Adding model 'MultiSpin'
        db.create_table(u'spin_base_multispin', (
            (u'spin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['spin_base.Spin'], unique=True, primary_key=True)),
            ('multimedia_path', self.gf('django.db.models.fields.files.FileField')(max_length=254)),
        ))
        db.send_create_signal('spin_base', ['MultiSpin'])

        # Adding model 'Comment'
        db.create_table(u'spin_base_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spin_base.UserProfile'])),
            ('spin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='commented', to=orm['spin_base.Spin'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('spin_base', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'spin_base_userprofile')

        # Removing M2M table for field blocked on 'UserProfile'
        db.delete_table('spin_base_userprofile_blocked')

        # Deleting model 'Relationship'
        db.delete_table(u'spin_base_relationship')

        # Deleting model 'Spin'
        db.delete_table(u'spin_base_spin')

        # Deleting model 'MultiSpin'
        db.delete_table(u'spin_base_multispin')

        # Deleting model 'Comment'
        db.delete_table(u'spin_base_comment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'spin_base.comment': {
            'Meta': {'ordering': "['date']", 'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spin_base.UserProfile']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'spin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commented'", 'to': "orm['spin_base.Spin']"})
        },
        'spin_base.multispin': {
            'Meta': {'ordering': "['-date']", 'object_name': 'MultiSpin', '_ormbases': ['spin_base.Spin']},
            'multimedia_path': ('django.db.models.fields.files.FileField', [], {'max_length': '254'}),
            u'spin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['spin_base.Spin']", 'unique': 'True', 'primary_key': 'True'})
        },
        'spin_base.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'followed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_followed'", 'to': "orm['spin_base.UserProfile']"}),
            'follower': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_following'", 'to': "orm['spin_base.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spin_base.spin': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Spin'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'spinned'", 'to': "orm['spin_base.UserProfile']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'respinned': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'respins'", 'null': 'True', 'to': "orm['spin_base.Spin']"})
        },
        'spin_base.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': [u'auth.User']},
            'blocked': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'black_listed'", 'symmetrical': 'False', 'to': "orm['spin_base.UserProfile']"}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers'", 'symmetrical': 'False', 'through': "orm['spin_base.Relationship']", 'to': "orm['spin_base.UserProfile']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['spin_base']