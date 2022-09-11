from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})


#for setting the csrf cookie
def index(request):
	#set session
    if not request.session or not request.session.session_key:
        request.session.save()
    print(request.session.session_key)
    
	#if request.method == 'GET':
	#	print('GET')
    #data = {}
    #data = "Waiting for server..."
    #return render(request, 'base.html')
    #return HttpResponse(data)
    return render(request, "index.html")

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
	return render(request, 'index/success.html')

def success(request):
	return render(request, 'index/success.html')