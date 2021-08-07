from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = "__all__"
    readonly_fields = ('id', 'username', 'date_joined')
    search_fields = ['username']


def save_model(self, request, obj, form, change):
    for attr, value in form.cleaned_data.items():
        if attr == 'password':
            form.instance.set_password(form.cleaned_data['password'])
    form.save()
    return form
