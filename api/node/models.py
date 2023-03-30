# 2023-03-07
# node/models.py

from django.db import models

from utils.model_abstracts import Model

class Node(Model):
    # Identification
    host        = models.URLField(null=False, blank=False, db_index=True, max_length=128, help_text='The host that the node is served from')
    username    = models.CharField(max_length=32, db_index=True, help_text='Username used for node-to-node communication')
    password    = models.CharField(max_length=64, help_text='Password used for node-to-node communication')
    api_path   = models.CharField(max_length=128, null=True, blank=True)
    display_name = models.CharField(max_length=128, default='')

    def __str__(self):
        return f'{self.host}'
