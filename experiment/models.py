from django.db import models

class Color(models.Model):
	red=models.IntegerField()
	green=models.IntegerField()
	blue=models.IntegerField()

	def __unicode__(self):
		return u'(%s, %s, %s)' % (self.red,self.green,self.blue)

class Experiment(models.Model):
	name=models.CharField(max_length=30)
	version=models.CharField(max_length=30)
	board_image=models.ImageField(upload_to='board_image',null=True,blank=True)
	show_stimulus_relative_size=models.BooleanField(default=False)
	window_x=models.IntegerField()
	window_y=models.IntegerField()

	def __unicode__(self):
		return u'%s' % (self.name)

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

class Preview(models.Model):
	board_color=models.ForeignKey(Color, related_name="board_color")
	background_color=models.ForeignKey(Color, related_name="background_color")
	show_label=models.BooleanField(default=True)
	position=models.IntegerField()
	shade=models.IntegerField()
	size=models.IntegerField()

class Order(models.Model):
	experiment=models.ForeignKey(Experiment, related_name="experiment_order")
	name=models.CharField(max_length=30)

	def __unicode__(self):
		return u'%s' % (self.name)

class OrderItem(models.Model):
	order=models.ForeignKey(Order, related_name="order")
	stimulus=models.ForeignKey(Stimulus,related_name="stimulus")

