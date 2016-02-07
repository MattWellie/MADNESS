from django.shortcuts import render
from django.http import HttpResponseRedirect

from django import forms


class UploadForm(forms.Form):
    file = forms.FileField()
