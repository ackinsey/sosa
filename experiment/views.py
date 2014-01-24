from django.shortcuts import render

def home(request):
	return render(request, 'experiment/index.html', {

    })
def create(request):
	return render(request, 'experiment/create.html', {

    })
