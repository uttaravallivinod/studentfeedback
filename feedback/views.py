from django.shortcuts import render,redirect
from feedback.models import College,Course,Student,Faculty,Teach,Feed,Ef
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as log
from django.contrib.auth.decorators import login_required
import pandas as pd
import xlrd
from random import randint
from django.core.mail import send_mail
from django.urls import reverse
import datetime
# Create your views here.


def home(request):
    return render(request,'base.html')


def login(request):
    if request.method=='POST':
        name=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=name,password=password)
        if user is not None:
            log(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Details Please Login Again')
            return redirect('/login')
    else:
        return render(request,'login.html')


@login_required
def profile(request):
    user=request.user
    l=College.objects.filter(user=user)
    if not l:
        return redirect('/extra')
    c=Course.objects.filter(college_n=request.user.college)
    return render(request,'profile.html',{'co':c,'c':l[0].name})


@login_required
def extra(request):
    if request.method=='POST':
        user=request.user
        college=request.POST['college']
        place=request.POST['place']
        l=College.objects.create(user=user,name=college,place=place)
        l.save()
        return redirect('/')
    else:
        return render(request,'extra.html')


def register(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['psw']
        if fname.isalpha() and lname.isalpha():
            if User.objects.filter(username=username).exists():
                messages.info(request,"User name is already exists take another one")
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email is already exists take another one")
                return redirect('/register')
            else:
                user=User.objects.create_user(username=username,email=email,first_name=fname,last_name=lname,password=password)
                user.save()
                return redirect('/login')
        else:
            messages.info(request,"correct your name")
            return redirect('/register')
    else:
        return render(request,'register.html')


@login_required
def addcourse(request):
    if request.method=='POST':
        college=request.user.college
        name=request.POST['cname']
        years=request.POST['yr']
        subjects=request.POST['sub']
        try:
            c=Course.objects.create(college_n=college,name=name.upper(),year=years,subjects=subjects)
            coll=College.objects.filter(id=request.user.college.id)
            coll.update(valid=False)
            c.save()
            messages.info(request,'1 Course Added')
            return redirect('/profile')
        except:
            messages.info(request,'Course Already exist or Something Went Wrong Please Check')
            return redirect('/profile')
    else:
        return redirect('/')


@login_required
def student(request):
    if request.method=='POST':
        college=request.user.college
        name=request.POST['name']
        number=request.POST['reg']
        phone=request.POST['phone']
        course=request.POST['course']
        email=request.POST['email']
        co=Course.objects.get(id=course)
        try:
            s=Student.objects.create(email=email,college_n=college,name=name,number=number,phone=phone,course_n=co)
            s.save()
            messages.info(request,'1 Student added')
            return redirect('/student')
        except:
            messages.info(request,'student alredy exist')
            return redirect('/student')
    else:
        cc=Course.objects.filter(college_n=request.user.college)
        s=Student.objects.filter(college_n=request.user.college).count()
        return render(request,'student.html',{'cc':cc,'s':s})


@login_required
def upload(request):
    if request.method=='POST':
        college=request.user.college
        dt=request.FILES['tfile']
        if str(dt).endswith('.csv'):
            df=pd.read_csv(dt)
        elif str(dt).endswith('.xlsx'):
            df=pd.read_excel(dt)
        else:
            messages.info(request,'you can only able to upload ".csv" or ".xlsx" files')
            return redirect('/student')
        d=df.to_dict(orient='record')
        col_values=set(list(d[0].keys()))
        if set(['name','phone','year','number','course','email']) <= col_values:
            cc=0
            for i in d:
                name=i.get('name')
                number=i.get('number')
                phone=i.get('phone')
                course=i.get('course')
                email=i.get('email')
                y=i.get('year')
                try:
                    co=Course.objects.filter(college_n=request.user.college,name=course.upper(),year=y)
                except:
                    continue
                try:
                    s=Student.objects.create(email=email,college_n=college,name=name,number=number,phone=phone,course_n=co[0])
                    s.save()
                    cc+=1
                except:
                    continue
            messages.info(request,str(cc)+' Student records uploaded')
            return redirect('/student')
        else:
            messages.info(request,'column names are not valid please check')
            return redirect('/student')




@login_required
def uploadfaculty(request):
    if request.method=='POST':
        college=request.user.college
        dt=request.FILES['tfile']
        if str(dt).endswith('.csv'):
            df=pd.read_csv(dt)
        elif str(dt).endswith('.xlsx'):
            df=pd.read_excel(dt)
        else:
            messages.info(request,'you can only able to upload ".csv" or ".xlsx" files')
            return redirect('/faculty')
        d=df.to_dict(orient='record')
        col_values=set(list(d[0].keys()))
        if set(['faculty_name','email','emp_id']) <= col_values:
            ccc=0
            for i in d:
                name=i.get('faculty_name')
                email=i.get('email')
                empid=i.get('emp_id')
                try:
                    s=Faculty.objects.create(college_n=college,name=name,email=email,empid=empid)
                    s.save()
                    ccc+=1
                except:
                    continue
            messages.info(request,str(ccc)+' Faculty Succussfully uploaded.')
            return redirect('/faculty')
        else:
            messages.info(request," Invalid Column names Please check the schema of  "+str(dt)+'  ^.')
            return redirect('/faculty')



@login_required
def faculty(request):
    if request.method=='POST':
        college=request.user.college
        name=request.POST['name']
        email=request.POST['email']
        empid=request.POST['empid']
        try:
            s=Faculty.objects.create(college_n=college,name=name,email=email,empid=empid)
            s.save()
            messages.info(request,'One Faculty Uploaded')
            return redirect('/faculty')
        except:
            messages.info(request,'Faculty Already exist or Something Went Wrong Please Check')
            return redirect('/faculty')
    else:
        cc=Faculty.objects.filter(college_n=request.user.college)
        return render(request,'faculty.html',{'cc':cc})




@login_required
def teach(request):
    if request.method=='POST':
        ii=1
        for i in request.POST:
            if ii==1:
                ii=0
                continue
            l=i.split('/')
            course=l[0]
            subject=l[1]
            faculty=request.POST[i]
            c=Course.objects.get(id=course)
            f=Faculty.objects.get(id=faculty)
            try:
                t=Teach.objects.create(college_n=request.user.college,course_n=c,faculty_n=f,subject=subject)
                t.save()
            except:
                continue
        messages.info(request,'Succussfully data uploaded')
        return redirect('/teach')
    else:
        cc=list(Course.objects.filter(college_n=request.user.college).values())
        tt=Teach.objects.filter(college_n=request.user.college).values('course_n')
        t=[]
        c=[]
        for i in tt:
            t.append(i['course_n'])
        for i in cc:
            if i['id'] not in t:
                c.append(i)
        for i in c:
            i['subjects']=i['subjects'].split('/')
        f=Faculty.objects.filter(college_n=request.user.college).values()
        if f:
            if c:
                return render(request,'teach.html',{'course':c,'f':f})
            else:
                tt=Teach.objects.filter(college_n=request.user.college,faculty_n__isnull=True)
                if tt:
                    return redirect('/updateteach')
                else:
                    coll=College.objects.filter(id=request.user.college.id)
                    coll.update(valid=True)
                    messages.info(request,'you can send link now')
                    return redirect('/link')
        else:
            messages.info(request,'you have to add faculty')
            return redirect('/faculty')




@login_required
def link(request):
    return render(request,'link.html')




def sauth(request):
    if request.method=='POST':
        num=request.POST['reg']
        college=request.POST['college']
        l=[]
        if Student.objects.filter(number=num,college_n_id=college).exists():
            s=Student.objects.get(number=num)
            otp=randint(100000,999999)
            request.session['college']=College.objects.get(id=request.POST['college']).slug
            request.session['otp']=otp
            request.session['student']=s.slug
            send_mail('FEEDBACK OTP','Secure OTP'+str(otp),'studentfeedbackc@gmail.com',[s.email],fail_silently=False)
            return redirect('/otpvalid')
        else:
            return HttpResponse('Invalid details <a href="/sauth">go back</a>')
    else:
        c=College.objects.all()
        return render(request,'slogin.html',{'c':c})




def feed(request,stslug,clslug):
    if Student.objects.get(college_n=College.objects.get(slug=clslug),slug=stslug).valid==True:
        dat=datetime.datetime.now()
        try:
            s=Student.objects.get(college_n=College.objects.get(slug=clslug),slug=stslug)
            tt=Teach.objects.filter(college_n=College.objects.get(slug=clslug),course_n=s.course_n)
        except:
            return HttpResponse('Invalid details')

        try:
            f=Feed.objects.filter(college_n=College.objects.get(slug=clslug),student_n=s,month=str(dat.month),year=dat.year)
            if f:
                return HttpResponse('You already submitted')
        except:
            return HttpResponse('Invalid details')
        if request.method=='POST':
            for i in tt:
                ct=request.POST[i.subject+'/ct']
                b=request.POST[i.subject+'/b']
                sc=request.POST[i.subject+'/sc']
                ec=request.POST[i.subject+'/ec']
                t=request.POST[i.subject+'/t']

                try:
                    f=Feed.objects.create(college_n=s.college_n,student_n=s,faculty_n=i.faculty_n,subject=i.subject,ct=ct,b=b,sc=sc,ec=ec,t=t,month=str(dat.month),year=dat.year)
                    f.save()
                    sm=Student.objects.filter(college_n=College.objects.get(slug=clslug),slug=stslug)
                    sm.update(valid=False)

                except:
                    return HttpResponse('Already Recorded')
            ef=Ef.objects.create(college_n=s.college_n,student_n=s,extra_feed=request.POST['ef'])
            return HttpResponse('Thank you for your feedback')
        else:
            return render(request,'feed.html',{'tt':tt})
    else:
        messages.info(request,'You are not verified yet')
        return redirect('/sauth')




def otpvalid(request):
    if request.method=='POST':
        num=request.POST['otp']
        if num==str(request.session['otp']):
            s=Student.objects.filter(slug=request.session['student'])
            s.update(valid=True)
            return redirect('/feed/'+str(request.session['student'])+'/'+str(request.session['college']))
        else:
            messages.info(request,"Entered OTP is Incorrect")
            return redirect('/otpvalid')
    else:
        return render(request,'otp.html')




@login_required
def uploadcourse(request):
    if request.method=='POST':
        college=request.user.college
        dt=request.FILES['tfile']
        if str(dt).endswith('.csv'):
            df=pd.read_csv(dt)
        elif str(dt).endswith('.xlsx'):
            df=pd.read_excel(dt)
        else:
            messages.info(request,'you can only able to upload ".csv" or ".xlsx" files')
            return redirect('/profile')
        d=df.to_dict(orient='record')
        col_values=set(list(d[0].keys()))
        if set(['course_name','course_year','course_subjects']) <= col_values:
            countt=0
            for i in d:
                name=i.get('course_name')
                year=i.get('course_year')
                subjects=i.get('course_subjects')
                try:
                    s=Course.objects.create(college_n=college,name=name.upper(),year=year,subjects=subjects)
                    s.save()
                    countt+=1
                except:
                    continue
            messages.info(request,str(countt)+' Courses Succussfully uploaded')
            return redirect('/profile')
        else:
            messages.info(request,"Please check the schema of  "+str(dt)+'  ^.')
            return redirect('/profile')



@login_required
def cdelete(request,slugg):
    c=Course.objects.get(slug=slugg)
    name=c.name
    c.delete()
    messages.info(request,name+' Course Deleted')
    return redirect('/profile')


@login_required
def fdelete(request,slugg):
    c=Faculty.objects.get(slug=slugg)
    name=c.name
    c.delete()
    messages.info(request,name+' Faculty Deleted')
    return redirect('/faculty')



@login_required
def updateteach(request):
    tt=Teach.objects.filter(college_n=request.user.college,faculty_n__isnull=True)
    f=Faculty.objects.filter(college_n=request.user.college).values()
    if request.method=='POST':
        ii=1
        for i in request.POST:
            if ii==1:
                ii=0
                continue
            faculty=request.POST[i]
            f=Faculty.objects.get(id=faculty)
            t=Teach.objects.filter(id=i)
            t.update(faculty_n=f)
        return redirect('/teach')
    else:
        if tt:
            return render(request,'upteach.html',{'tt':tt,'f':f})
        else:
            return redirect('/teach')



@login_required
def cupdate(request,slugg):
    c=Course.objects.filter(slug=slugg)
    if request.method=='POST':
        sname=request.POST['snames']
        try:
            c.update(subjects=sname)
            messages.info(request,c[0].name+' Course Updated')
            return redirect('/profile')
        except:
            messages.info(request,'Something went wrong')
            return redirect('/faculty')
    else:
        return render(request,'cupdate.html',{'c':c[0]})



@login_required
def fupdate(request,slugg):
    f=Faculty.objects.filter(slug=slugg)
    if request.method=='POST':
        fname=request.POST['fname']
        email=request.POST['email']
        try:
            f.update(name=fname,email=email)
            messages.info(request,'One Faculty upadated')
            return redirect('/faculty')
        except:
            messages.info(request,'Something went wrong')
            return redirect('/faculty')
    else:
        return render(request,'fupdate.html',{'f':f[0]})



@login_required
def anal(request):
    try:
        ff=Feed.objects.filter(college_n=request.user.college)
    except:
        return redirect('/extra')

    ts=Student.objects.filter(college_n=request.user.college).count()
    l=[j.student_n_id for j in ff]
    gs=len(set(l))
    ct=[]
    ec=[]
    sc=[]
    b=[]
    t=[]
    for i in ff:
        ct.append(i.ct)
        ec.append(i.ec)
        sc.append(i.sc)
        b.append(i.b)
        t.append(i.t)
    z=ct+ec+sc+b+t
    gr=z.count(10)+z.count(7)
    br=z.count(3)+z.count(1)
    fdict={'Class Taking':{},'Exams Conducting':{},'Behaviour':{},'Teaching':{},'Syllabus Completion':{}}
    fac=Faculty.objects.filter(college_n=request.user.college).values()
    for i in ff:
        fdict['Class Taking'][i.faculty_n.name]=fdict['Class Taking'].get(i.faculty_n.name,'')+' '+str(i.ct)
        fdict['Teaching'][i.faculty_n.name]=fdict['Teaching'].get(i.faculty_n.name,'')+' '+str(i.t)
        fdict['Behaviour'][i.faculty_n.name]=fdict['Behaviour'].get(i.faculty_n.name,'')+' '+str(i.b)
        fdict['Exams Conducting'][i.faculty_n.name]=fdict['Exams Conducting'].get(i.faculty_n.name,'')+' '+str(i.ec)
        fdict['Syllabus Completion'][i.faculty_n.name]=fdict['Syllabus Completion'].get(i.faculty_n.name,'')+' '+str(i.sc)
    for i in fdict:
        for j in fdict[i]:
            fdict[i][j]=list(map(int,fdict[i][j].split()))
            fdict[i][j]=round((sum(fdict[i][j])/(len(fdict[i][j])*10))*100)
    tdict={}
    for i in ff:
        tdict[i.faculty_n.name]=tdict.get(i.faculty_n.name,'')+' '+str(i.ct)+' '+str(i.sc)+' '+str(i.b)+' '+str(i.t)+' '+str(i.ec)
    for i in tdict:
        tdict[i]=list(map(int,tdict[i].split()))
        tdict[i]=((sum(tdict[i])/(len(tdict[i])*10)))*100
    mi=0
    tdictt={}
    tdd={k: v for k, v in sorted(tdict.items(),reverse=True, key=lambda item: item[1])}
    for i,k in tdd.items():
        if mi>4:
            break
        mi+=1
        tdictt[i]=k
    ef=Ef.objects.filter(extra_feed__isnull=False,college_n=request.user.college)
    fff=Faculty.objects.filter(college_n=request.user.college)




    d={'ts':ts,'gs':gs,'gr':gr,'br':br,'fdict':fdict,'tdict':tdictt,'tdd':tdd,'ef':ef,'fff':fff}

    return render(request,'anal/dashboard.html',d)



@login_required(login_url='/login/')
def fanal(request,slugg):
    ff=Feed.objects.filter(college_n=request.user.college,faculty_n=Faculty.objects.get(slug=slugg))
    if not ff:
        return redirect('/dashboard')
    ts=Student.objects.filter(college_n=request.user.college).count()
    l=[j.student_n_id for j in ff]
    gs=len(set(l))
    ct=[]
    ec=[]
    sc=[]
    b=[]
    t=[]
    for i in ff:
        ct.append(i.ct)
        ec.append(i.ec)
        sc.append(i.sc)
        b.append(i.b)
        t.append(i.t)
    z=ct+ec+sc+b+t
    gr=z.count(10)+z.count(7)
    br=z.count(3)+z.count(1)
    ef=Ef.objects.filter(extra_feed__isnull=False,college_n=request.user.college)
    fff=Faculty.objects.filter(college_n=request.user.college)
    gp={}
    for i in ff:
        gp[i.student_n.course_n.name+' ('+i.subject+')']=gp.get(i.student_n.course_n.name+' '+i.subject,'')+' '+str(i.ct)+' '+str(i.sc)+' '+str(i.b)+' '+str(i.t)+' '+str(i.ec)
    for i in gp:
        gp[i]=list(map(int,gp[i].split()))
        gp[i]=((sum(gp[i])/(len(gp[i])*10)))*100
    d={'ts':ts,'gs':gs,'gr':gr,'br':br,'fff':fff,'z':z,'faculty':ff[0].faculty_n.name,'ef':ef,'gp':gp}
    return render(request,'anal/facanal.html',d)



@login_required
def pp(request):
    if request.method=='POST':
        cp=request.POST['cp']
        np=request.POST['np']

        us=User.objects.get(id=request.user.id)
        if us.check_password(cp):
            us.set_password(np)
            us.save()
            messages.info(request,'Succussfully Changed')
            return redirect('/pp')
        else:
            messages.info(request,'You entered password is incorrect')
            return redirect('/pp')
    return render(request,'pp.html')





@login_required
def alert(request):
    if Teach.objects.filter(college_n=request.user.college).exists():
        return redirect('/teach')
    else:
        if Course.objects.filter(college_n=request.user.college).exists():
            if Faculty.objects.filter(college_n=request.user.college).exists():
                if Student.objects.filter(college_n=request.user.college).exists():
                    return redirect('/teach')
                else:
                    messages.info(request,'You have to Add Students')
                    return redirect('/student')
            else:
                messages.info(request,'You have to add Facultys')
                return redirect('/faculty')

        else:
            messages.info(request,'You have to add Courses')
            return redirect('/profile')




@login_required
def sms(request):
    if College.objects.get(id=request.user.college.id).valid==True:
        s=Student.objects.filter(college_n=request.user.college)
        college=request.user.college.name
        co=0
        for i in s:
            try:
                co+=1
                send_mail(college,'This mail from '+college+' to Submit Feed back of your faculty. Your number ('+i.number+').Here is the link http://127.0.0.1:8000/sauth','studentfeedbackc@gmail.com',[i.email],fail_silently=False)
            except:
                continue
        messages.info(request,str(co)+' mails are Succussfully sent')
        return redirect('/link')


    else:
        return redirect('/alert')
