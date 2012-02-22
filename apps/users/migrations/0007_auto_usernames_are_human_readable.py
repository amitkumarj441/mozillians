# encoding: utf-8
import re
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    no_dry_run = True

    def forwards(self, orm):
        for user in orm['auth.User'].objects.all():
            irc = user.get_profile().ircname
            user.username = 'u/'+user.username
            if irc and self.clean_username(irc, orm):
                    user.username = irc
            user.save()

    def clean_username(self, username, orm):
        # Don't be jacking somebody's username
        if orm.User.objects.filter(username=username):
            return False

        # No funky characters in username
        if not re.match(r'^[a-zA-Z0-9 .:,-]*$', username):
            return False

        return True

    def backwards(self, orm):
        # It doesn't really matter what the usernames are so we don't need to
        # have this.
        pass

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'groups.group': {
            'Meta': {'object_name': 'Group', 'db_table': "'group'"},
            'always_auto_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'system': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'url': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'users.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'profile'"},
            'bio': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'confirmation_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['groups.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ircname': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_vouched': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'photo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'vouched_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.UserProfile']", 'null': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['users']
