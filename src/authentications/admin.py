from django.contrib import admin

# Register your models here.

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "profil_type",
        "gender",
        "venndor_authorized",
    ]
    search_fields = ["email"]
    list_editable = ('venndor_authorized',)










admin.site.site_header = "Administration d'Agri-Jeune"                    # default: "Django Administration"
#admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = "Admin" # default: "Django site admin"