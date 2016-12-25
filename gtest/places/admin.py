from django.contrib import admin

# Register your models here.
from .models import User
from .models import Guide
from .models import Country
from .models import City

admin.site.register(User)
admin.site.register(Guide)
admin.site.register(Country)
admin.site.register(City)

