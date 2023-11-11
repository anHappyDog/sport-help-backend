from django.contrib import admin
from .models import User,Sport,SportRecord,Team,Article
# Register your models here.
admin.site.register(User)
admin.site.register(Sport)
admin.site.register(SportRecord)
admin.site.register(Team)
admin.site.register(Article)