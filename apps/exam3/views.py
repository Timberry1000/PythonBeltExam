from django.shortcuts import render,redirect,HttpResponse
from .models import Reg,Job
import bcrypt
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'exam3/index.html')

def reg(request):
    results = Reg.objects.validate(request.POST)
    print(results)
    if not results[0]:
        for error_message in results[1]:
            messages.add_message(request,messages.ERROR, error_message)
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = Reg.objects.create(firstname = request.POST['firstname'], lastname=request.POST['lastname'],email=request.POST['email'],pw_hash=hash1)
        request.session['Reg_id'] = user.id
        request.session['firstname'] = user.firstname
        request.session['lastname'] = user.lastname
        request.session['email'] = user.email
        print(hash1)
        return redirect('/dash')
    return redirect('/')

""" Checks if login attempt is valid """
def login(request):
    success, errors = Reg.objects.login(request.POST)    
    if not success:
        for error_message in errors:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect('/')    
    else:
        user = Reg.objects.get(email=request.POST['email'])
        print(user.pw_hash)
        if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
            request.session['Reg_id'] = user.id
            request.session['firstname'] = user.firstname
            request.session['lastname'] = user.lastname
            request.session['email'] = user.email
            user.save()
            
            return redirect('/dash')
        else:
            return redirect("/")
"""This will render all the jobs"""
def dash(request):
    if 'Reg_id' not in request.session:
        return redirect('/')

    jobs = Job.objects.all().distinct().exclude(joins__id =request.session['Reg_id'])
    my_jobs = Job.objects.all().distinct().filter(jobs = request.session["Reg_id"]) 
    all_jobs = Job.objects.all().exclude(jobs = request.session["Reg_id"]) & Job.objects.all().exclude(joins__id = request.session['Reg_id'])
    joined_jobs = Job.objects.distinct().filter(joins__id = request.session['Reg_id'])
    

    context = {
        'my_jobs': my_jobs,
        'all_jobs': all_jobs,
        'joined': joined_jobs,
        'jobs': jobs
    }
    return render(request, 'exam3/dash.html', context)



""" This will render the add page only """
def add(request):
    return render(request, 'exam3/addjob.html')



"""This will actually add the job or bring errors to the page """
def addjob(request):
    success, errors = Job.objects.valid(request.POST)
    if not success:
        for error_message in errors:
            messages.add_message(request, messages.ERROR, error_message)
            return redirect('/addjob')
    else:
        Job.objects.create(title = request.POST['title'], desc = request.POST['desc'], location = request.POST['location'], jobs =Reg.objects.get(id = request.session['Reg_id']))
    return redirect('/dash')


"""This will render the view page """
def view(request,id):
    my_job = Job.objects.get(id= id)
    
    context = {
        'my_job': my_job
    }
    return render(request, 'exam3/view.html',context)


"""This will render the edit page"""
def edit(request,id):
    my_job = Job.objects.get(id= id)
    context = {
        'my_job' : my_job
    }
    return render(request, 'exam3/edit.html', context)

def editlogic(request,id):
    success, errors = Job.objects.valid(request.POST)
    if not success:
        for error_message in errors:
            messages.add_message(request, messages.ERROR, error_message)
            return redirect('/edit/'+ id)
    else:
        job = Job.objects.get(id = id)
        job.title = request.POST['title']
        job.desc = request.POST['desc']
        job.location = request.POST['location']
        job.save()
    return redirect('/dash')

"""This will cancel/delete the selected job """
def cancel(request,id):
    Job.objects.get(id=id).delete()
    return redirect('/dash')


"""This will delete the selected job from a table and DB """
def done(request,id):
    Job.objects.get(id=id).delete()
    return redirect('/dash')


"""This will add a job to your list"""
def addingjob(request,id):
    this_joiner = Reg.objects.get(id = request.session["Reg_id"])
    this_job = Job.objects.get(id =id)
    this_job.joins.add(this_joiner)
    return redirect('/dash')
    

def logout(request):
    request.session.clear()
    return redirect('/')