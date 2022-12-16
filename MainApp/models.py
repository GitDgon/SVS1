from django.db import models


LANG = [
    ("py", "python"),
    ("js", "java"),
    ("Cpp", "С++")
]

class Svs_k(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)

class Svs_z(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)