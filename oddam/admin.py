from django.contrib import admin

# Register your models here.

from oddam.models import Category, Institution, Donation


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_editable = ['name']
#
#
# @admin.register(Institution)
# class InstitutionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'description', 'type')
#     list_editable = ('name', 'description', 'type')
#
#
# @admin.register(Donation)
# class DonationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'quantity', 'institution', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date',
#                     'pick_up_time', 'pick_up_comment', 'user')
#     list_editable = ('quantity', 'institution', 'address', 'phone_number', 'city', 'zip_code', 'pick_up_date',
#                      'pick_up_time', 'pick_up_comment')

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)