from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'marketsdataintelligence/home.html')

def about(request):
	return HttpResponse('<h1>About Markets data intelligence</h1>')                                   