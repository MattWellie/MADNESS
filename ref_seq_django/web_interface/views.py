from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadForm
from django.core.servers.basehttp import FileWrapper

import os


def index(request):
    html = '<html><body>This is the ref seq home page</body></html>'
    return HttpResponse(html)


def upload_file(request):

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the actual form stuff here
            print 'The form has been accepted'
            line = handle_uploaded_file(request.FILES['file'])
            print line
            return render(request, 'web_interface/success.html', {'line':line})
    else:
        form = UploadForm()
    return render(request, 'web_interface/upload.html', {'form':form})


def handle_uploaded_file(input_file):

    filename, extension = os.path.splitext(input_file.name)
    filepath = '/tmp/somefile.txt'
    with open(filepath, 'wb') as destination:
        for chunk in input_file.chunks():
            destination.write(chunk)
    return process_file(filepath, extension)


def process_file(filepath, extension):

    with open(filepath, 'r') as handle:
        line = handle.readline()
    return line


def send_file(request, filename):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Length'] = os.path.getsize(filename)
    return response