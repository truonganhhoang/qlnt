# -*- coding: utf-8 -*-

from django.forms.widgets import  DateInput
from school.utils import *
from school.models import *
from app.models import *
from school.widgets import *
import xlrd
    
from django.conf import settings
TEMP_FILE_LOCATION = settings.TEMP_FILE_LOCATION
EXPORTED_FILE_LOCATION = settings.EXPORTED_FILE_LOCATION

class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
    
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ('school_id', 'user_id', 'index')
        widgets = {
            'birthday' : DateInput(attrs = {'class':'datepicker'}),
        }
    def __init__(self,school_id, *args, **kwargs):
        super(TeacherForm,self).__init__(*args, **kwargs)
        school = Organization.objects.get(id = school_id)
        self.fields['team_id'] = forms.ModelChoiceField(queryset= school.team_set.all(), required=False, label=u'Tổ')


class TeacherITForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ('school_id', 'user_id')
        widgets = {
            'birthday' : DateInput(attrs = {'class':'datepicker'}),
        }
    def __init__(self,team_id, *args, **kwargs):
        super(TeacherITForm,self).__init__(*args, **kwargs)
        team = Team.objects.get(id = team_id)
        school = team.school_id
        self.fields['team_id'] = forms.ModelChoiceField(queryset= school.team_set.all(), required=False, label=u'Tổ')
        self.fields['group_id'] = forms.ModelChoiceField(queryset= team.group_set.all(), required=False, label=u'Nhóm')

class TeacherTTCNForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('last_name','first_name','birthday','sex','birth_place','dan_toc','ton_giao','quoc_tich','home_town','major')
        widgets = {
            'birthday' : DateInput(attrs = {'class':'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(TeacherTTCNForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'

class TeacherTTLLForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('current_address','phone','email','sms_phone')

    def __init__(self, *args, **kwargs):
        super(TeacherTTLLForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'

class TeacherTTCBForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('cmt','ngay_cap','noi_cap','ngay_vao_doan','ngay_vao_dang','muc_luong','hs_luong','bhxh')
        widgets = {
            'ngay_vao_doan' : DateInput(attrs= {'class': 'datepicker'}),
            'ngay_vao_dang' : DateInput(attrs= {'class': 'datepicker'})
        }

    def __init__(self, *args, **kwargs):
        super(TeacherTTCBForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'
            
class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        exclude = ('school_id','user_id','index')
        widgets = {
            'birthday' : DateInput(attrs = {'class':'datepicker'}),
            'school_join_date' : DateInput(attrs = {'class':'datepicker'}),
            'ngay_vao_doan': DateInput(attrs = {'class':'datepicker'}),
            'ngay_vao_doi': DateInput(attrs = {'class':'datepicker'}),
            'ngay_vao_dang': DateInput(attrs = {'class':'datepicker'}),
            'father_birthday': DateInput(attrs = {'class':'datepicker'}),
            'mother_birthday': DateInput(attrs = {'class':'datepicker'}),
        }
    def __init__(self, school_id, *args, **kwargs):
        super(PupilForm, self).__init__(*args, **kwargs)
        school = Organization.objects.get(id = school_id)
        year_id = school.year_set.latest('time').id
        self.fields['start_year_id'] = forms.ModelChoiceField(queryset = StartYear.objects.filter(school_id = school_id),label='Khóa')
        self.fields['class_id'] = forms.ModelChoiceField(queryset = Class.objects.filter(year_id = year_id),label='Lớp')

class ThongTinCaNhanForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ('last_name','first_name','birthday','sex','class_id','start_year_id','birth_place','dan_toc','ton_giao','uu_tien','quoc_tich','home_town','ban_dk','school_join_date','school_join_mark')
        widgets = {
            'birthday' : DateInput(attrs = {'class':'datepicker'}),
            'school_join_date' : DateInput(attrs = {'class':'datepicker'})
        }
        
    def __init__(self, school_id, *args, **kwargs):
        super(ThongTinCaNhanForm, self).__init__(*args, **kwargs)
        school = Organization.objects.get(id = school_id)
        year_id = school.year_set.latest('time').id
        self.fields['start_year_id'] = forms.ModelChoiceField(queryset = StartYear.objects.filter(school_id = school_id),label='Khóa')
        self.fields['class_id'] = forms.ModelChoiceField(queryset = Class.objects.filter(year_id = year_id),label='Lớp')
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'

class ThongTinLienLacForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ('current_address','phone','father_phone','mother_phone','sms_phone','email')
    def __init__(self, *args, **kwargs):
        super(ThongTinLienLacForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'

class ThongTinGiaDinhForm(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = ('father_name','father_birthday','father_job','mother_name','mother_birthday','mother_job')
        widgets = {
            'father_birthday': DateInput(attrs = {'class':'datepicker'}),
            'mother_birthday': DateInput(attrs = {'class':'datepicker'}),
        }
    def __init__(self, *args, **kwargs):
        super(ThongTinGiaDinhForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'
        
class ThongTinDoanDoiForm(forms.ModelForm):
    def __init__(self, student_id, *args, **kw):
        student = Pupil.objects.get(id = student_id)
        def validate_ttdd_date(value):
            if value < student.birthday+timedelta(days=2190) or value > date.today():
                raise ValidationError(u'Ngày nằm ngoài khoảng cho phép')
        super(ThongTinDoanDoiForm, self).__init__(*args, **kw)
        self.fields.keyOrder = ['doi','ngay_vao_doi','doan','ngay_vao_doan','dang','ngay_vao_dang']
        self.fields['ngay_vao_doi'] = forms.DateField(required=False, label=u'Ngày vào đội', validators=[validate_ttdd_date], widget=forms.DateInput(attrs={'class':'datepicker'}))
        self.fields['ngay_vao_doan'] = forms.DateField(required=False, label=u'Ngày vào đoàn', validators=[validate_ttdd_date], widget=forms.DateInput(attrs={'class':'datepicker'}))
        self.fields['ngay_vao_dang'] = forms.DateField(required=False, label=u'Ngày vào đảng', validators=[validate_ttdd_date], widget=forms.DateInput(attrs={'class':'datepicker'}))
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = 'disabled'
        
    class Meta:
        model = Pupil
        fields = {'doi','ngay_vao_doi','doan','ngay_vao_doan','dang','ngay_vao_dang'}

        
class SchoolForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SchoolForm, self).__init__(*args, **kwargs)
        if get_permission(self.request) in [u'HIEU_TRUONG', u'HIEU_PHO']:
            self.fields['name'] = forms.CharField(label=u'Tên trường:', max_length = 100 ) #tên đơn vị. tổ chức
            school = get_school(self.request)
            self.fields['school_level'] = forms.ChoiceField(label=u"Cấp:", choices = KHOI_CHOICES)
            if school.status in [1,2]:
                self.fields['school_level'].widget.attrs['disabled'] = 'disabled'
                self.fields['school_level'].required = False
            self.fields['address'] = forms.CharField(label=u"Địa chỉ:", max_length = 255, required = False) #
            self.fields['phone'] = forms.CharField(label="Điện thoại:", max_length = 20, validators=[validate_phone], required = False)
            self.fields['email'] = forms.EmailField(max_length = 50,  required = False) 
    def save_to_model(self):
        try:
            school = get_school(self.request)
            school.name = self.cleaned_data['name']
            if self.cleaned_data['school_level']:
                school.school_level = self.cleaned_data['school_level']
            school.address = self.cleaned_data['address']
            school.phone = self.cleaned_data['phone']
            school.email = self.cleaned_data['email']
            school.save()
        except Exception as e:
            print e

class SettingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SettingForm, self).__init__(*args, **kwargs)
        self.fields['lock_time'] = forms.IntegerField(label=u"Thời gian khóa điểm(Giờ):", required = True) #
        self.fields['class_labels'] = forms.CharField(label=u"Danh sách lớp học:", max_length = 512,
                                                      validators=[validate_class_label],
                                                      required = False)
        
    def save_to_model(self):
        try:
            school = get_school(self.request)
            if self.cleaned_data['lock_time'] >= 0:
                school.save_settings('lock_time', self.cleaned_data['lock_time'])
            else:
                raise Exception('LockTimeValueError')
            if self.cleaned_data['class_labels']:
                labels = self.cleaned_data['class_labels']
                labels = labels.split(',')
                result = u'['
                for label in labels:
                    if label.strip():
                        result += u"u'%s'," % label.strip()
                result = result[:-1]
                result += u']'
                print 'result', result
                school.save_settings('class_labels', unicode(result) )

        except Exception as e:
            print e



class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        
    def __init__(self, school_id, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.fields['teacher_id'] = forms.ModelChoiceField(required = False, queryset=Teacher.objects.filter(school_id = school_id))
        self.fields['year_id'] = forms.ModelChoiceField(queryset=Year.objects.filter(school_id = school_id),initial = Year.objects.filter(school_id = school_id).latest('time'))
        self.fields['block_id'] = forms.ModelChoiceField(queryset=Block.objects.filter(school_id = school_id))

class TBNamForm(forms.ModelForm):
    class Meta:
        model = TBNam
        exclude = {'number_subject', 'number_finish', 'tong_so_ngay_nghi', 'danh_hieu_nam', 'len_lop', 'thi_lai', 'tb_thi_lai', 'hl_thi_lai'}

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = {'index','class_id'}
        
    def __init__(self, school_id, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        self.fields['teacher_id'] = forms.ModelChoiceField(required = False, queryset = Teacher.objects.filter(school_id = school_id), label=u'Giáo viên giảng dạy')

class KhenThuongForm(forms.ModelForm):
    class Meta:
        model = KhenThuong
        exclude = ('student_id', 'term_id')
        widgets = {
            'noi_dung': forms.Textarea(attrs = {'cols': 50, 'rows': 10}),
        }

    def __init__(self, student_id, *args, **kw):
        student = Pupil.objects.get(id = student_id)
        def validate_ktkl_date(value):
            if value < student.school_join_date or value > date.today():
                raise ValidationError(u'Ngày nằm ngoài khoảng cho phép')
        super(KhenThuongForm, self).__init__(*args, **kw)
        self.fields['time'] = forms.DateField(required=False, label=u'Ngày', validators=[validate_ktkl_date], widget=forms.DateInput(attrs={'class':'datepicker'}))

class KiLuatForm(forms.ModelForm):        
    class Meta:
        model = KiLuat
        exclude = ('student_id', 'term_id')
        field = ('time', 'noi_dung')
        widgets = {
            'time' : DateInput(attrs = {'class':'datepicker'}),
            'noi_dung': forms.Textarea(attrs = {'cols': 50, 'rows': 10}),
        }

    def __init__(self, student_id, *args, **kw):
        student = Pupil.objects.get(id = student_id)
        def validate_ktkl_date(value):
            if value < student.school_join_date or value > date.today():
                raise ValidationError(u'Ngày nằm ngoài khoảng cho phép')
        super(KiLuatForm, self).__init__(*args, **kw)
        self.fields['time'] = forms.DateField(required=False, label=u'Ngày', validators=[validate_ktkl_date], widget=forms.DateInput(attrs={'class':'datepicker'}))

class TeamForm(forms.ModelForm):
    class Meta:
            model = Team
        
class GroupForm(forms.ModelForm):
    class Meta:
            model = Group

class HanhKiemForm(forms.ModelForm):
    class Meta:
        model = HanhKiem
    
class DiemDanhForm(forms.ModelForm):
    class Meta:
        model = DiemDanh
        field = ('time')
        widgets = {
            'time' : DateInput(attrs = {'class':'datepicker'}),
        }

class TKDiemDanhForm(forms.ModelForm):
    class Meta:
        model = TKDiemDanh

class TermForm(forms.ModelForm):
    class Meta:
        model = Term

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        
class DateForm(forms.Form):
    date = forms.DateField(label = '',
                           widget = DateInput(attrs = {'class':'datepicker'}),
                           initial = datetime.date.today())

        
class DateAndClassForm(forms.Form):
    class_id = forms.ModelChoiceField(queryset = Class)
    date = forms.DateField(label = u'ngày',
                           widget = DateInput(attrs = {'class':'datepicker'}),
                           initial= datetime.date.today)
    
    def __init__(self, year_id, *args, **kwargs):
        super(DateAndClassForm, self).__init__(*args, **kwargs)
        self.fields['class_id'] = forms.ModelChoiceField(queryset = Class.objects.filter(year_id = year_id),
                                                         label = u'lớp')
    
class UploadImportFileForm(forms.Form):
    def __init__(self, * args, ** kwargs):
        class_list = kwargs.pop('class_list')
        super(UploadImportFileForm, self).__init__(*args, ** kwargs)
        self.fields['the_class'] = forms.ChoiceField(label=u'Nhập vào lớp:', choices=class_list, required=False)
        self.fields['import_file'] = forms.FileField(label=u'Chọn file Excel:')
        
class ManualAddingForm(forms.Form):
    def __init__(self, * args, ** kwargs):
        class_list = kwargs.pop('class_list')
        super(ManualAddingForm, self).__init__(*args, ** kwargs)
        self.fields['the_class'] = forms.ChoiceField(label=u'Nhập vào lớp:', choices=class_list, required=False)
        
class ClassifyForm(forms.Form):
    def __init__(self, * args, ** kwargs):
        students = kwargs.pop('student_list')
        classes = kwargs.pop('class_list')
        super(ClassifyForm, self).__init__(*args, ** kwargs)
        for student in students:
            label = ' '.join([student.last_name, student.first_name])
            label += u'[' + str(student.birthday.day ) \
                          + '-' + str(student.birthday.month) \
                          + '-' + str(student.birthday.year)+']'
            self.fields[str(student.id)] = forms.ChoiceField(label = label, choices=classes, required=False)
CONTENT_TYPES = ['application/vnd.ms-excel']            

class uploadFileExcel(forms.Form):
    file  = forms.FileField(label=u'Chọn file Excel:', widget=forms.FileInput())
    
    def is_valid(self):
        file = self.cleaned_data['file']
        if not file.content_type in CONTENT_TYPES:
            os.remove(filepath)
            raise forms.ValidationError(u'Bạn chỉ được phép tải lên file Excel.')
        elif not os.path.getsize(filepath):
            raise forms.ValidationError(u'File của bạn rỗng.')
        elif not xlrd.open_workbook(filepath).sheet_by_index(0).nrows:
            raise forms.ValidationError(u'File của bạn rỗng.')
        else:
            return super(uploadFileExcel, self).is_valid()
    
            
class smsFromExcelForm(forms.Form):
    file  = forms.Field(label="Chọn file Excel:",
                        error_messages={'required': 'Bạn chưa chọn file nào để tải lên.'},
                        widget=forms.FileInput())
    
    def clean_file(self):
        file = self.cleaned_data['file']
        save_file(file)            
        filepath = os.path.join(TEMP_FILE_LOCATION, 'sms_input.xls')
        
        if not file.content_type in CONTENT_TYPES:
            os.remove(filepath)
            raise forms.ValidationError(u'Bạn chỉ được phép tải lên file Excel.')
        elif not os.path.getsize(filepath):
            raise forms.ValidationError(u'Hãy tải lên một file Excel đúng. File của bạn hiện đang trống.')
        elif not xlrd.open_workbook(filepath).sheet_by_index(0).nrows:
            raise forms.ValidationError(u'Hãy tải lên một file Excel đúng. File của bạn hiện đang trống.')
#        if content._size > settings.MAX_UPLOAD_SIZE:
#            raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            return file     

class UsernameChangeForm(forms.Form):
    new_username = forms.RegexField(label=u"Tài khoản mới", max_length=30, regex=r'^[\w.@+-]+$')
    password = forms.CharField(label=u'Mật khẩu', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UsernameChangeForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['new_username', 'password']
        
    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(u"Mật khẩu không đúng hãy nhập lại")
        return password
    
    def clean_new_username(self):
        new_username = self.cleaned_data["new_username"]
        try:
            User.objects.get(username=new_username)
        except User.DoesNotExist:
            return new_username
        raise forms.ValidationError(u"Tên đăng nhập này đã tồn tại")

    def save(self,commit=True):
        self.user.username = self.cleaned_data["new_username"]
        self.user.userprofile.username_change = 1
        if commit:
            self.user.save()
            self.user.userprofile.save()
        return self.user