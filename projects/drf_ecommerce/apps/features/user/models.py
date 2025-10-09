# py
# django
from django.db import models # type: ignore
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # type: ignore
# third
# own
from apps.core.models import BaseModels, DocumentTypes
from apps.shared.models import Countries, Cities

# Create your models here.

class UsersManager(BaseUserManager):
    def _create_user(self, username, email, name, lastname, document_type, document, phone, rol, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            name = name,
            lastname = lastname,
            document_type = document_type,
            document = document,
            phone = phone,
            rol = rol,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        if password not in [None, '']:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, name, lastname, document_type, document, phone, rol, password=None, is_staff=False, is_superuser=False, **extra_fields):
        return self._create_user(username, email, name, lastname, document_type, document, phone, rol, password, is_staff, is_superuser, **extra_fields)

    def create_superuser(self, username, email, name, lastname, document_type=None, document=None, phone=None, rol=None, password=None, is_staff=True, is_superuser=True, **extra_fields):
        return self._create_user(username, email, name, lastname, document_type, document, phone, rol, password, is_staff, is_superuser, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class Roles(BaseModels):
    """Model definition for Roles."""

    # TODO: Define fields here
    code = models.CharField('Code', max_length=50, unique=True)  # Ej: ADMIN, SELLER, SUPERVISOR
    name = models.CharField('Name', max_length=100)              # Nombre legible: "Administrador"
    description = models.TextField('Description', null=True, blank=True)

    class Meta:
        """Meta definition for Roles."""
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Roles."""
        return f"{self.code} - {self.name}"


class Users(AbstractBaseUser, PermissionsMixin, BaseModels):
    """Model definition for Users."""

    # TODO: Define fields here
    username = models.CharField('Username', unique=True, max_length=255)
    email = models.EmailField('Email', unique=True, max_length=255)
    name = models.CharField('Name', max_length=150, blank=True, null=True)
    lastname = models.CharField('Lastname', max_length=150, blank=True, null=True)
    document_type = models.ForeignKey(DocumentTypes, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Document Type')
    document = models.CharField('Document Number', max_length=20, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='user/profile/image/', blank=True, null=True, verbose_name='Image')
    is_staff = models.BooleanField('Is Staff', default=False)
    phone = models.CharField('Phone Number', max_length=15, null=True, blank=True)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Role')
    country = models.ForeignKey(
        Countries,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Country"
    )
    city = models.ForeignKey(
        Cities,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="City"
    )
    objects = UsersManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'lastname']

    class Meta:
        """Meta definition for Users."""
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']
    
    def natural_key(self):
        return (self.username,)

    def __str__(self):
        """Unicode representation of Users."""
        return self.username

    def save(self, *args, **kwargs):
        if self.pk:
            # Si es una actualización, verificamos si cambió la contraseña
            old = Users.objects.filter(pk=self.pk).first()
            if old and old.password != self.password and not self.password.startswith('pbkdf2_sha256$'):
                self.set_password(self.password)
        else:
            # Usuario nuevo, se asegura que la contraseña esté hasheada
            if self.password and not self.password.startswith('pbkdf2_sha256$'):
                self.set_password(self.password)
        super().save(*args, **kwargs)

class Fingerprints(BaseModels):
    """Model definition for Fingerprints."""
    
    FINGER_CHOICES = [
        ('left_thumb', 'Pulgar izquierdo'),
        ('left_index', 'Índice izquierdo'),
        ('left_middle', 'Medio izquierdo'),
        ('left_ring', 'Anular izquierdo'),
        ('left_little', 'Meñique izquierdo'),
        ('right_thumb', 'Pulgar derecho'),
        ('right_index', 'Índice derecho'),
        ('right_middle', 'Medio derecho'),
        ('right_ring', 'Anular derecho'),
        ('right_little', 'Meñique derecho'),
    ]

    # TODO: Define fields here
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='fingerprints',
        verbose_name='User'
    )
    finger = models.CharField(
        max_length=20,
        choices=FINGER_CHOICES,
        verbose_name="Finger"
    )
    template = models.BinaryField(
        verbose_name="Plantilla biométrica",
        help_text="Datos binarios del patrón extraído del lector"
    )
    device_serial_number = models.CharField('Device Serial Number', max_length=100, blank=True, null=True)

    class Meta:
        """Meta definition for Fingerprints."""

        verbose_name = 'Fingerprint'
        verbose_name_plural = 'Fingerprints'
        unique_together = ('user', 'finger')

    def __str__(self):
        """Unicode representation of Fingerprints."""
        return f"{self.user.username} - {self.get_finger_display()}"

class AccessLogs(BaseModels):
    """Model definition for AccessLogs."""
    
    ACCESS_TYPE = [
        ('entry', 'Entrada'),
        ('exit', 'Salida'),
    ]

    # TODO: Define fields here
    user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs',
        verbose_name="User"
    )
    fingerprint = models.ForeignKey(
        Fingerprints,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs',
        verbose_name="Huella usada"
    )
    device_serial_number = models.CharField(
        max_length=100,
        verbose_name="Dispositivo lector",
        help_text="Número de serie o identificador del lector que registró el acceso."
    )
    verified = models.BooleanField(
        default=False,
        verbose_name="Huella verificada"
    )
    access_type = models.CharField(
        max_length=10,
        choices=ACCESS_TYPE,
        default='entry',
        verbose_name="Tipo de acceso"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y hora del acceso"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas o detalles"
    )

    class Meta:
        """Meta definition for AccessLogs."""

        verbose_name = 'AccessLog'
        verbose_name_plural = 'AccessLogs'
        ordering = ['-timestamp']

    def __str__(self):
        """Unicode representation of AccessLogs."""
        user = self.user.username if self.user else "Desconocido"
        type = "Entrada" if self.access_type == "entry" else "Salida"
        state = "Éxito" if self.verified else "Error"
        return f"({state}) {user} - {type} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"