from django.contrib import admin
from .models import Material, MaterialType, Discipline, Faculty, News, ProjectParagraph, Project, Paragraph

from django.contrib.auth.models import User, Group
from django import forms

admin.site.unregister(User)
admin.site.unregister(Group)


class ProjectParagraphInline(admin.TabularInline):
    model = ProjectParagraph
    extra = 1
    autocomplete_fields = ("paragraph",)



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_visible")
    list_filter = ("is_visible",)
    search_fields = ("title",)
    inlines = (ProjectParagraphInline,)



@admin.register(Paragraph)
class ParagraphAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "type",
        "is_visible",
    )
    list_filter = (
        "type",
        "is_visible",
    )
    search_fields = (
        "title",
        "text",
    )


class MaterialAdminForm(forms.ModelForm):
    FACULTY_CHOICES = [
        ("fn1", "ФН1"),
        ("others", "Другие факультеты"),
    ]
    faculty_group = forms.ChoiceField(choices=FACULTY_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Material
        exclude = ("faculties",) 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.faculties.filter(name="ФН1").exists():
                self.fields["faculty_group"].initial = "fn1"
            else:
                self.fields["faculty_group"].initial = "others"


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save() 

        choice = self.cleaned_data["faculty_group"]
        if choice == "fn1":
            faculties = Faculty.objects.filter(name="ФН1")
        else:
            faculties = Faculty.objects.exclude(name="ФН1")

        instance.faculties.set(faculties)  # заменяем M2M связи
        return instance


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    form = MaterialAdminForm
    list_display = ("id", "title", "discipline", "semester", "material_type", "file")
    list_filter = ("discipline", "semester", "material_type")
    search_fields = ("title", "discipline__name")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "heading", "text", "image")
    search_fields = ("heading", "text")
