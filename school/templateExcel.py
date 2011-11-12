from xlwt import easyxf
noneSubject="............................."
e=0.00000001
s1=1000
s2=5000
s3=2000
s4=3000
m1=3000
m2=4000
m3=4000
m4=1400
m5=1400

m6=3000
m7=3000
m8=3500
m9=1000
m10=1400
d1=1400
d2=2000 # kick thuoc cot o trang 31  
d3=6000
d4=1200 # kich thuoc 1 o diem
FIRSTNAME_WIDTH =5000
LASTNAME_WIDTH  =2000
BIRTHDAY_WIDTH  =3000
SIZE_PAGE_WIDTH=36200
SIZE_PAGE_WIDTH1=22000
A4_WIDTH=24500
h1 = easyxf(
    'font:name Arial, bold on,height 1000 ;align: vert centre, horz center')
h2 = easyxf(
    'font:name Times New Roman, bold on,height 1000 ;align: vert centre, horz center')
h3 = easyxf(
    'font:name Times New Roman, bold on,height 400 ;align: vert centre, horz center')
h4 = easyxf(
'font    :name Times New Roman, bold on,height 260 ;align:wrap on, vert centre, horz center;'
'borders : top thin ,right thin, left thin, bottom thin')
h41 = easyxf(
'font    :name Times New Roman, bold on,height 260 ;align:wrap on, horz left;'
'borders : top thin ,right thin, left thin, bottom thin')
h40 = easyxf(
'font    :name Times New Roman, bold on,height 260 ;align:wrap on, vert centre, horz center;')

h5 = easyxf(
'font:name Times New Roman ,height 240 ;align:wrap on, vert centre, horz center;'
'borders: top thin,right thin,left thin,bottom thin')
h6 = easyxf(
'font:name Times New Roman ,height 240 ;align:wrap on;'
'borders: right thin,left thin,bottom dotted')
h61 = easyxf(
'font:name Times New Roman ,height 240 ;align:horz right;'
'borders: right thin,left thin,bottom dotted')
h7 = easyxf(
'font:name Times New Roman ,height 240 ;align:wrap on;'
'borders: right thin,left thin,bottom thin')
h71 = easyxf(
'font:name Times New Roman ,height 240 ;align:horz right;'
'borders: right thin,left thin,bottom thin')

h72 = easyxf(
'font:name Times New Roman ,height 220 ;align:horz right;'
'borders: right thin,left thin,bottom thin,top thin',
)
h73 = easyxf(
'font:name Times New Roman ,height 220 ;align:horz right;'
'borders: right thin,left thin,bottom thin,top thin',
num_format_str='0.00' )

h8 = easyxf(
'font:name Times New Roman ,height 240 ; align:wrap on,horz left')
h81 = easyxf(                                    
'font:name Times New Roman ,height 240 ; align:wrap on,horz left;'# trang 31
'borders: right thin,left thin')

h82 = easyxf(                                    
'font:name Times New Roman ,height 240 ; align:wrap on,horz left;'# trang 31
'borders: right thin,left thin,bottom thin,top thin')

h8center = easyxf(
'font:name Times New Roman ,height 240 ; align:wrap on,horz center')

h9 = easyxf(
'font:name Times New Roman,bold on ,height 240 ;align:horz centre')# xac nhan
h91 = easyxf(
'font:name Times New Roman,bold on ,height 240 ;align:horz centre;'
'borders: right thin,left thin')
h92 = easyxf(
'font:name Times New Roman,bold on ,height 240 ;align:horz centre;'
'borders: right thin,left thin,bottom thin,top thin')

h10 = easyxf(
'font:name Times New Roman,bold on ,height 200 ;align:wrap on,horz centre,vert centre ;'
'borders: top thin,right thin,left thin,bottom thin')

hh1 = easyxf(
'font:name Times New Roman,italic on ,height 240 ;align:horz centre;'
'borders: right thin,left thin')
 
first_name = easyxf(
'font:name Times New Roman ,height 240 ;'
'borders: right thin,left no_line,bottom dotted')
last_name = easyxf(
'font:name Times New Roman ,height 240 ;'
'borders: right no_line,left thin,bottom dotted')

first_name1 = easyxf(
'font:name Times New Roman ,height 220 ;'
'borders: right thin,left no_line,bottom thin')
last_name1 = easyxf(
'font:name Times New Roman ,height 220 ;'
'borders: right no_line,left thin,bottom thin')
