import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from agrijeune.base_enum import ExtendedEnum
from agrijeune.constants import USER_IMAGE_PATH
from agrijeune.validators import validate_image_extension, valideta_image_size
# Create your models here.


class GenderEnums(ExtendedEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class ProfileTypeEnums(ExtendedEnum):
    AGRIPRENEUR = "AGRIPRENEUR"
    MERCHANT = "MERCHANT"
    CLIENT = "CLIENT"
    USER = "USER"


class User(AbstractUser):
    PROFIL_TYPE = (
        (ProfileTypeEnums.AGRIPRENEUR.value, 'AGRIPRENEUR'),
        (ProfileTypeEnums.MERCHANT.value, 'MERCHANT'),
        (ProfileTypeEnums.CLIENT.value, 'CLIENT'),
        (ProfileTypeEnums.USER.value, 'USER')
    )
    GENDER = (
        (GenderEnums.MALE.value, 'MALE'),
        (GenderEnums.FEMALE.value, 'FEMALE')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.FileField(
        upload_to = USER_IMAGE_PATH, 
        verbose_name = 'photo de profil',
        blank = True,
        null = True,
        validators=[valideta_image_size, validate_image_extension]
    )
    email = models.EmailField(max_length=225, unique=True)
    venndor_authorized = models.BooleanField(default=False, verbose_name='vendeur autorisé  ?', editable=True)
    profil_type = models.CharField(max_length=255, verbose_name='type de profil', default=ProfileTypeEnums.USER.value)
    gender = models.CharField(max_length=255, verbose_name='sexe', null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=150, null=True, blank=True)


    def is_vendor(self):
        return self.profil_type in ["agripreneur", "commerçant", "AGRIPRENEUR", "MERCHANT"]
    
    def is_client(self):
        return self.profil_type in ["client", "user", "CLIENT", "USER"]
    
    def __str__(self):
        return self.email