from django.http import HttpResponse, Http404
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

from account.models import Contact, User, ActivationCode
from account.tasks import send_email_async

from account.forms import CustomUserCreationForm, SignUpForm


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


class SignUpView(CreateView):
    template_name = 'signup.html'
    queryset = User.objects.all()

    success_url = reverse_lazy('index')
    form_class = SignUpForm


class Activate(View):
    def get(self, request, activation_code):
        ac = get_object_or_404(ActivationCode.objects.select_related('user'),
                               code=activation_code, is_activated=False)

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')
