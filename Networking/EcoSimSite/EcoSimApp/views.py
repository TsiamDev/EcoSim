from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json

#for setting the csrf cookie
def index(request):
	#set session
	if not request.session or not request.session.session_key:
   		request.session.save()
	print(request.session.session_key)
	#data = {}

	if request.method == 'GET':
		print('GET')

	return render(request, 'base.html')#, data)

#for setting the tractor actions (by voting)
def set_tractor_actions(request):
	#if not request.session or not request.session.session_key:
   	#	request.session.save()
	print(request.session.session_key)
	data = {}
	if request.method == 'POST':
		print('POST')
		for k,v in request.POST.items():
			if k != 'csrfmiddlewaretoken':
				data[k] = v
		print(data)
	else:
		print('Something went wrong')

	#TODO generate HTML and return it
	response = HttpResponse()
	response.write(data)
	return render(request, 'success.html')

def success(request):
	return render(request, 'index/success.html')