from django.contrib import admin
from django.utils import timezone
from django.db.models import Count
from django_summernote.admin import SummernoteModelAdmin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import DateTimeRangeFilter
# from leaflet.admin import LeafletGeoAdmin
from import_export.admin import ImportExportModelAdmin

from app.models import Blog, Comment, Category, Place
from app.resources import CommentResource


class CommentInline(admin.TabularInline):  # another options is admin.StackedInline; changes the display design

    model = Comment
    fields = ('text', 'is_active')
    extra = 0  # default 3; amount of empty boxes for new comments
    classes = ('collapse', )  # custom css classes


class BlogAdmin(SummernoteModelAdmin):

    list_display = ('title', 'date_created', 'last_modified', 'is_draft', 'days_since_creation', 'edited_today',
                    'number_of_comments')
    list_filter = (
        'is_draft',
        ('date_created', DateTimeRangeFilter),
    )
    ordering = ('title', '-date_created')  # add - for descending order
    search_fields = ('title', )  # case insensitive
    prepopulated_fields = {'slug': ('title',)}  # slug field will be prepopulated with the value from title field
    list_per_page = 50  # amount of results per page; default is 100
    actions = ('set_blogs_to_published', )
    date_hierarchy = 'date_created'
    # fields = (('title', 'slug'), 'body', 'is_draft')  # can also be used to change order of displayed fields
    # you can either have fields or fieldsets in admin class
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'body'),
        }),
        ('Advanced options', {
            'fields': ('is_draft', 'categories'),
            'description': 'Options to configure blog creation',
            'classes': ('collapse',),  # add custom css classes
        })
    )
    summernote_fields = ('body',)
    inlines = (CommentInline, )
    filter_horizontal = ('categories', )

    def get_actions(self, request):
        """
        Disable 'delete selected' action from dashboard
        """
        actions = super().get_actions(request)
        try:
            del actions['delete_selected']
        except KeyError:
            pass
        return actions

    def has_delete_permission(self, request, obj=None):
        """
        Remove permission to delete objects for all users
        """
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comments_count=Count('comments'))
        return queryset

    def number_of_comments(self, blog):
        return blog.comments_count

    def edited_today(self, blog):
        return timezone.now().date() == blog.last_modified.date()

    def get_ordering(self, request):  # custom ordering based on user (use this instead of "ordering" attribute
        if request.user.is_superuser:
            return ('title', '-date_created')
        return ('title',)

    def set_blogs_to_published(self, request, queryset):
        count = queryset.update(is_draft=False)
        self.message_user(request, f'{count}  blogs have been published successfully.')

    set_blogs_to_published.short_description = 'Mark selected blogs as published'  # display name in the dropdown
    edited_today.short_description = 'Changed today'  # change display name of the column
    number_of_comments.admin_order_field = 'comments_count'


class CommentAdmin(ImportExportModelAdmin):
    list_display = ('blog', 'text', 'date_created', 'is_active', )
    list_editable = ('is_active', )  # fields that are editable in list display
    list_filter = (
        ('blog', RelatedDropdownFilter),
    )
    resource_class = CommentResource
    list_select_related = True  # reduces number of db queries for foreign keys
    # list_select_related = ('blog', )  # can also be a tuple of fields
    raw_id_fields = ('blog', )  # changes dropdown for foreign field into search field for more complex lookup


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
# admin.site.register(Place, LeafletGeoAdmin)
