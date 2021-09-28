from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Employee(models.Model):
    """Modelo Employee"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    Photo = models.ImageField(
        upload_to='pictures/%y/%m/%d',
        default='pictures/default.jpg',
        max_length=255
    )
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicionales del modelo Employee"""
        db_table = 'Employee'

class Role(models.Model):
    """Modelo Role de Usuario"""
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicionales del modelo Role"""
        db_table = 'Role'

class CustomUser(models.Model):
    """ Modelo Usuario """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(('Correo electronico'), unique=True)
    #first_name = None
    #last_name = None
    #is_staff = None
    #is_superuser = None
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    def __str__(self):
        return self.email

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicioneles del modelo Usuario"""
        db_table = 'CustomUser'