from django.forms import ModelForm, Textarea, TextInput
from MainApp.models import Svs_z


class ZvsForm(ModelForm):
   class Meta:
       model = Svs_z
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code']
       widgets = {
           'name': TextInput(attrs={"placeholder": "Название", "class": "blue"}),
           'code': Textarea(attrs={"placeholder": "Код"}),
       }
       labels = {
           'name': '',
           'lang': '',
           'code': ''
       }


