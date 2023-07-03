from django.contrib import admin

from users.models import Profile, EmailVerif
# Register your models here.

admin.site.register(Profile)


@admin.register(EmailVerif)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created']

    readonly_fields = ['created', ]