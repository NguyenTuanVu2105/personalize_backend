from HUB.models.random_id_model import RandomIDModel
from django.db import models

class AdminImageUploaded(RandomIDModel):
    name = models.CharField(max_length=100)
    file_url = models.TextField()
    is_public = models.BooleanField(default=True, db_index=True)
    path = models.TextField(null=True, blank=True)
    path_dir = models.TextField(null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = 'admin_image_uploaded'
        ordering = ['create_time']

