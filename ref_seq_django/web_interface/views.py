from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadForm
from django.core.servers.basehttp import FileWrapper
from LrgParser import LrgParser
from GbkParser import GbkParser
from reader import Reader
from latex_writer import LatexWriter
from subprocess import call
import os

import os


@property
def get_version(self):
    """
    Quick function to grab version details for final printing
    :return:
    """
    return 'Version: {0}, Version Date: {1}'.format('0.1', '7/2/2016')

def run_parser(filepath, file_type):

    padding = 300
    file_name = filepath.split('/')[-2] + '/' + filepath.split('/')[-1]
    file_type = check_file_type(filepath)
    if file_type == 'file error':
        return ['error']
    dictionary = {}
    if file_type == 'gbk':
        gbk_reader = GbkParser(file_name, padding, True)
        dictionary = gbk_reader.run()
        parser_details = gbk_reader.get_version
    elif file_type == 'lrg':
        lrg_reader = LrgParser(file_name, padding, True)
        dictionary  = lrg_reader.run()
        parser_details = lrg_reader.get_version

    parser_details = '{0} {1} {2}'.format(file_type.upper(), 'Parser:', parser_details)
    files_created = []
    os.chdir("output")
    for transcript in dictionary['transcripts']:
        print 'transcript: %d' % transcript

        input_reader = Reader()
        writer = LatexWriter()
        reader_details = 'Reader: ' + input_reader.get_version
        writer_details = 'Writer: ' + writer.get_version
        xml_gui_details = 'Control: ' + get_version()
        list_of_versions = [parser_details, reader_details, writer_details, xml_gui_details]
        lrg_num = file_name.split('.')[0].split('/')[1].replace('_', '\_')+'t'+str(transcript)
        input_list, nm = input_reader.run(dictionary, transcript, True, list_of_versions, True, file_type, lrg_num, 'web user')
        if file_type == 'gbk':
            filename = dictionary['genename']+'_'+ nm
        else:
            filename = dictionary['genename']+'_'+ file_name.split('.')[0].split('/')[1]+'t'+str(transcript)
        latex_file, pdf_file = writer.run(input_list, filename)
        call(["pdflatex", "-interaction=batchmode", latex_file])
        files_created.append(pdf_file)
        clean_up(os.getcwd(), pdf_file)


def clean_up(path, pdf_file):
    pdf_split = pdf_file.split('_')
    pwd_files = os.listdir(path)
    pdf_files = [doc for doc in pwd_files if \
                doc.split('.')[-1] == 'pdf']
    for target in pdf_files:
        if target == 'tex files':
            pass
        else:
            target_split = target.split('_')
            if target_split[0:3] == pdf_split[0:3]\
                and target_split[-2:] != pdf_split[-2:]:
                os.remove(os.path.join(path, target))
    targets = [doc for doc in pwd_files if \
                doc.split('.')[-1] not in ['pdf', 'tex']]
    for target in targets:
        if target == 'tex files':
            pass
        else:
            os.remove(os.path.join(path, target))


def check_file_type(file_name):
    """
        This function takes a file name and determines the type via extension
        If the extension is not appropriate for the program, an error is returned
    """
    if file_name[-4:] == '.xml':
        return 'lrg'
    elif file_name[-3:] == '.gb':
        return 'gbk'
    elif file_name[-4:] == '.gbk':
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
            filepath, extension = handle_uploaded_file(request.FILES['file'])

            wrapper = FileWrapper(file(filepath))
            response = HttpResponse(wrapper, content_type='application/pdf')
            response['Content-Length'] = os.path.getsize(filepath)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filepath)
            return response
            #return render(request, 'web_interface/success.html', {'line':filepath})
    else:
        form = UploadForm()
    return render(request, 'web_interface/upload.html', {'form':form})


def handle_uploaded_file(input_file):

    filename, extension = os.path.splitext(input_file.name)
    filepath = '/tmp/somefile.txt'
    with open(filepath, 'wb') as destination:
        for chunk in input_file.chunks():
            destination.write(chunk)
    return filepath, extension


def download(request, filename):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response