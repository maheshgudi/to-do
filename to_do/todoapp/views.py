from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

# local imports
from todoapp.models import Task
from todoapp.forms import (UserLoginForm, UserRegisterForm, TaskForm)
from todoapp.todoutils import (EmailManipulation)

# TODO: Use default django login view
# Put complexity in backend
def user_login(request):
    """
    Index page of Website. Also serves as a login page.
    """
    user = request.user
    if user.is_authenticated():
        return redirect('home')
    else:
        context = {}
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                cred = form.cleaned_data
                try:
                    user = authenticate(email=cred['email'],
                                        password=cred['password']
                                        )
                except User.DoesNotExist:
                    messages.error(request,
                                   'No email by that name.'
                                   )
                if user.is_active:
                    login(request, user)
                    return redirect('home')
        else:
            context["form"] = UserLoginForm()
    return render(request, 'login.html', context)

@login_required(login_url='/login')
def home(request):
    """Logged in user home page. Can see tasks assigned to them. Can mark
       tasks as completed.
    """
    user = request.user
    context = {}
    context["user"] = user
    return render(request, 'home.html', context)


def user_register(request):
    """ Register a new user."""
    user = request.user
    if user.is_authenticated():
        return redirect("home")
    context = {}
    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            u_name, user_email, pwd = form.save()
            new_user = authenticate(email=user_email, password=pwd)
            login(request, new_user)

            user_email_domain = EmailManipulation.get_email_domain(user_email)
            group_content_type = ContentType.objects.get_for_model(Group)
            if user_email_domain:
                user_group, created = Group.objects.get_or_create(
                    name=user_email_domain
                    )
                user_group.user_set.add(user)
                user_group.save()
                if created:
                    permission = Permission.objects.create(
                        codename='is_admin',
                        content_type=group_content_type,
                        name="Is Group Admin"
                        )
                    user.user_permissions.add(permission)
                    user.save()
            return redirect('home')
        else:
            form = UserRegisterForm()
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})


#TODO: When doing POST always redirect. never render
@login_required(login_url='/login')
def show_group_tasks(request):
    """ Show all pending tasks of the user group."""
    user = request.user
    context = {}
    user_group = user.groups.all().first()
    group_tasks = Task.objects.filter(completed=False, group=user_group)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.cleaned_data["group"] = user_group
            form.save()
    else:
        form = TaskForm()
    context['all_tasks'] = group_tasks
    return render(request, 'show_tasks.html', {'form': form})


# if request.POST.get('done') == 'done':
#     data = request.POST.getlist('my_tasks')
#     if data is not None:
#         tasks_done = Task.objects.filter(id__in=data)
#         for task in tasks_done:
#             task.completed = True
#             task.save()
