from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.conf import settings

from account.models import User
from account.models import Contact
from account.tasks import send_email_async

from account.forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserCreate(generic.CreateView):
    model = User
    fields = ['username', 'email']
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('index')


class ContactForm(CreateView):
    model = Contact
    fields = ('email', 'title', 'text')
    template_name = 'contact_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        email_from = form.instance.email
        subject = form.instance.title
        message = form.instance.text
        recipient_list = [settings.EMAIL_HOST_USER, ]
        send_email_async.delay(subject, message, email_from, recipient_list)
        return super().form_valid(form)


class MyProfile(UpdateView):
    template_name = 'my_profile.html'
    queryset = User.objects.filter(is_active=True)
    fields = ('email',)
    success_url = reverse_lazy('index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(id=self.request.user.id)
