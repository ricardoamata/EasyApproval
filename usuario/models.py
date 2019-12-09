from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    TIPOS = (
        (0, 'ALUMNO'),
        (1, 'INSTRUCTOR'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institucion = models.CharField(max_length=40, blank=True)
    tipo = models.SmallIntegerField(choices=TIPOS, null=True, blank=True)
    numero_borradores = models.IntegerField(default=0)
    cv = models.FileField(null=True, blank=True)

    @property
    def nombre(self):
        return self.user.first_name

    @property
    def apellido(self):
        return self.user.last_name

    def __str__(self):
        return str(self.nombre) + (" " + str(self.apellido) if self.apellido != None else "")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
