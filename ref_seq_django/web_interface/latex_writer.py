import os
import time

__author__ = 'mwelland'
__version__ = 1.3
__version_date__ = '11/02/2015'
""" This will be a class to receive a list of objects and a file name
    and compose the output to be written to file
    This will also check if an existing file has the same name and file
    location as the intended output file, and offer to cancel the write
    process or to delete the existing file contents to make way for new
    output
"""

class LatexWriter:

    def __init__(self):
        pass


    def run(self, input_list, filename):
        self.input_list = input_list
        self.filename = filename

        self.outfile_name = self.filename+'_'+time.strftime("%d-%m-%Y")+\
                        '_'+time.strftime("%H-%M-%S")+'.tex'
        self.pdfname = self.filename+'_'+time.strftime("%d-%m-%Y")+\
                        '_'+time.strftime("%H-%M-%S")+'.pdf'

        out = open(self.outfile_name, "w")
        self.fill_output_file(out)
        return self.outfile_name, self.pdfname

    def fill_output_file(self, out):

        for line in self.input_list:
            print >> out, line
        print 'File written'