from django.forms import ModelForm, Textarea, TextInput
from MainApp.models import Svs_z, Svs_k, Comment
from django.contrib.auth.models import User
from django.forms import CharField, PasswordInput
from django.core.exceptions import ValidationError



class ZvsForm(ModelForm):
   class Meta:
       model = Svs_z
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code', 'private']
       widgets = {
           'name': TextInput(attrs={"placeholder": "Название", "class": "blue"}),
           'code': Textarea(attrs={"placeholder": "Код"}),
       }
       labels = {
           'name': '',
           'lang': '',
           'code': ''
       }



class KvsForm(ModelForm):
   class Meta:
       model = Svs_k
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'date', 'test', 'rab', 'priem', 'lang']
       widgets = {
        #   'name': TextInput(attrs={"placeholder": "Название", "class": "blue"}),
           'lang': Textarea(attrs={"placeholder": "Примечание"}),

       }
       labels = {
#           'name': '',
#           'lang': '',
#           'code': ''
       }

#    name = models.CharField(max_length=3, choices=NAMEKVS)
#    date = models.DateField(null=True, blank=True)
#    test = models.IntegerField(default=0)
#    rab = models.PositiveSmallIntegerField(default=0)
#    priem = models.BooleanField(default=False)
#    lang = models.CharField(max_length=300)


class UserRegistrationForm(ModelForm):
   class Meta:
       model = User
       fields = ["username", "email"]

   password1 = CharField(label="password", widget=PasswordInput)
   password2 = CharField(label="password confirm", widget=PasswordInput)

   def clean_password2(self):
       pass1 = self.cleaned_data.get("password1")
       pass2 = self.cleaned_data.get("password2")
       if pass1 and pass2 and pass1 == pass2:
           return pass2
       raise ValidationError("Пароли не совпадают или пустые")

   def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data["password1"])
       if commit:
           user.save()
       return user



class CommentForm(ModelForm):
   class Meta:
       model = Comment
       fields = ['text']
