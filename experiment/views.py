from django.shortcuts import render, HttpResponseRedirect
from experiment.models import Peg, Color, Preview
from json import dumps, loads, JSONEncoder
from django.core.serializers import serialize
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
import json


def home(request):
	return render(request, 'experiment/index.html', {

    })
def create(request):
	if request.POST:
		print "hey"
		#print request.POST
		json_data=json.loads(request.POST['json'])
		pegs = json_data.get('pegs', 'not found')
		for json_peg in pegs:
			peg=Peg()
			peg.label_text=json_peg.get('stim_label', 'not found')
			peg.processingID=json_peg.get('processing_id', 'not found')
			peg.is_peg=json_peg.get('stim_type', 'not found')

			#define a color object and set it to the peg
			label_color=Color()
			json_label_color=json_peg.get('label_color', 'not found')
			label_color.red=json_label_color.get('R', 'not found')
			label_color.green=json_label_color.get('G', 'not found')
			label_color.blue=json_label_color.get('B', 'not found')
			label_color.save()
			peg.label_color=Color.objects.get(id=label_color.id)

			#define a color object and set it to the peg
			json_label_color=json_peg.get('peg_color', 'not found')
			peg_color=Color(red=json_label_color.get('R', 'not found'),
				green=json_label_color.get('G', 'not found'),
				blue=json_label_color.get('B', 'not found'))
			peg_color.save()
			peg.peg_color=Color.objects.get(id=peg_color.id)


			peg.save()
		return HttpResponseRedirect('/')
	return render(request, 'experiment/create.html', {
    })

def load(request):
	if request.POST:
		p = Preview()

		color = Color()
		color.red = request.POST['RSliderBoard']
		color.blue = request.POST['BSliderBoard']
		color.green = request.POST['GSliderBoard']
		color.save()

		p.board_color = color

		color = Color()
		color.red = request.POST['RSliderBackground']
		color.blue = request.POST['BSliderBackground']
		color.green = request.POST['GSliderBackground']
		color.save()

		p.background_color = color

		try:
			request.POST['labelsShow']
		except:
			p.show_labels = False

		for field in Preview._meta.fields[4:]:
			setattr(p, field.name, request.POST[field.name])

		p.save()
	return render(request, 'experiment/previewExperiment.html', {
	    })



def uploader(request):
	if request.POST:
		print "hey"
		#y=loads(serialize('json',request.POST['json']))
		#lol=LazyEncoder()
		#lo=lol.default(request.POST['json'])
		v=json.loads(request.POST['json'])
		
		#print v
		for i in v:
			print "yolo"
			print i.peg_color
		peg=Peg()
		peg.label_text="mine"
		peg.processingID="0"
		#peg.image=request.FILES['image']
		peg.label_color=Color.objects.all()[0]
		peg.peg_color=Color.objects.all()[0]
		peg.is_peg=True
		#peg.save()
		return HttpResponseRedirect('/')      
	return render(request, 'experiment/uploader.html', {
    })


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)