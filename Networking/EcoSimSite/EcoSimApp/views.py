from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json

def index(request):
	data = {}
	if request.method == 'POST':
		print('POST')

		data['data'] = request.POST['data']
		print(data)
	else:
		print('GET')
	return render(request, 'base.html', data)