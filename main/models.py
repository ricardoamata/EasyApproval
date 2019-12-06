from django.db import models

class Instructor(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    institucion = models.CharField(max_length=40)
    cv = models.FileField()

class Curso(models.Model):
    ESTADOS = (
        (0, 'Planeación'),
        (1, 'En proceso de aprobación'),
        (2, 'Aprobado'),
        (3, 'No aprobado'),
        (4, 'En proceso de impartición'),
        (5, 'Terminado'),
    )

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=40, null=True, blank=True)
    duracion = models.DurationField(null=True, blank=True)
    fecha_inicial = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    financiamiento = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    costo = models.FloatField(null=True, blank=True)
    aula = models.CharField(max_length=20, null=True, blank=True)
    cupo = models.SmallIntegerField(null=True, blank=True)
    estado = models.SmallIntegerField(max_length=6, null=True, blank=True, choices=ESTADOS)

class Alumno(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    institucion = models.CharField(max_length=40)
    cursos = models.ManyToManyField(Curso)


