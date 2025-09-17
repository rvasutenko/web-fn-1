from django.db import models
from collections import defaultdict


class News(models.Model):
    image = models.ImageField(verbose_name="Изображение новость", upload_to="news/images/")
    heading = models.CharField(verbose_name="Заголовок", max_length=50)
    text = models.CharField(verbose_name="Текст", max_length=200)

    def __str__(self):
        return self.heading


class Faculty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=255)
    faculties = models.ManyToManyField(Faculty, related_name="disciplines")

    def __str__(self):
        return self.name


class Course(models.Model):
    semester = models.PositiveSmallIntegerField(null=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.discipline.name} (семестр {self.semester})"


class MaterialType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MaterialManager(models.Manager):
    def grouped(self, include_fn1=True, exclude_fn1=False):
        """
        Вернёт словарь:
        {
            1: { 'Математический анализ': [ {type, title, url}, ... ], ... },
            2: { 'Физика': [...], ... }
        }
        """

        qs = (
            self.get_queryset()
            .select_related("course__discipline", "course", "material_type")
            .order_by("course__semester", "course__discipline__name")
        )

        data = defaultdict(lambda: defaultdict(list))

        for material in qs:
            # исключение ФН1
            faculty_names = [f.name for f in material.course.discipline.faculties.all()]
            if exclude_fn1 and "ФН1" in faculty_names:
                continue
            if not include_fn1 and "ФН1" in faculty_names:
                continue

            semester = material.course.semester
            discipline_name = material.course.discipline.name

            data[semester][discipline_name].append({
                "type": material.material_type.name,
                "title": material.title,
                "url": material.file.url if material.file else None,
            })

        return data

    def for_fn1(self):
        return self.grouped(include_fn1=True, exclude_fn1=False)

    def for_other_faculties(self):
        return self.grouped(include_fn1=False, exclude_fn1=True)


class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(verbose_name="Файл материалы", upload_to="materials/", null=True, blank=True)

    objects = MaterialManager()

    def __str__(self):
        return self.title or f"{self.material_type.name} ({self.course})"
