from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

class LoginHome(TemplateView):
    template_name = 'loginhome.html' #after logging in: test.html is loaded

class LogoutHome(TemplateView):
    template_name = 'logouthome.html' #after logging out: thanks.html is loaded

class HomePage(TemplateView):
    template_name = "index.html" #default Homepage : index.html 

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("loginhome")) #after logging in : reversed to loginhome.html
        return super().get(request, *args, **kwargs)

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)