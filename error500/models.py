from django.db import models


class Error500(models.Model):

    class Meta:
        db_table = "error500"

    request_scheme = models.CharField(max_length=20, null=True)  # http/https
    request_url = models.CharField(max_length=500, null=True)
    request_method = models.CharField(max_length=50, null=True)
    request_headers = models.TextField(null=True)  # headers in JSON
    request_data = models.TextField(null=True)  # request.POST
    request_body = models.TextField(null=True)  # request.body
    description = models.TextField(null=True)  # traceback
    created_at = models.DateTimeField(auto_now_add=True)
