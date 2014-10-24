from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from forumapp.models import *



class ProfileInline(admin.StackedInline):
    model = UserProfile
    #fk_name = 'user'
    max_num = 1
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# our porject

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class ThreadAdmin(admin.ModelAdmin):
    
    inlines = [CommentInline]



admin.site.register(Category)
admin.site.register(Thread,ThreadAdmin)
admin.site.register(Comment)
admin.site.register(Subject)
admin.site.register(Review)
admin.site.register(Document)
admin.site.register(Video)

