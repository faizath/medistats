from django.db import models

class medistatsData(models.Model):
    username = models.CharField(max_length=100)
    data = models.TextField(default='{"bloodpressure":[],"oximetry":[],"temperature":[],"glucose":[],"medication":[]}')

    def __str__(self):
        return self.username