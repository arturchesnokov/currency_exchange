from django.http import HttpResponse, Http404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, View, FormView
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect

from account.models import Contact, User, ActivationCodeSms
from account.tasks import send_email_async

from account.forms import CustomUserCreationForm, SignUpForm, ActivateForm


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

    success_url = reverse_lazy('account:activate')
    form_class = SignUpForm

    def get_success_url(self):
        self.request.session['user_id'] = self.object.id
        us_id = [self.object.id]
        return reverse_lazy('account:activate', args=us_id)
        # return reverse_lazy('account:activate', kwargs={'us_id' : us_id})


class Activate(FormView):
    form_class = ActivateForm
    template_name = 'signup.html'

    def get_initial(self):
        initials = super(Activate, self).get_initial()
        # breakpoint()
        initials['user_id'] = self.request.path.split('/')[-1]
        return initials

    #
    # def get_success_url(self):
    #     pk = self.kwargs['user_id']
    #     return reverse('banker', kwargs={'pk': pk})

    def post(self, request):
        user_id = request.session['user_id']
        sms_code = request.POST['sms_code']
        ac = get_object_or_404(
            ActivationCodeSms.objects.select_related('user'),
            code=sms_code,
            user_id=user_id,
            is_activated=False
        )

        if ac.is_expired:
            raise Http404

        ac.is_activated = True
        ac.save(update_fields=['is_activated'])

        user = ac.user
        user.is_active = True
        user.save(update_fields=['is_active'])
        return redirect('index')
