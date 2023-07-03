from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import views
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from .forms import UserFormLogin, UserRegisterForm, ProfileForm
from users.models import EmailVerif
# Create your views here.


class Login(views.LoginView):
    form_class = UserFormLogin
    template_name = "users/login.html"
    

class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = '/users/login'
    success_message = 'Вы успешно зарегистрированы'


@login_required
def profile(request):
    if request.method == "POST":
        form_u = ProfileForm(instance=request.user, data=request.POST)
        form_p = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form_u.is_valid() and form_p.is_valid():
            form_u.save()
            form_p.save()
            return HttpResponseRedirect('/')
    else:
        form_u = ProfileForm(instance=request.user)
        form_p = ProfileForm(instance=request.user.profile)

    context = {
        'title': 'Store - Профиль', 
        'form_u': form_u, 
        'form_p': form_p,
    }
    return render (request, 'users/profile.html', context)
#Для обработки ссылки подтверждения пароля
class EmailVerificationView(TemplateView):
    
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerif.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))