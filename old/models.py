from django.db import models

class Section(models.Model):
	name=models.CharField(max_length=30)
	order=models.IntegerField()

	def __unicode__(self):
		return self.name