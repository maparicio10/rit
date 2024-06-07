from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import OfficerCreationForm, OfficerChangeForm
from core.models import Person, Officer, Vehicle, Violation

# Register your models here.
admin.site.site_title = "Infracciones de tránsito"
admin.site.site_header = "Infracciones de tránsito"


# admin.site.register([Person, Officer, Vehicle, Violation])
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('display_fullname', 'email')

    def display_fullname(self, obj):
        return obj.fullname

    display_fullname.short_description = 'Nombre Completo'


@admin.register(Officer)
class OfficerAdmin(UserAdmin):
    add_form = OfficerCreationForm
    form = OfficerChangeForm
    model = Officer
    list_display = ('display_fullname', 'identification_number')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name', 'last_name', 'email'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'identification_number')

    def display_fullname(self, obj):
        return obj.fullname

    display_fullname.short_description = 'Nombre Completo'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand', 'color', 'person')


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'vehicle', 'officer')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True
