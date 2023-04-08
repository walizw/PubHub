from django.contrib import admin
from .models import ActivityUser, Activity, DiscoveredInstances

# Register your models here.
admin.site.register(ActivityUser)
admin.site.register(Activity)
admin.site.register(DiscoveredInstances)
