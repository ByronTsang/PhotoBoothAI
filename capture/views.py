from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.mixins import LoginRequiredMixin
#from braces.views import SelectRelatedMixin
from django.views import generic
from django.contrib.auth.decorators import login_required

from .forms import EmailForm
from photos import models
from albums.models import Album
from django.contrib.auth import get_user_model
User = get_user_model()

from django.http import HttpResponse, HttpResponseRedirect
import qrcode
from django.utils.six import BytesIO

from django.core.mail import send_mail
from django.conf import settings


from django.core.mail import send_mail, BadHeaderError

# Create your views here.

def index(request):
    return render(request, 'capture/index.html', {})

#Capture photos Class
class CapturePhotos(generic.ListView):
    model = models.Photo
    template_name = "capture/capturejs.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(album_id=1)

#Single photo Detail class 
class CapturePhotoDetail(generic.DetailView, generic.FormView):
    model = models.Photo
    form_class = EmailForm
    template_name = "capture/photo_detail.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            from django.core.mail.message import EmailMessage
            filepath = str(models.Photo.objects.get(id=self.kwargs.get("pk")))
            email = EmailMessage(subject='Check out your photo:' + self.kwargs.get("pk"),
                                 body='Your photo ID:' + self.kwargs.get("pk") + ' is attached in this mail.',
                                 from_email='no_reply@somebody.com',#settings.EMAIL_HOST_USER,
                                 to=[form.cleaned_data['to_email']]
                                )
            email.attach_file(settings.BASE_DIR + filepath)
            try:
                email.send(fail_silently=not(settings.DEBUG))
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('capture:home')
        else:
            return self.form_invalid(form)
    
def generate_qrcode(request, data):
    img = qrcode.make(data)
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    return response

