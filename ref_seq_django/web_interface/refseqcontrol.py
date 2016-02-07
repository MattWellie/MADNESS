# -*- coding: utf-8 -*-
from LrgParser import LrgParser
from GbkParser import GbkParser
from reader import Reader
from latex_writer import LatexWriter
from subprocess import call
import os

__author__ = 'mwelland'
__version__ = 1.3
__version_date__ = '11/02/2015'
'''
    This module of the reference sequencer program will be replaced by a more comprehensive view

    Program flow:

    - GUI is generated
        - User chooses an input file (type: LRG (XML) / GenBank
        - User chooses an amount of intronic flanking sequence (number)
        - User clicks 'TRANSLATE'

    - The input file type is checked and the file_type variable is set
        - If the input is LRG, an LRG_Parser instance is created
        - If the input is GenBank, an GbkParser instance is created
        - The appropriate Parser instance is used to read the input file
            contents into a dictionary object which is returned
        - The dictionary has the following structure:

            Dict { pad
                   filename
                   genename
                   refseqname
                   transcripts {  transcript {   protein_seq
                                                 cds_offset
                                                 exons {        exon_number {   genomic_start
                                                                                genomic_stop
                                                                                transcript_start
                                                                                transcript_stop
                                                                                sequence (with pad)

        - Use of this dictionary structure allows for use of absolute references
            to access each required part of the processed input, and allows for
            the extension of the format to include any features required later

    - The returned dictionary is passed through a Reader instance, which scans
        through the created dictionary, and creates a list of Strings which
        represent the typesetting which will be used for the final output.
    - The Reader instance has been chosen to write out in a generic format, to
        allow the dictionary contents to be used as a text output or for LaTex.
        Use of a Boolean write_as_latex variable can be used to decide whether
        the output will include LaTex headers and footers

    - The list output from the Reader instance is written to an output file using
        a writer object. Currently this is a LatexWriter instance, using standard
        printing to file.This could be replaced with a print to .txt for inspection
    - The LatexWriter Class creates an output directory which contains a reference
        to the input file name, intronic padding, the date and time. This is done
        to ensure that the output directory is unique and identifies the exact point
        in time when the output file was created
    - The LatexWriter also creates the full PDF output using a Python facilitated
        command line call. The output '.tex' file is created in the new output
        directory and is processed using pdflatex
'''


def get_version():
    """
    Quick function to grab version details for final printing
    :return:
    """
    return 'Version: {0}, Version Date: {1}'.format(str(__version__), __version_date__)


