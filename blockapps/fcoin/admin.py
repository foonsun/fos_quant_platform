from django.contrib import admin
from djcom.utils import registerAdminFromModels
from . import models 
from djcom.admin_perms import PermModelAdmin

registerAdminFromModels(models)
