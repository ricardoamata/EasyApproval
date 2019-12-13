from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

import uuid

from usuario.models import Profile

class Curso(models.Model):
    ESTADOS = (
        (0, 'Planeación'),
        (1, 'En proceso de aprobación'),
        (2, 'Aprobado'),
        (3, 'Comenzado'),
        (4, 'Terminado'),
    )

    DATE_INPUT_FORMATS = ['%d-%m-%Y']

    hash_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    duracion = models.SmallIntegerField(null=True, blank=True)
    fecha_inicial = models.DateField(null=True, blank=True)
    fecha_final = models.DateField(null=True, blank=True)
    financiamiento = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    costo = models.FloatField(null=True, blank=True)
    aula = models.CharField(max_length=40, null=True, blank=True)
    #cupo = models.SmallIntegerField(null=True, blank=True)
    cupo_min = models.SmallIntegerField(null=True, blank=True)
    cupo_max = models.SmallIntegerField(null=True, blank=True)
    estado = models.SmallIntegerField(choices=ESTADOS, default=0)
    division = models.CharField(max_length=60, null=True, default="Ciencias exactas y naturales")
    departamento = models.CharField(max_length=40, null=True, default="Matematicas")
    caracter = models.CharField(max_length=150,default="")
    obj_general = models.TextField(null=True, blank=True)
    obj_particular = models.TextField(null=True, blank=True)
    contenido_sintetico = models.TextField(null=True, blank=True)
    estilo_enseñanza = models.TextField(null=True, blank=True)
    req_evaluacion = models.TextField(null=True, blank=True)
    bibliografia = models.TextField(null=True, blank=True)
    perfil_academico = models.TextField(null=True, blank=True)
    utilidad_programa = models.TextField(null=True, blank=True)
    experiencia = models.TextField(null=True, blank=True)
    hab_alumnos = models.TextField(null=True, blank=True)
    idioma =  models.CharField(max_length=50,null=True,blank=True)
    infraestructura= models.CharField(max_length=200,null=True,blank=True)
    cargo_instructor = models.CharField(max_length=50,null=True,blank=True)
    dependencia = models.CharField(max_length=50,null=True,blank=True)
    telefono = models.CharField(max_length = 15,null=True,blank=True)
    correo =  models.CharField(max_length = 35,null=True,blank=True)

    slug = models.SlugField(null=True, blank=True, default="")


    def __str__(self):
        return self.nombre

    @property
    def get_estado(self):
        return self.ESTADOS[int(self.estado)][1]

@receiver(pre_save, sender=Curso)
def create_slug(sender, instance, **kwargs):
    if instance.estado == 2 and instance.slug == None:
        print("paso el if")
        instance.slug = slugify(instance.nombre)
        repeat = 0

        while Curso.objects.filter(slug=instance.slug).count():
            repeat += 1
            instance.slug = slugify(instance.nombre + " " + str(repeat))

class Inscripcion(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='constancias/', null=True, blank=True)
    calificacionCurso = models.IntegerField(null=True, blank=True)
    sugerenciaCurso = models.TextField(null=True, blank=True)
    calificacionInstructor = models.IntegerField(null=True, blank=True)
    sugerenciaInstructor = models.TextField(null=True, blank=True)
    calficacion_curso = models.PositiveSmallIntegerField(null=True, blank=True)
