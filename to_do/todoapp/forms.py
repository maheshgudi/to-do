from django.contrib.auth.models import User, Group
from django import forms

# Local import
from todoapp.models import Task


class UserLoginForm(forms.Form):
    """
    User login form for to-do app
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegisterForm(forms.Form):
    """User registeration form for to-do app. Customises """

    username = forms.CharField(max_length=30, help_text='Letters, digits,\
                period and underscores only.')
    email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        max_length=30, widget=forms.PasswordInput())

    def clean_username(self):
        u_name = self.cleaned_data["username"]
        try:
            User.objects.get(username__exact=u_name)
            raise forms.ValidationError("Username already exists.")
        except User.DoesNotExist:
            return u_name

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if User.objects.filter(email=user_email).exists():
            raise forms.ValidationError("This email already exists")
        return user_email

    def clean_password(self):
        return self.cleaned_data['password']

    def clean_confirm_password(self):
        c_pwd = self.cleaned_data['confirm_password']
        pwd = self.data['password']

        if c_pwd != pwd:
            raise forms.ValidationError("Passwords do not match")
        return c_pwd

    def save(self):
        u_name = self.cleaned_data["username"]
        email = self.cleaned_data['email']
        pwd = self.cleaned_data["password"]
        new_user = User.objects.create_user(u_name, email, pwd)
        new_user.save()
        return u_name, email, pwd

class TaskForm(forms.ModelForm):
    """
    Form for tasks.
    """
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        print(*args)
    class Meta:
        model = Task
        exclude=['completed']
        
        # if user:
        #     try:
        #         group = user.groups.all().order_by("id").last()
        #     except AttributeError:
        #         print(dict(user))
        #     group_users = group.user_set.all()
        #     print("group_user", group_users)
        #     self.fields["assignee"] = forms.ModelChoiceField(
        #                                     queryset=group_users
        #                                     )
