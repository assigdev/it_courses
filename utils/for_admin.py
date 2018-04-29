from django.contrib import admin


class PrepopulatedSlug(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
