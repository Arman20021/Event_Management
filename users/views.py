from django.shortcuts import render, redirect
 
from django.contrib.auth.models import Group
from django.contrib.auth import login,   logout
from django.contrib.auth.tokens import default_token_generator
from users.forms import CustomRegistrationForm
from django.contrib import messages
from users.forms import LoginForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm,CustomPasswordResetForm,CustomPasswordResetConfirmForm,EditProfileForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.views import LoginView,PasswordChangeDoneView,PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView,UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.contrib.auth import get_user_model
 
 

User=get_user_model() 
# Create your views here.
"""
class EditProfileView(UpdateView):
    model=User
    form_class=EditProfileForm
    template_name='accounts/update_profile.html'
    context_object_name='form'


    def get_object(self):
        return self.request.user
    
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['userprofile']=UserProfile.objects.get(user=self.request.user)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user_profile=UserProfile.objects.get(user=self.request.user)
        context['form']=self.form_class(instance=self.object,userprofile=user_profile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
"""

class EditProfileView(UpdateView):
    model=User
    form_class=EditProfileForm
    template_name='accounts/update_profile.html'
    context_object_name='form'


    def get_object(self):
        return self.request.user
 
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')


#test for user
# Test for users
def is_admin(user):
    return user.groups.filter(name='CEO').exists()


def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})


def sign_in(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔹 ROLE-BASED REDIRECTION
            if is_admin(user):
                return redirect('admin-dashboard')
            elif is_manager(user):
                return redirect('manager-dashboard')
            elif is_participant(user):
                return redirect('user-dashboard')
            else:
                return redirect('no-permission')

    return render(request, 'registration/login.html', {'form': form})

     
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user

        if is_admin(user):
            return reverse_lazy('admin-dashboard')
        elif is_manager(user):
            return reverse_lazy('manager-dashboard')
        elif is_participant(user):
            return reverse_lazy('user-dashboard')
        else:
            return reverse_lazy('no-permission')       

  

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    


def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
                user.is_active=True
                user.save()
                return redirect('sign-in')
        else:
             return HttpResponse ("Invalid ID or token")
    except User.DoesNotExist:
         return HttpResponse("User not found")



@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related('groups')

    for user in users:
        groups = list(user.groups.all())  
        if groups:
            user.group_name = groups[0].name
        else:
            user.group_name = 'No Groups Assigned'

    return render(request, 'admin/dashboard.html', {'users': users})

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role" 
                             )
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})


@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})


@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
     groups=Group.objects.prefetch_related('permissions').all()
     return render(request,'admin/group_list.html',{'groups':groups})


class ProfileView(TemplateView):
    template_name='accounts/profile.html'


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        user=self.request.user
        context['username']=user.username
        context['email']=user.email
        context['name']=user.get_full_name()
        context['member_since']=user.date_joined
        context['last_login']=user.last_login 
        context['bio']=user.bio 
        context['profile_image']=user.profile_image 



        return context


class ChangePassword(PasswordChangeView):
    template_name='accounts/password_change.html'
    form_class=CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name="registration/reset_password.html"
    success_url=reverse_lazy('sign-in')
    html_email_template_name='registration/reset_email.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol']='https' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context
         
    

    def form_valid(self,form):
        messages.success(self.request,"A reset password Email has sent. Please check your Email")
        return super().form_valid(form)   

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
     form_class=CustomPasswordResetConfirmForm
     template_name="registration/reset_password.html"
     success_url=reverse_lazy('sign-in')

     def form_valid(self,form):
        messages.success(self.request,"Password Reset Succesfully")
        return super().form_valid(form)   
