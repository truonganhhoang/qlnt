# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Pupil.index'
        db.add_column('school_pupil', 'index', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Teacher.index'
        db.add_column('school_teacher', 'index', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding unique constraint on 'DiemDanh', fields ['student_id', 'term_id', 'time']
        db.create_unique('school_diemdanh', ['student_id_id', 'term_id_id', 'time'])

        # Adding field 'Class.index'
        db.add_column('school_class', 'index', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Removing unique constraint on 'DiemDanh', fields ['student_id', 'term_id', 'time']
        db.delete_unique('school_diemdanh', ['student_id_id', 'term_id_id', 'time'])

        # Deleting field 'Pupil.index'
        db.delete_column('school_pupil', 'index')

        # Deleting field 'Teacher.index'
        db.delete_column('school_teacher', 'index')

        # Deleting field 'Class.index'
        db.delete_column('school_class', 'index')


    models = {
        'app.membership': {
            'Meta': {'object_name': 'Membership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'org': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']"}),
            'user_admin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'app.organization': {
            'Meta': {'object_name': 'Organization'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'manager_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'school_level': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'upper_organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']", 'null': 'True', 'blank': 'True'}),
            'user_admin': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['app.Membership']", 'symmetrical': 'False'})
        },
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
        'school.block': {
            'Meta': {'object_name': 'Block'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '2'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']"})
        },
        'school.class': {
            'Meta': {'unique_together': "(('year_id', 'name'),)", 'object_name': 'Class'},
            'block_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Block']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'teacher_id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['school.Teacher']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'year_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Year']"})
        },
        'school.danhsachloailop': {
            'Meta': {'object_name': 'DanhSachLoaiLop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loai': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']"})
        },
        'school.diemdanh': {
            'Meta': {'unique_together': "(('student_id', 'time', 'term_id'),)", 'object_name': 'DiemDanh'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loai': ('django.db.models.fields.CharField', [], {'default': "'k'", 'max_length': '10'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"}),
            'time': ('django.db.models.fields.DateField', [], {})
        },
        'school.hanhkiem': {
            'Meta': {'object_name': 'HanhKiem'},
            'hk_ren_luyen_lai': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ren_luyen_lai': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'term1': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'term2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'year_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Year']"})
        },
        'school.khenthuong': {
            'Meta': {'object_name': 'KhenThuong'},
            'dia_diem': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hinh_thuc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'luu_hoc_ba': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'noi_dung': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']", 'null': 'True'}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']", 'null': 'True'}),
            'time': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        'school.kiluat': {
            'Meta': {'object_name': 'KiLuat'},
            'dia_diem': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hinh_thuc': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'luu_hoc_ba': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'noi_dung': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"}),
            'time': ('django.db.models.fields.DateField', [], {'blank': 'True'})
        },
        'school.mark': {
            'Meta': {'object_name': 'Mark'},
            'ck': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mieng_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_4': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_5': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_4': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_5': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_4': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_5': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sent_mark': ('django.db.models.fields.CharField', [], {'default': "'0000000000000000000'", 'max_length': '19'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']", 'null': 'True', 'blank': 'True'}),
            'subject_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Subject']"}),
            'tb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"})
        },
        'school.marktime': {
            'Meta': {'object_name': 'MarkTime'},
            'ck': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark_id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['school.Mark']", 'unique': 'True'}),
            'mieng_1': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_2': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_3': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_4': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mieng_5': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_1': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_2': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_3': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_4': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mlam_5': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_1': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_2': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_3': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_4': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mot_tiet_5': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tb': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'school.pupil': {
            'Meta': {'unique_together': "(('class_id', 'first_name', 'last_name', 'birthday'),)", 'object_name': 'Pupil'},
            'ban_dk': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'class_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Class']", 'null': 'True', 'blank': 'True'}),
            'current_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'current_status': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dan_toc': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'dang': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'disable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'father_birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'father_job': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'father_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'home_town': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'khu_vuc': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'mother_birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mother_job': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mother_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'mother_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'ngay_vao_dang': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ngay_vao_doan': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ngay_vao_doi': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'quoc_tich': ('django.db.models.fields.CharField', [], {'default': "'Vi\\xe1\\xbb\\x87t Nam'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']", 'null': 'True', 'blank': 'True'}),
            'school_join_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2011, 7, 28)'}),
            'school_join_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'Nam'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'sms_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'start_year_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.StartYear']"}),
            'ton_giao': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'school.startyear': {
            'Meta': {'object_name': 'StartYear'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']"}),
            'time': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        },
        'school.subject': {
            'Meta': {'object_name': 'Subject'},
            'class_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Class']"}),
            'hs': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'primary': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'teacher_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Teacher']", 'null': 'True', 'blank': 'True'})
        },
        'school.tbhocky': {
            'Meta': {'object_name': 'TBHocKy'},
            'danh_hieu_hk': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hl_hk': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_finish': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'number_subject': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'tb_hk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"})
        },
        'school.tbnam': {
            'Meta': {'object_name': 'TBNam'},
            'danh_hieu_nam': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hk_nam': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hl_nam': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hl_thi_lai': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'len_lop': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'number_finish': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'number_subject': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'tb_nam': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tb_thi_lai': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'thi_lai': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'tong_so_ngay_nghi': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Year']"})
        },
        'school.teacher': {
            'Meta': {'unique_together': "(('school_id', 'first_name', 'last_name', 'birthday'),)", 'object_name': 'Teacher'},
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'current_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dan_toc': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'home_town': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'quoc_tich': ('django.db.models.fields.CharField', [], {'default': "'Vi\\xe1\\xbb\\x87t Nam'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']"}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'Nam'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'sms_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'ton_giao': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'school.term': {
            'Meta': {'object_name': 'Term'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'year_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Year']"})
        },
        'school.tkdiemdanh': {
            'Meta': {'object_name': 'TKDiemDanh'},
            'co_phep': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'khong_phep': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"}),
            'tong_so': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'school.tkmon': {
            'Meta': {'object_name': 'TKMon'},
            'diem_thi_lai': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'subject_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Subject']"}),
            'tb_nam': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'thi_lai': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'school.year': {
            'Meta': {'object_name': 'Year'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']"}),
            'time': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['school']
