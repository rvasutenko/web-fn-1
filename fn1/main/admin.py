from django.contrib import admin
from .models import Material, MaterialType, Course, Discipline, Faculty, News

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_faculties")
    list_filter = ("faculties",)
    search_fields = ("name",)

    def get_faculties(self, obj):
        return ", ".join([f.name for f in obj.faculties.all()])
    get_faculties.short_description = "Факультеты"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "semester", "discipline")
    list_filter = ("semester", "discipline__faculties")
    search_fields = ("discipline__name",)

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "material_type", "file")
    list_filter = ("course__discipline__faculties", "course__semester", "material_type")
    search_fields = ("title",)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "heading", "text", "image")
    search_fields = ("heading", "text")
