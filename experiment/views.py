from django.shortcuts import render, redirect,render_to_response,  HttpResponse, HttpResponseRedirect
from experiment.models import Stimulus, Color, Experiment, Order, OrderItem, Results, Preview
from json import dumps, loads, JSONEncoder
from django.core.serializers import serialize
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from django.template import RequestContext
from settings import MEDIA_URL
import json, datetime, csv

def home(request):
	"""Sends the user to the homepage. Also sends Experiments to the page so they can be displayed as options to be loaded."""
	return render_to_response('experiment/index.html', {
		"stimulus":Stimulus.objects.values('label_text','experiment__name','experiment').order_by('experiment')
    },context_instance=RequestContext(request))

def create(request):
	"""The create page is where the user creates the Experiment and its related stimulus. This view handles all the data being submitted to the server."""
	
	""""If there is nothing in the POST that means the user was redirected or went to the page and didn't try to submit the form. In this case we will send them to a new form. If there is data in the post that data needs to be processed."""
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
			text = json_peg.get('stim_label', 'not found')
			text = text.replace(' ', '_')
			stimulus=Stimulus(experiment=experiment,form_id=json_peg.get('stim_index', 'not found'),label_text=text,
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
		"MEDIA_URL":MEDIA_URL,
		"stimulus":Stimulus.objects.all(),
    })

def load(request):
	""""The Load view is where the Preview model is constructed. It also allows the user to get a visual preview of what affect their changes will have."""

	"""If the POST has data in it we want to save it in the database. If not we want to display the page so they can fill out the form."""
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

		p.hide_background=True if request.POST['hide_background']=='true' else False
		p.position=request.POST['position']
		p.shade=request.POST['shade']
		p.show_label=True if request.POST['show_label']=='true' else False
		p.size=request.POST['size']

		p.experiment=Experiment.objects.get(id=request.GET['experiment_id'])
		p.save()
		return render(request, 'experiment/prompt.html', {
		})
	if request.GET:
		experiment=Experiment.objects.get(id=request.GET['experiment_id'])
	else:		
		experiment=Experiment.objects.all()[0]
	orders=Order.objects.filter(experiment=experiment)
	stim_orders=[]
	for order in orders:
		stim_orders.append(OrderItem.objects.filter(order=order))
	return render(request, 'experiment/previewExperiment.html', {
		"orders":stim_orders,
		"experiment":experiment,
		"previews":Preview.objects.all()
	    })

def save_settings(request):
	"""This is the AJAX based view for creating a new Preview instance. It is activated by hitting the Export button on the Preview page."""
	if request.POST:
		finalData=json.loads(request.POST['finalData'])

		boardColor=finalData['board_color']
		bd_color=Color(red=boardColor['red'],green=boardColor['green'],blue=boardColor['blue'])
		bd_color.save()

		backgroundColor=finalData['background_color']
		bg_color=Color(red=backgroundColor['red'],green=backgroundColor['green'],blue=backgroundColor['blue'])
		bg_color.save()

		preview=Preview(experiment=Experiment.objects.get(id=finalData['experiment_id']),hide_background=finalData['hide_background'], name=finalData['preview_name'], board_color= bd_color,background_color=bg_color,show_label=finalData['show_labels'],position=finalData['position'],shade=finalData['shade'],size=finalData['size'])
		preview.save()
	response=HttpResponse()
	return response

def save_stimulus(request):
	"""This view hasn't been implemented, but it includes the fundamentals to save the stimulus asynchronously through the Create Experiment page."""
	if request.POST:
		finalData=json.loads(request.POST['finalData'])

		label_color=finalData['label_color']
		l_color=Color(red=label_color['red'],green=label_color['green'],blue=label_color['blue'])
		l_color.save()

		peg_color=finalData['peg_color']
		p_color=Color(red=peg_color['red'],green=peg_color['green'],blue=peg_color['blue'])
		p_color.save()

		ex=Experiment(name="",version="",window_x=0,window_y=0)
		ex.save()
		print request.FILES
		print request.POST
		stimulus=Stimulus(experiment=ex,form_id=-1, label_text=finalData['label_text'],processingID=finalData['id'],image=request.POST['image'],
			label_color=l_color,peg_color=p_color,is_peg=finalData['is_peg'],peg_size=finalData['peg_size'],image_size=finalData['image_size'])
		stimulus.save()
	response=HttpResponse()
	return response

def run(request, id, startTime, subjectID=None):
	"""This is the view fired off when the experiment is started. It returns the data required to run an experiment."""
	experiment=Experiment.objects.get(id=id)
	#were just going to grab the last one here.
	preview = Preview.objects.filter(experiment=experiment).order_by('-id')[0]
	stimuli=Stimulus.objects.filter(experiment=experiment)
	return render(request, 'experiment/SOSAModelingExperiment.html', {
		"preview":preview,
		"stimuliList":stimuli,
		"experiment":experiment,
		"MEDIA_URL":MEDIA_URL,
		"subjectID":subjectID,
		'startTime':startTime
	})

def finish(request):     
	"""This view is called when the user completes the experiment. It creates the Results model so the data can later be exported."""
	
	try:
		dict = eval(request.POST['finalData'])
		results = Results(experiment=Experiment.objects.get(id=dict['experiment_id']),preview_start_time=dict['prevStartTime'],experiment_start_time=dict['startTime'],experiment_end_time=dict['endTime'],actions=dict['pegMoves'],final_positions=dict['finalPositions'], distances=dict['distances'],subject_id=dict['subjectID'], order=dict['pegOrder'])
		results.save()
	except:
		pass
	
	return render(request, 'experiment/index.html', {
		"stimulus":Stimulus.objects.values('label_text','experiment__name','experiment').order_by('experiment'),
		"results_id":Results.objects.all().order_by('-experiment_end_time')[0].id,
    })


def view_stimuli(request):
	"""The view_stimuli view gives the subject a preview of the different stimulus included in the experiment. Once the user is finished viewing the stimulus the experiment is started from here."""
	experiment = Experiment.objects.get(id=request.GET['experiment_id'])
	orders=Order.objects.filter(experiment=experiment)
	stim_orders=[]
	for order in orders:
		stim_orders.append(OrderItem.objects.filter(order=order))
	"""If there's data (time and id) in the POST start the experiment. Otherwise just display the view_stimuli page."""
	if request.POST:
		return run(request, request.GET['experiment_id'], request.POST['prevstartTime'], request.POST['subjectID'])
	return render(request, 'experiment/stimuli_preview.html', {
		"experiment":experiment,
		"orders":stim_orders,
	})

def view_all(request):
	"""The view_all view is fired off from the view_stimuli view when the user clicks the 'View All' button. This view allows the user to see all of the stimulus related to a specific experiment."""
	experiment = Experiment.objects.get(id=request.GET['experiment_id'])
	orders=Order.objects.filter(experiment=experiment)
	stim_orders=[]
	for order in orders:
		stim_orders.append(OrderItem.objects.filter(order=order))

	return render(request, 'experiment/viewStimuli.html', {
		"experiment":experiment,
		"orders":stim_orders,
	})	

def about(request):
	"""Simple static about page for the SOSA project. Hopefully will be helpful when viewed locally on a VM without an Internet connection."""
	return render(request, 'experiment/about.html', {})

def view_results(request, id):
	"""This view creates and initializes the download of the csv file associated with the completed experiment."""
	results=Results.objects.get(id=id)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="'+results.experiment.name+'.csv"'
	writer = csv.writer(response)
	writer.writerow(['Experiment:', results.experiment.name])
	writer.writerow(['Version:', results.experiment.version])
	writer.writerow(['Subject:', results.subject_id])
	writer.writerow(['Date:', datetime.date.today().strftime("%Y/%m/%d")])
	writer.writerow([''])
	writer.writerow(['Stimuli Presentation Order:'])
	writer.writerow(['ID','Label'])
	for stimulus in Stimulus.objects.filter(experiment=results.experiment):
		writer.writerow([stimulus.processingID,stimulus.label_text])
	writer.writerow([''])
	writer.writerow(['Subject Initial Preview:', results.preview_start_time])#js error stopping this todo
	writer.writerow(['Subject Experiment Start:', results.experiment_start_time])
	writer.writerow([''])

	writer.writerow(['Subject Actions:'])
	writer.writerow(['Time', 'ID', 'Label', 'From', 'To'])
	dict = eval(results.actions)
	#this is using mouse positions instead of peg position, will fix later todo
	for action in dict:
		writer.writerow([action['timeMoved'], action['ID'], action['label'], action['previousPosition'], action['currentPosition']])

	writer.writerow([''])

	writer.writerow(['Final Positions:'])
	writer.writerow(['ID', 'Label', 'Position'])
	dict = eval(results.final_positions)
	print dict
	for fp in dict:
		writer.writerow([fp['id'], fp['label'], fp['pos']])
	writer.writerow([''])

	writer.writerow(['Distances'])
	dict = eval(results.distances)
	writer.writerow(['Label'] + eval(results.order))#all labels
	for counter, l in enumerate(eval(results.order)):
		writer.writerow([l] + dict[counter])#label, x, y
	
	writer.writerow([''])

	writer.writerow(['Background Image Location:'])
	if results.experiment.board_image:
		writer.writerow([results.experiment.board_image.url])
	else:
		writer.writerow(['No Image'])
	writer.writerow([''])
	return response
