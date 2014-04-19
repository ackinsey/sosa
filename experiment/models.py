from django.db import models
import datetime


"""The Color class was built to reduce the number of variables and also increase the readibility of other classes.

    Attributes:
        red: The red value (0-255) of the color.
        green: The red value (0-255) of the color.
        blue: The red value (0-255) of the color.
"""
class Color(models.Model):
	red=models.IntegerField()
	green=models.IntegerField()
	blue=models.IntegerField()

	def __unicode__(self):
		return u'(%s, %s, %s)' % (self.red,self.green,self.blue)

"""The Experiment class contains the main data relating to an experiment. 

    Attributes:
		name: The experiments name.
		version: The experiments version.
		board_image: The image associated with the experiment's board
		show_stimulus_relative_size: If true the stimulus will be displayed at a size relative to the board in the experiment window.
		window_x: The width value (in pixels) of the experiment's board.
		window_y: The height value (in pixels) of the experiment's board.
"""
class Experiment(models.Model):
	name=models.CharField(max_length=30)
	version=models.CharField(max_length=30)
	board_image=models.ImageField(upload_to='board_image',null=True,blank=True)
	show_stimulus_relative_size=models.BooleanField(default=False)
	window_x=models.IntegerField()
	window_y=models.IntegerField()

	def __unicode__(self):
		return u'%s' % (self.name)

"""The Stimulus class stores all data related to a given stimulus. It also includes data relating to where stimulus information (such as label) will be displayed.

    Attributes:
		experiment: A ForeignKey linking the stimulus to its parent experiment.
		form_id: Used for tracking the stimulus on the create page and once it's passed to the server. Not used for the experiment.
		label_text: The text that is displayed above the stimulus.
		processingID: ID created with the stimulus, it's displayed in the exported CSV after the completion of the experiment.
		image: Stimulus image, not required unless the is_peg option is False.
		label_color: A ForeignKey to the color of the 'label_text'
		peg_color: A ForeignKey to the color of the 'peg_color'
		is_peg: A Boolean value that toggles whether a peg image is displayed or a user uploaded image.
		peg_size: A list of options to scale the peg. Doesn't affect image settings.
		image_size: The amount of scaling applied to an image. Can be in the range (.5-2.0).
"""
class Stimulus(models.Model):
	experiment=models.ForeignKey(Experiment, related_name="experiment_stimulus")
	form_id=models.IntegerField(help_text="Do not modify")
	label_text=models.CharField(max_length=30)
	processingID=models.CharField(max_length=30)
	image=models.ImageField(upload_to="peg_image",null=True,blank=True)
	label_color=models.ForeignKey(Color, related_name="label_color")
	peg_color=models.ForeignKey(Color, related_name="peg_color",null=True,blank=True)
	is_peg=models.BooleanField(default=True)
	peg_size=models.CharField(max_length=30,null=True,blank=True)
	image_size=models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)

	def __unicode__(self):
		return u'%s' %(self.label_text)
	    
"""The Preview class attachs to the Experiment class and allows the settings to be able modified before each experiment. The Preview can also be loaded at runtime to expedite the experiment process.

    Attributes:
		name: The preview name. Useful for identifying which Preview you are loading when using the Import functionality on the Preview Page.
		board_color:A ForeignKey to the color of the 'board_color.' Currently not implemented.
		background_color: A ForeignKey to the color of the 'background_color.' Changes the background color behind the board image.
		show_label: If False then labels will not be displayed.
		position: Adjusts the Y-axis positioning of the lablel text above the stimulus.
		shade: The shade (from 0-100) that will darken the font color.
		size: The fontsize of the label text.
		hide_background: If true the background image will not be displayed during the experiment.
"""
class Preview(models.Model):
	name=models.CharField(max_length=80, default="Preview")
	board_color=models.ForeignKey(Color, related_name="board_color")
	background_color=models.ForeignKey(Color, related_name="background_color")
	show_label=models.BooleanField(default=True)
	position=models.IntegerField()
	shade=models.IntegerField()
	size=models.IntegerField()
	hide_background=models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s' % (self.name)

"""The Order class represents an order of stimulus display that the experimenter can set for an experiment. The experimenter can create as many different orders as they want to display stimulus in different orders to the subject.

    Attributes:
		experiment: A ForeignKey to the 'Experiment' that the order is associated with.
		name: The name of the order.
"""
class Order(models.Model):
	experiment=models.ForeignKey(Experiment, related_name="experiment_order")
	name=models.CharField(max_length=30)

	def __unicode__(self):
		return u'%s' % (self.name)

"""The OrderItem serves as a link between the Stimulus and the Order. It allows for the simplest way to link the same Stimulus to many different Orders.

    Attributes:
    	order: A ForeignKey to the 'Order' that the OrderItem is associated with.
		stimulus: A ForeignKey to the 'Stimulus' that the OrderItem is linking to.
"""
class OrderItem(models.Model):
	order=models.ForeignKey(Order, related_name="order")
	stimulus=models.ForeignKey(Stimulus,related_name="stimulus")

"""The Results class is used to take all of data from a completed experiment and transer it to the view that will compile it into the CSV.

    Attributes:
		date: Date the experiment was taken on.
		experiment: The experiment that the results data represents.
		preview_start_time: The time when the subject reaches the view_stimuli page.
		experiment_start_time: The time when the subject starts the experiment.
		experiment_end_time: The time when the subjects clicks the submit button to complete the experiment.
		actions: A dictionary (String) of every stimulus move the subject made.
		final_positions: The final positions of all of the stimulus.
		distances: Stores the distances between the final positions of all of the stimulus.
		background_image_location: The background image's server location (if it exists)
		subject_id: The ID provided by the subject at the view_stimuli page. Used for tracking who took the experiment in the CSV file.
		order: Identifies the chosen order for the experiment.
"""
class Results(models.Model):
	date=models.DateTimeField(default=datetime.datetime.now())
	experiment=models.ForeignKey(Experiment, related_name="experiment_results")
	preview_start_time=models.CharField(max_length=50)
	experiment_start_time=models.CharField(max_length=50)
	experiment_end_time=models.CharField(max_length=50)
	actions=models.TextField(max_length=200)
	final_positions=models.TextField(max_length=200)
	distances=models.TextField(max_length=200)
	background_image_location=models.CharField(max_length=200)
	subject_id=models.CharField(null=True, max_length=50)
	order=models.CharField(max_length=200)

	def __unicode__(self):
		return "subject: %s, experiment: %s"% (self.subject_id, self.experiment)