from django.db import models
from django.contrib.auth.models import User


LANG = [
    ("py", "python"),
    ("js", "java"),
    ("Cpp", "С++")
]

NAMEKVS = [
    ("KVS-ГФИ", "KVS-ГФИ"),
    ("KVS-Приемная", "KVS-Приемная"),
    ("KVS-Уренгой", "KVS-Уренгой"),

]

OPERATORKVS = [
    ("Ivanov I.I.", "Иванов"),
    ("Petrov P.P.", "Петров"),
    ("Sidorov S.S.", "Сидоров"),

]

VEDUSHIJKVS = [
    ("MinStroj", "Минстрой"),
    ("MinZdrav", "Минздрав"),
    ("Ektb", "Екатеринбург"),

]

class Svs_k(models.Model):
    name = models.CharField(max_length=12, choices=NAMEKVS)
    operator = models.CharField(max_length=13, choices=OPERATORKVS, default=True)
    vedushij = models.CharField(max_length=13, choices=VEDUSHIJKVS, default=True)
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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)   #blank=True, null=True - т.е. неавторизованные могут добавлять svs

                                                        #on_delete=models.CASCADE - если удалим пользователя
                                                         #то удалятся все его сниппеты
    private = models.BooleanField(default=True)  #все раннее введенные будут приватные

class Comment(models.Model):
   text = models.TextField(max_length=2000)
   creation_date = models.DateTimeField(auto_now=True)
   author = models.ForeignKey(to=User, on_delete=models.CASCADE)
   snippet = models.ForeignKey(to=Svs_z, on_delete=models.CASCADE, related_name='comments')
