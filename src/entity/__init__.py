from pymodm import MongoModel, fields
from pymodm.manager import Manager
from pymodm.queryset import QuerySet


class PostQuerySet(QuerySet):
    def posts_by_user(self, user_id):
        return self.raw({'ref_user': user_id})


class CommentQuerySet(QuerySet):
    def comments_by_post(self, post_id):
        return self.raw({'ref_post': post_id})


class User(MongoModel):
    username = fields.CharField()

    def get_posts(self):
        return list(Post.manager.posts_by_user(self._id))


class Post(MongoModel):
    ref_user = fields.ReferenceField(User)

    # Override full_clean by pass exclude to super,
    # so that the reference field will not be checked in clean()
    def full_clean(self, exclude=None):
        super().full_clean(exclude=['ref_user'])

    # All queries must be executed via this_manger
    manager = Manager.from_queryset(PostQuerySet)()

    def get_comments(self):
        return list(Comment.manager.comments_by_post(self._id))

    class Meta:
        # Important for cascade saving
        cascade = True


class Comment(MongoModel):
    ref_post = fields.ReferenceField(Post)

    def full_clean(self, exclude=None):
        super().full_clean(exclude=['ref_post'])

    # All queries must be executed via this_manger
    manager = Manager.from_queryset(CommentQuerySet)()

    class Meta:
        cascade = True
