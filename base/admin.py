from django.contrib import admin

# Register your models here.

from .models import Dosen,Review,Fakultas,DosenGrade

admin.site.register(Dosen)
admin.site.register(Review)
admin.site.register(Fakultas)
admin.site.register(DosenGrade)
