from django.db import models

class Color(models.Model):
	red=models.IntegerField()
	green=models.IntegerField()
	blue=models.IntegerField()

class Experiment(models.Model):
	name=models.CharField(max_length=30)
	version=models.CharField(max_length=30)
	board_image=models.ImageField(upload_to='peg_image')
	window_x=models.IntegerField()
	window_y=models.IntegerField()


class Peg(models.Model):
	label_text=models.CharField(max_length=30)
	processingID=models.CharField(max_length=30)
	image=models.ImageField(upload_to='peg_image')
	label_color=models.ForeignKey(Color, related_name="label_color")
	peg_color=models.ForeignKey(Color, related_name="peg_color")
	is_peg=models.BooleanField(default=True)


class Preview(models.Model):
	board_color=models.ForeignKey(Color, related_name="board_color")
	background_color=models.ForeignKey(Color, related_name="background_color")
	show_label=models.BooleanField(default=True)
	position=models.IntegerField()
	shade=models.IntegerField()
	size=models.IntegerField()
