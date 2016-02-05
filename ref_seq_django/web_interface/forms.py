from django.shortcuts import render
from django.http import HttpResponseRedirect

from django import forms


class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()