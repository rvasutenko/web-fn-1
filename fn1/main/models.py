from django.db import models
from collections import defaultdict


class News(models.Model):
    image = models.ImageField(verbose_name="Изображение новость", upload_to="news/images/")
    heading = models.CharField(verbose_name="Заголовок", max_length=50)
    text = models.CharField(verbose_name="Текст", max_length=200)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
    
    def __str__(self):
        return self.heading
    


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"

    def __str__(self):
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name

class MaterialType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Тип материала"
        verbose_name_plural = "Типы материала"

    def __str__(self):
        return self.name


class MaterialManager(models.Manager):
    def grouped(self, include_fn1=True, exclude_fn1=False):
        qs = (
            self.get_queryset()
            .select_related("discipline", "material_type")
            .order_by("semester", "discipline__name")
        )

        data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for material in qs:
            faculty_names = [f.name for f in material.faculties.all()]
            if exclude_fn1 and "ФН1" in faculty_names:
                continue
            if not include_fn1 and "ФН1" in faculty_names:
                continue

            semester = material.semester
            discipline_name = material.discipline.name
            type = material.material_type.name

            data[semester][discipline_name][type].append({
                "title": material.title,
                "url": material.file.url if material.file else None,
            })

        return data

    def for_fn1(self):
        
        return self.grouped(include_fn1=True, exclude_fn1=False)

    def for_other_faculties(self):
        return self.grouped(include_fn1=False, exclude_fn1=True)


class Material(models.Model):
    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    semester = models.PositiveSmallIntegerField(null=True)
    faculties = models.ManyToManyField(Faculty, related_name="disciplines")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name="materials", null=True)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(verbose_name="Файл материалы", upload_to="materials/", null=True, blank=True)

    objects = MaterialManager()

    def __str__(self):
        return self.title or f"{self.material_type.name} ({self.discipline}, семестр {self.semester})"
