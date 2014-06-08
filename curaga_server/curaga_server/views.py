from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import os
from .models import Package, PackageDownload
# Create your views here.

def home(request):
    """Renders a howto template"""
    data = {}
    return render_to_response('home.html', RequestContext(request, data))

@csrf_exempt
def upload(request):
    """accepts a post request that stores a file on the server
    and makes a record of the package's existance in the db"""
    #TODO:  allow a user to reupload his own package, prevent
    #       another user from overriding a package
    if request.method != 'POST':
        return redirect(reverse('home'))

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        # pointer to the file
        package = request.FILES['package']
        # name of uploaded file
        package_file_name = package.name
        # name of uploaded file without the extension
        package_name = package_file_name.split('.')[0]

        # make a database record of the package
        try:
            package_record = Package()
            package_record.name = package_name
            package_record.file_name = package_file_name
            package_record.package = package
            package_record.user = user
            package_record.save()
        except:
            return HttpResponse("A package named %s already exists." % package_name)

        return HttpResponse("Successfully uploaded %s" % package.name)

    return HttpResponse("Invalid credentials. Have you registered?")



def package(request, package_name):
    """accepts a get request and returns a script that when piped
    to the shell will download the package"""
    #TODO:  write the script to download/install
    package = Package.objects.get(name=package_name)
    package_download = PackageDownload()
    package_download.package = package
    package_download.ip = request.META.get('REMOTE_ADDR')
    package_download.save()
    return HttpResponse("script to download and install the file. file url is %s" % package.package.url)


@csrf_exempt
def register(request):
    """An endpoint for adding users for package upload"""
    if request.method != 'POST':
        return redirect(reverse('home'))

    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    print username, password, email

    try:
        new_user = User.objects.create_user(username, email, password)
        return HttpResponse("success")
    except:
        raise
        return HttpResponse("failure")

