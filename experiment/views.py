from django.shortcuts import render, HttpResponseRedirect
from experiment.models import Stimulus, Color, Experiment, Order, OrderItem
from json import dumps, loads, JSONEncoder
from django.core.serializers import serialize
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from settings import MEDIA_URL
import json


def home(request):
	return render(request, 'experiment/index.html', {
    })
def create(request):
	if request.POST:
		json_data=json.loads(request.POST['json'])
		experiment_data = json_data.get('experiment', 'not found')
		stimulus_data = json_data.get('pegs', 'not found')
		order_data = json_data.get('orders', 'not found')

		experiment=Experiment(name=experiment_data.get('name','not found'), version=experiment_data.get('version','not found'),
			show_stimulus_relative_size=experiment_data.get('show_stim','not found'),window_x=experiment_data.get('window_x','not found'),
			window_y=experiment_data.get('window_y','not found'))
		if request.FILES and 'board_image' in request.FILES:
			experiment.board_image=request.FILES['board_image']
		experiment.save()

		for index,json_peg in enumerate(stimulus_data):
			stimulus=Stimulus(experiment=experiment,form_id=json_peg.get('stim_index', 'not found'),label_text=json_peg.get('stim_label', 'not found'),
				processingID=json_peg.get('processing_id', 'not found'),
				is_peg=json_peg.get('stim_type', 'not found'))
			
			#define a color object and set it to the peg	
			json_label_color=json_peg.get('label_color', 'not found')
			label_color=Color(red=json_label_color.get('R', 'not found'),
				green=json_label_color.get('G', 'not found'),
				blue=json_label_color.get('B', 'not found'))
			label_color.save()
			stimulus.label_color=Color.objects.get(id=label_color.id)

			#define a color object and set it to the peg
			json_label_color=json_peg.get('peg_color', 'not found')
			peg_color=Color(red=json_label_color.get('R', 'not found'),
				green=json_label_color.get('G', 'not found'),
				blue=json_label_color.get('B', 'not found'))
			peg_color.save()
			stimulus.peg_color=Color.objects.get(id=peg_color.id)
			stimulus.experiment=experiment
			if 'stimulus_image_'+str(index) in request.FILES:
				stimulus.image=request.FILES['stimulus_image_'+str(index)]
			stimulus.save()
		for index,json_order in enumerate(order_data):
			order = Order(experiment=experiment,name="Order "+str(index+1))
			order.save()
			for json_order_item in json_order.get('order_items', 'not found'):
				order_item=OrderItem(stimulus=Stimulus.objects.get(experiment=experiment,form_id=json_order_item.get('stim_index', 'not found')),order=order)	
				order_item.save()
		return HttpResponseRedirect('/')
	return render(request, 'experiment/create.html', {
		"MEDIA_URL":MEDIA_URL
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
	experiment=Experiment.objects.all()[0]
	orders=Order.objects.filter(experiment=experiment)
	stim_orders=[]
	for order in orders:
		stim_orders.append(OrderItem.objects.filter(order=order))
	return render(request, 'experiment/previewExperiment.html', {
		"orders":stim_orders,
		"experiment":experiment,
	    })
