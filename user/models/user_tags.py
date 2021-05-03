from django.db.models import ForeignKey, CASCADE, CharField, DateTimeField

from HUB.models.random_id_model import RandomIDModel
from user.models import User


class UserTag(RandomIDModel):
    user = ForeignKey(to=User, related_name='tags', on_delete=CASCADE)
    tag = CharField(max_length=255)

    create_time = DateTimeField(auto_now_add=True)
    update_time = DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_user_tags'
        ordering = ['id']
