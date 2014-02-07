from django.contrib import admin
from experiment.models import Color,Experiment,Stimulus,Preview,Order,OrderItem

admin.site.register(Color)
admin.site.register(Experiment)
admin.site.register(Stimulus)
admin.site.register(Preview)
admin.site.register(Order)
admin.site.register(OrderItem)