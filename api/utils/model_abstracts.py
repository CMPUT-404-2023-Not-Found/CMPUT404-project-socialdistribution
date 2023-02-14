# 
# This code came from a video tutorial from Bobby Stearman on 2022-11-28 retrieved on 2023-02-12, to Youtube freeCodeCamp.org
# video here:
# https://www.youtube.com/watch?v=tujhGdn1EMI
# 

import uuid
from django.db import models

class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True