from django.shortcuts import render, HttpResponse, redirect
from ..login_registration.models import User
from .models import Message, Comment, Description
from ..harttv_app.models import Show, ShowRating, Review
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import bcrypt
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    user = User.objects.get(id=request.session['id'])
    boolean = user.admin
    context = {
        "users": User.objects.all(),
        "boolean": boolean
    }

    return render(request, 'dashboard/dashboard.html', context)



def add_user(request):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    user = User.objects.get(id=request.session['id'])
    boolean = user.admin
    if boolean:
        return render(request, 'dashboard/add_user.html')
    else:
        return redirect('dashboard:index')


def create_user(request):
    if request.method =='POST':
        userObject = User.objects.isValidRegistration(request.POST)
    return redirect(reverse('dashboard:index'))

def edit_user(request, user_id):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    print user_id
    user = User.objects.get(id=user_id)

        

    admin_user = User.objects.get(id=request.session['id'])
    context = {
        "user": user,
        "boolean": admin_user.admin,
    }

    description = Description.objects.filter(user=user)
    if len(description) > 0:
        context['description'] = description[0]
    if admin_user.admin or int(user_id) == request.session['id']:
        print user.admin
        print "i'm an admin"
        return render(request, 'dashboard/edit_user.html', context)
    else:
        print "not rendering correctly >:("
        return redirect(reverse('dashboard:index'))

def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        print request.POST
        if 'password' in request.POST and request.POST['password'] == request.POST['password']:
            hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            print hashed
            user.password = hashed
            user.save()
            #user.password = request.POST['password']
        else:
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            if 'admin' in request.POST:
                user.admin = request.POST['admin']
            user.save()

    # if password in request.POST
    # do password change
    #else do information change.
    return redirect(reverse('dashboard:index'))

def update_user_description(request, user_id):
    user = User.objects.get(id=user_id)
    description = Description.objects.filter(user=user)
    if request.method == 'POST':
        if len(description) > 0:
            Description.objects.filter(user=user).update(description_text=request.POST['description'])
        else:
            Description.objects.create(description_text=request.POST['description'], user=user)
    return redirect(reverse('dashboard:index'))
    
        
    
    

def destroy_user(request, user_id):
    current_user = User.objects.get(id=request.session['id'])
    user_to_delete = User.objects.get(id=user_id)
    if current_user.admin and not user_to_delete.admin:
        user = User.objects.get(id=user_id).delete()
    return redirect(reverse('dashboard:index'))

def show_user(request, user_id):
    if not 'id' in request.session:
        return redirect(reverse('auth:index'))
    user = User.objects.get(id=user_id)
    if Description.objects.filter(user=user):
        description = Description.objects.get(user=user)
    else:
        description = "The user has not yet entered a bio!"
    context = {
        "user": user,
        "messages": Message.objects.filter(wall=user),
        "top_rated_shows": ShowRating.objects.filter(user=user).order_by('-rating', 'show__title'),
        "users_reviews": Review.objects.filter(user=user).order_by('-rating__rating'),
        "description": description,
    }
    #create forms, render messages on show page and you're done :)
    return render(request, 'dashboard/show_user.html', context)

def create_message(request, wall_id):
    if request.method == 'POST':
        wall_id = wall_id
        poster_id = request.session['id']
        user_who_owns_wall = User.objects.get(id=wall_id)
        user_who_posted_message = User.objects.get(id=poster_id)

        Message.objects.create(message_text=request.POST['message'], wall=user_who_owns_wall, user=user_who_posted_message)

        print "the wall and poster ids are", wall_id, poster_id
        url = reverse('dashboard:show_user', kwargs={'user_id': wall_id})
        return HttpResponseRedirect(url)
    
def create_comment(request, message_id):
    if request.method =='POST':
        message_id = message_id
        message = Message.objects.get(id=message_id)
        user_who_commented = User.objects.get(id=request.session['id'])
        wall_id = message.wall.id

        Comment.objects.create(comment_text=request.POST['comment'], message=message, commenter=user_who_commented)
        url = reverse('dashboard:show_user', kwargs={'user_id': wall_id})
        return HttpResponseRedirect(url)




