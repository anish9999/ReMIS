from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from LEC_RMSapp.models import Course, Session_year, Student, Staff,Subject,Staff_Notification
from django.contrib import messages
from LEC_RMSapp.models import CustomUser


@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count  = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count =  Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()




    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
    }


    return render(request,'Hod/home.html',context)


@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id = request.POST.get('id')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        joining_date = request.POST.get('joining_date')
        mobile_number= request.POST.get('mobile_number')

        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_number = request.POST.get('father_number')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_number = request.POST.get('mother_number')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        if CustomUser.objects.filter(email=email).exists():
           messages.warning(request, 'Email Is Already Taken')
           return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request, 'Username Is Already Taken')
           return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id = course_id)
            session_year = Session_year.objects.get(id = session_year_id)

            student = Student(
                admin=user,
                id=id,
                joining_date=joining_date,
                dob=dob,
                mobile_number=mobile_number,
                gender=gender,
                session_year_id=session_year,
                course_id=course,
                father_name=father_name,
                father_occupation=father_occupation,
                father_number=father_number,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                mother_number=mother_number,
                present_address=present_address,
                permanent_address=permanent_address,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + " Is Successfully Added !")
            return redirect('add_student')

    context = {
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'HOd/add_student.html', context)

@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()

    context ={
        'student':student,
    }
    return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_year.objects.all()

    context = {
        'student': student,
        'course': course,
        'session_year':session_year,

    }
    return render(request,'Hod/edit_student.html',context)

@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id = request.POST.get('id')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')

        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_number = request.POST.get('father_number')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_number = request.POST.get('mother_number')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        user = CustomUser.objects.get(id = id)
        user.profile_pic = profile_pic
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = id)
        student.gender = gender
        student.dob = dob
        student.joining_date= joining_date
        student.mobile_number= mobile_number
        student.father_name= father_name
        student.father_occupation= father_occupation
        student.father_number= father_number
        student.mother_name= mother_name
        student.mother_occupation= mother_occupation
        student.mother_number= mother_number
        student.present_address= present_address
        student.permanent_address= permanent_address

        course = Course.objects.get(id = course_id)
        student.course_id = course

        session_year = Session_year.objects.get(id = session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_student')

    return render(request,'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request,'Record Are Successfully Deleted!')
    return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')

        course = Course(
            name= course_name,
        )
        course.save()
        messages.success(request,'Course Are Successfully Created')
        return redirect('add_course')
    return render(request,'Hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course':course,
    }
    return render(request,'Hod/view_course.html',context)

@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id = id)

    context = {
        'course':course,
    }
    return render(request,'Hod/edit_course.html',context)

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')

        course = Course.objects.get(id = course_id)
        course.name = name
        course.save()
        messages.success(request,'Course Are Successfully Updated')
        return redirect('view_course')

    return render(request,'Hod/edit_course.html')

@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request,'Course Are Successfully Deleted')

    return redirect('view_course')

@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id = request.POST.get('id')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        number = request.POST.get('number')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email Is Already Taken!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken!')
            return redirect('add_staff')
        else:
            user = CustomUser(username =username,first_name =first_name,last_name = last_name, email= email, profile_pic=profile_pic, user_type=2)
            user.set_password(password)
            user.save()
            staff = Staff(
                admin=user,
                address=address,
                gender = gender, number=number, dob = dob,
                id = id,
            )
            staff.save()
            messages.success(request,'Staff Are Successfully Added!')
            return redirect('add_staff')

    return render(request,'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff':staff,
    }
    return render(request,'Hod/view_staff.html',context)

@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.get(id = id)

    context = {
        'staff':staff,
    }
    return render(request,'Hod/edit_staff.html',context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        number = request.POST.get('number')
        address = request.POST.get('address')

        user= CustomUser.objects.get(id = staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name= last_name
        user.email= email
        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()
        staff = Staff.objects.get(admin = staff_id)
        staff.gender = gender
        staff.address = address
        staff.dob = dob
        staff.number = number

        staff.save()
        messages.success(request,'Faculty Is Successfully Updated')
        return redirect('view_staff')

    return render(request,'Hod/edit_staff.html')

@login_required(login_url='/')
def DELETE_STAFF(request,admin):
    staff = CustomUser.objects.get(id = admin)
    staff.delete()
    messages.success(request,'Record Are Successfully Deleted ! ')
    return redirect('view_staff')

@login_required(login_url='/')
def ADD_SUBECT(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request,'Subjects Are Successfully Added !')
        return redirect('add_subject')

    context={
        'course':course,
        'staff':staff,
    }
    return render(request,'Hod/add_subject.html',context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()

    context = {
        'subject':subject,
    }
    return render(request,'Hod/view_subject.html',context)

@login_required(login_url='/')
def EDIT_SUBJECT(request, id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all
    staff = Staff.objects.all

    context = {
        'subject':subject,
        'course':course,
        'staff':staff,
    }
    return render(request,'Hod/edit_subject.html',context)


def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(
            id = subject_id,
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request,'Subject Are Successfully Updated !')
        return redirect('view_subject')


def DELETE_SUBJECT(request,id):
    subject = Subject.objects.filter(id=id)
    subject.delete()
    messages.success(request,'Subjects Are Successfully Deleted!')
    return redirect('view_subject')


def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_year(
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Are Successfully Created')
        return redirect('add_session')
    return render(request,'Hod/add_session.html')


def VIEW_SESSION(request):
    session = Session_year.objects.all()


    context = {
        'session':session,
    }
    return render(request,'Hod/view_session.html',context)


def EDIT_SESSION(request,id):
    session = Session_year.objects.filter(id = id)

    context = {
        'session':session,
    }
    return render (request,'Hod/edit_session.html',context)


def UPDATE_SESSION(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')


        session = Session_year(
            id = session_id,
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Are Successfully Updated !')
        return redirect('view_session')


def DELETE_SESSION(request,id):
    session = Session_year.objects.get(id = id)
    session.delete()
    messages.success(request,'Session IS Successfully Deleted !')
    return redirect('view_session')


def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all()



    context = {
        'staff':staff,
        'see_notification': see_notification,

    }
    return render(request,'Hod/staff_notification.html',context)


def SEND_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id= request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request,'Notification Are Successfully Send')
        return redirect('staff_send_notification')


