from import_export import resources

from app.models import Comment


class CommentResource(resources.ModelResource):

    class Meta:
        model = Comment
        # fields = ('text', )  # default all
