from django.contrib import admin
from .models import ActivityUser, Activity, DiscoveredInstances, Note

# Register your models here.
admin.site.register(ActivityUser)
admin.site.register(Activity)
admin.site.register(DiscoveredInstances)
admin.site.register(Note)
