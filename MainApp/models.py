from django.db import models


LANG = [
    ("py", "python"),
    ("js", "java"),
    ("Cpp", "С++")
]

NAMEKVS = [
    ("KVS", "KVS"),

]

class Svs_k(models.Model):
    name = models.CharField(max_length=3, choices=NAMEKVS)
    date = models.DateField(null=True, blank=True)
    test = models.IntegerField(default=0)
    rab = models.PositiveSmallIntegerField(default=0)
    priem = models.BooleanField(default=False)
    lang = models.CharField(max_length=300)



class Svs_z(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)