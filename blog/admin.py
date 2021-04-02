from django.contrib import admin
from .models import Post,BlogComment,User,Category
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'POSTS',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'posts',
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register( BlogComment)
admin.site.register( Category)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author','timeStamp')
    list_filter = ('timeStamp','author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'timeStamp'
    ordering = ('timeStamp',)
    class Media:
        js= ('tinyInject.js',)