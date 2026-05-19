from django.db import models
from django.contrib.auth.models import User


class Application(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=100)

    job_role = models.CharField(max_length=100)

    status = models.CharField(max_length=50)

    applied_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.company_name