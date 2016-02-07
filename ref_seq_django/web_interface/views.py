from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadForm
from .models import created_documents
from django.core.servers.basehttp import FileWrapper
from LrgParser import LrgParser
from GbkParser import GbkParser
from reader import Reader
from latex_writer import LatexWriter
from subprocess import call
import os, sys


@property
def get_version():
    """
    Quick function to grab version details for final printing
    :return:
    """
    return 'Version: {0}, Version Date: {1}'.format('0.1', '7/2/2016')


def run_parser(filepath):
    print >>sys.stderr, 'Parsing started with {}'.format(filepath)

    padding = 300
    file_type = check_file_type(filepath)
    if file_type == 'file error':
        print >>sys.stderr, file_type
    dictionary = {}
    if file_type == 'gbk':
        gbk_reader = GbkParser(filepath, padding, True)
        dictionary = gbk_reader.run()
        parser_details = gbk_reader.get_version
    elif file_type == 'lrg':
        lrg_reader = LrgParser(filepath, padding, True)
        dictionary  = lrg_reader.run()
        parser_details = lrg_reader.get_version
    parser_details = '{0} {1} {2}'.format(file_type.upper(), 'Parser:', parser_details)
    files_created = {}
    os.chdir(os.path.join('web_interface', 'output'))
    for transcript in dictionary['transcripts']:
        input_reader = Reader()
        writer = LatexWriter()
        reader_details = 'Reader: ' + input_reader.get_version
        writer_details = 'Writer: ' + writer.get_version
        xml_gui_details = 'Control: {}'.format(get_version)
        list_of_versions = [parser_details, reader_details, writer_details, xml_gui_details]
        input_list, nm = input_reader.run(dictionary, transcript, True, list_of_versions, True, file_type, 'web user')
        transcript_accession = dictionary['transcripts'][transcript]['NM_number']
        file_name = transcript_accession
        latex_file, pdf_file = writer.run(input_list, file_name)
        call(["pdflatex", "-interaction=batchmode", latex_file])
        save_as_model = created_documents(transcript=transcript_accession, location=pdf_file)
        save_as_model.save()
        clean_up(os.getcwd())
    os.chdir(os.pardir) # Web interface
    os.chdir(os.pardir) # project level


def clean_up(path):
    pwd_files = os.listdir(path)
    for file in pwd_files:
        if 'pdf' not in file:
            os.remove(os.path.join(path, file))


def check_file_type(file_name):
    """
        This function takes a file name and determines the type via extension
        If the extension is not appropriate for the program, an error is returned
    """
    if file_name[-3:] == 'xml':
        return 'lrg'
    elif file_name[-2:] == 'gb':
        return 'gbk'
    elif file_name[-3:] == 'gbk':
        return 'gbk'
    else:
        return 'file error'


def index(request):
    html = '<html><body>This is the ref seq home page</body></html>'
    return HttpResponse(html)


def upload_file(request):

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle the actual form stuff here
            print >> sys.stderr, os.getcwd()
            filepath = handle_uploaded_file(request.FILES['file'])
            run_parser(filepath)
            #wrapper = FileWrapper(file(filepath))
            #response = HttpResponse(wrapper, content_type='application/pdf')
            #response['Content-Length'] = os.path.getsize(filepath)
            #response['Content-Disposition'] = 'attachment; filename="{}"'.format(filepath)
            #return response
            return render(request, 'web_interface/success.html', {'line':filepath})
    else:
        form = UploadForm()
    return render(request, 'web_interface/upload.html', {'form':form})


def handle_uploaded_file(input_file):

    filepath = os.path.join('web_interface', 'input', input_file.name)
    with open(filepath, 'wb') as destination:
        for chunk in input_file.chunks():
            destination.write(chunk)
    return filepath


def download(request, filename):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    if request.method == 'POST':
        pass
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response