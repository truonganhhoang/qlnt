# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DanhSachLoaiLop'
        db.create_table('school_danhsachloailop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('loai', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('school_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Organization'])),
        ))
        db.send_create_signal('school', ['DanhSachLoaiLop'])

        # Adding model 'Block'
        db.create_table('school_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.SmallIntegerField')(max_length=2)),
            ('school_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Organization'])),
        ))
        db.send_create_signal('school', ['Block'])

        # Adding model 'Teacher'
        db.create_table('school_teacher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dan_toc', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('ton_giao', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('quoc_tich', self.gf('django.db.models.fields.CharField')(default='Vi\xe1\xbb\x87t Nam', max_length=20, null=True, blank=True)),
            ('home_town', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='Nam', max_length=3, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('sms_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('current_address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('school_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Organization'])),
        ))
        db.send_create_signal('school', ['Teacher'])

        # Adding unique constraint on 'Teacher', fields ['school_id', 'first_name', 'last_name', 'birthday']
        db.create_unique('school_teacher', ['school_id_id', 'first_name', 'last_name', 'birthday'])

        # Adding model 'Year'
        db.create_table('school_year', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('school_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Organization'])),
        ))
        db.send_create_signal('school', ['Year'])

        # Adding model 'StartYear'
        db.create_table('school_startyear', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('school_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Organization'])),
        ))
        db.send_create_signal('school', ['StartYear'])

        # Adding model 'Term'
        db.create_table('school_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('year_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Year'])),
        ))
        db.send_create_signal('school', ['Term'])

        # Adding model 'Class'
        db.create_table('school_class', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(max_length=3, null=True, blank=True)),
            ('year_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Year'])),
            ('block_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Block'])),
            ('teacher_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Teacher'], null=True, blank=True)),
        ))
        db.send_create_signal('school', ['Class'])

        # Adding unique constraint on 'Class', fields ['year_id', 'name']
        db.create_unique('school_class', ['year_id_id', 'name'])

        # Adding model 'Pupil'
        db.create_table('school_pupil', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dan_toc', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('ton_giao', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('quoc_tich', self.gf('django.db.models.fields.CharField')(default='Vi\xe1\xbb\x87t Nam', max_length=20, null=True, blank=True)),
            ('home_town', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(default='Nam', max_length=3, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('sms_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('current_address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('school_join_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 7, 23))),
            ('ban_dk', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('school_join_mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('khu_vuc', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('doan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ngay_vao_doan', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('doi', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ngay_vao_doi', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dang', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ngay_vao_dang', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('father_birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('father_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('father_job', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('mother_name', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('mother_birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('mother_job', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('mother_phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('current_status', self.gf('django.db.models.fields.CharField')(default='OK', max_length=200, null=True, blank=True)),
            ('disable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('start_year_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.StartYear'])),
            ('class_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Class'], null=True, blank=True)),
            ('school_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Organization'], null=True, blank=True)),
        ))
        db.send_create_signal('school', ['Pupil'])

        # Adding unique constraint on 'Pupil', fields ['class_id', 'first_name', 'last_name', 'birthday']
        db.create_unique('school_pupil', ['class_id_id', 'first_name', 'last_name', 'birthday'])

        # Adding model 'Subject'
        db.create_table('school_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('hs', self.gf('django.db.models.fields.FloatField')()),
            ('class_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Class'])),
            ('teacher_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Teacher'], null=True, blank=True)),
        ))
        db.send_create_signal('school', ['Subject'])

        # Adding model 'Mark'
        db.create_table('school_mark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mieng_1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mieng_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mieng_3', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mieng_4', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mieng_5', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mlam_1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mlam_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mlam_3', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mlam_4', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mlam_5', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mot_tiet_1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mot_tiet_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mot_tiet_3', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mot_tiet_4', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mot_tiet_5', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ck', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('tb', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('subject_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Subject'])),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'], null=True, blank=True)),
            ('term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Term'])),
        ))
        db.send_create_signal('school', ['Mark'])

        # Adding model 'TKMon'
        db.create_table('school_tkmon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tb_nam', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('thi_lai', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('diem_thi_lai', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('subject_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Subject'])),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'])),
        ))
        db.send_create_signal('school', ['TKMon'])

        # Adding model 'KhenThuong'
        db.create_table('school_khenthuong', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'], null=True)),
            ('term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Term'], null=True)),
            ('time', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('hinh_thuc', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dia_diem', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('noi_dung', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('luu_hoc_ba', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('school', ['KhenThuong'])

        # Adding model 'KiLuat'
        db.create_table('school_kiluat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'])),
            ('term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Term'])),
            ('time', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('hinh_thuc', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('dia_diem', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('noi_dung', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('luu_hoc_ba', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('school', ['KiLuat'])

        # Adding model 'HanhKiem'
        db.create_table('school_hanhkiem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'])),
            ('term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Term'])),
            ('loai', self.gf('django.db.models.fields.CharField')(default=u'T', max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('school', ['HanhKiem'])

        # Adding model 'TBHocKy'
        db.create_table('school_tbhocky', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'])),
            ('term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Term'])),
            ('tb_hk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hl_hk', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('danh_hieu_hk', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('school', ['TBHocKy'])

        # Adding model 'TBNam'
        db.create_table('school_tbnam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'])),
            ('year_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Year'])),
            ('tb_nam', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hl_nam', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('hk_nam', self.gf('django.db.models.fields.CharField')(default=u'T', max_length=2, null=True, blank=True)),
            ('tong_so_ngay_nghi', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('danh_hieu_nam', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('len_lop', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('thi_lai', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('tb_thi_lai', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hl_thi_lai', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('ren_luyen_lai', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('hk_ren_luyen_lai', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('school', ['TBNam'])

        # Adding model 'DiemDanh'
        db.create_table('school_diemdanh', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'])),
            ('term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Term'])),
            ('time', self.gf('django.db.models.fields.DateField')()),
            ('loai', self.gf('django.db.models.fields.CharField')(default='k', max_length=10)),
        ))
        db.send_create_signal('school', ['DiemDanh'])

        # Adding model 'TKDiemDanh'
        db.create_table('school_tkdiemdanh', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Pupil'])),
            ('term_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.Term'])),
            ('tong_so', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('co_phep', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('khong_phep', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('school', ['TKDiemDanh'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Pupil', fields ['class_id', 'first_name', 'last_name', 'birthday']
        db.delete_unique('school_pupil', ['class_id_id', 'first_name', 'last_name', 'birthday'])

        # Removing unique constraint on 'Class', fields ['year_id', 'name']
        db.delete_unique('school_class', ['year_id_id', 'name'])

        # Removing unique constraint on 'Teacher', fields ['school_id', 'first_name', 'last_name', 'birthday']
        db.delete_unique('school_teacher', ['school_id_id', 'first_name', 'last_name', 'birthday'])

        # Deleting model 'DanhSachLoaiLop'
        db.delete_table('school_danhsachloailop')

        # Deleting model 'Block'
        db.delete_table('school_block')

        # Deleting model 'Teacher'
        db.delete_table('school_teacher')

        # Deleting model 'Year'
        db.delete_table('school_year')

        # Deleting model 'StartYear'
        db.delete_table('school_startyear')

        # Deleting model 'Term'
        db.delete_table('school_term')

        # Deleting model 'Class'
        db.delete_table('school_class')

        # Deleting model 'Pupil'
        db.delete_table('school_pupil')

        # Deleting model 'Subject'
        db.delete_table('school_subject')

        # Deleting model 'Mark'
        db.delete_table('school_mark')

        # Deleting model 'TKMon'
        db.delete_table('school_tkmon')

        # Deleting model 'KhenThuong'
        db.delete_table('school_khenthuong')

        # Deleting model 'KiLuat'
        db.delete_table('school_kiluat')

        # Deleting model 'HanhKiem'
        db.delete_table('school_hanhkiem')

        # Deleting model 'TBHocKy'
        db.delete_table('school_tbhocky')

        # Deleting model 'TBNam'
        db.delete_table('school_tbnam')

        # Deleting model 'DiemDanh'
        db.delete_table('school_diemdanh')

        # Deleting model 'TKDiemDanh'
        db.delete_table('school_tkdiemdanh')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'teacher_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Teacher']", 'null': 'True', 'blank': 'True'}),
            'year_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Year']"})
        },
        'school.danhsachloailop': {
            'Meta': {'object_name': 'DanhSachLoaiLop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loai': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Organization']"})
        },
        'school.diemdanh': {
            'Meta': {'object_name': 'DiemDanh'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loai': ('django.db.models.fields.CharField', [], {'default': "'k'", 'max_length': '10'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"}),
            'time': ('django.db.models.fields.DateField', [], {})
        },
        'school.hanhkiem': {
            'Meta': {'object_name': 'HanhKiem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loai': ('django.db.models.fields.CharField', [], {'default': "u'T'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"})
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
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']", 'null': 'True', 'blank': 'True'}),
            'subject_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Subject']"}),
            'tb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"})
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
            'school_join_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2011, 7, 23)'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'teacher_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Teacher']", 'null': 'True', 'blank': 'True'})
        },
        'school.tbhocky': {
            'Meta': {'object_name': 'TBHocKy'},
            'danh_hieu_hk': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hl_hk': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Pupil']"}),
            'tb_hk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'term_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.Term']"})
        },
        'school.tbnam': {
            'Meta': {'object_name': 'TBNam'},
            'danh_hieu_nam': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hk_nam': ('django.db.models.fields.CharField', [], {'default': "u'T'", 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hk_ren_luyen_lai': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'hl_nam': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'hl_thi_lai': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'len_lop': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ren_luyen_lai': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
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
