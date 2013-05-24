import os, re, string
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from profiles.utils import to_alphanumeric
from profiles.storage import OverwriteFileSystemStorage

class ModelWithSlugBase(models.Model):
    slug = models.CharField(max_length=8, editable=False, blank=True)
    
    offset = 0
    
    def generate_slug(self):
        integer = self.id + self.offset 
        return to_alphanumeric(integer)
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # Call the "real" save() method.
        super(ModelWithSlugBase, self).save(force_insert, force_update, *args, **kwargs)
        self.slug = self.generate_slug()
        # Call the "real" save() method to update slug field only.
        super(ModelWithSlugBase, self).save(update_fields=['slug'])
        
    class Meta:
        abstract = True

# PROFILES_ICON_UPLOAD_FOLDER requires trailing slash
ICON_UPLOAD_FOLDER = getattr(settings, 'PROFILES_ICON_UPLOAD_FOLDER', 'usericons/')

def usericon_path(instance, filename):
    root, ext = os.path.splitext(filename)
    return "%s%s%s" % (ICON_UPLOAD_FOLDER, instance.slug, ext)

class ContribUserProfileManager(UserManager):
    def get_query_set(self):
        return super(ContribUserProfileManager, self).get_query_set().filter(
                                                    is_contributor=True)

class NonContribUserProfileManager(UserManager):
    def get_query_set(self):
        return super(NonContribUserProfileManager, self).get_query_set().filter(
                                                    is_contributor=False)

class CustomUser(ModelWithSlugBase, AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=30, unique=True,
        help_text='Required. 30 characters or fewer. Letters, numbers and '
                    '/./-/_ characters',
        validators=[
            validators.RegexValidator(re.compile('^[\w.-]+$'), 'Enter a valid username.', 'invalid')
        ])
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    email = models.EmailField('email address', max_length=254, unique=True)
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    icon = models.ImageField(storage=OverwriteFileSystemStorage(), upload_to=usericon_path)
    bio = models.TextField(validators=[validators.MaxLengthValidator(500)], blank=True)
    is_contributor = models.BooleanField(default=True, editable=False)
    
    offset = 3900000000000
 
    objects = ContribUserProfileManager()
    non_contribs = NonContribUserProfileManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-user__username']
    
    def __unicode__(self):
        return "Profile for %s" % self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={ 'username': self.username })
