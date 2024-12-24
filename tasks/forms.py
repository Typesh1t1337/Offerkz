from .models import Task,Category
from django.forms import Form,ModelForm,TextInput,Textarea,DateInput,CheckboxInput,Select,NumberInput,ModelChoiceField,ChoiceField,DecimalField,CharField
from django import forms

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description','deadline','price','category','isAgreed']

        widgets={
            "title": TextInput(attrs={'placeholder':'Название  (минимум 5 символов)'
                                      ,'type':'text'
                                      ,'name':'title'
                                      ,'id':'title'
                                      }),
            "description": Textarea(attrs={
                                            'type':'text'
                                           ,'name':'description'
                                           ,'placeholder':'Описание задании (минимум 50 символов)'
                                           ,'id':'desc'

                                            }),
            'deadline': DateInput(attrs={'type':'date',
                                         'name':'deadline',
                                         'id':'deadline'
                                         }),
            'isAgreed': CheckboxInput(attrs={'type':'checkbox',
                                             'name':'isAgreed',}),
            'price': NumberInput(attrs={'type':'number',
                                        'name':'cost',
                                        'id':'cost'}),

            'category': Select(attrs={'type':'text','name':'category','id':'selector'})
        }

        category = ModelChoiceField(queryset=Category.objects.all(),empty_label="Выберите категорию")


class FilterTaskForm(forms.Form):
    category = ModelChoiceField(queryset=Category.objects.all(),empty_label="Выберите категорию",required=False)
    price_min = DecimalField(required=False,max_digits=10,decimal_places=2,widget=NumberInput(attrs={'placeholder':'От'}))
    price_max = DecimalField(required=False,max_digits=10,decimal_places=2,widget=NumberInput(attrs={'placeholder':'До'}))
    order_by_time = ChoiceField(choices=[('',"Фильтр по дате"),('time_created','С начала новые'),('-time_created',"С начала старые")],required=False)
    order_by_price = ChoiceField(choices=[('',"Фильтр по цене"),("price","C начала дешевые"),("-price","С начала дорогие")],required=False)
    query = CharField(required=False,widget=TextInput(attrs={'placeholder':'Поиск задании'}))


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','deadline','price','category','isAgreed']

        widgets = {
            "title": TextInput(attrs={'placeholder': 'Название  (минимум 5 символов)'
                , 'type': 'text'
                , 'name': 'title'
                , 'id': 'title'

            }),
            "description": Textarea(attrs={
                'type': 'text'
                , 'name': 'description'
                , 'placeholder': 'Описание задании (минимум 50 символов)'
                , 'id': 'desc'


            }),
            'deadline': DateInput(attrs={'type': 'date',
                                         'name': 'deadline',
                                         'id': 'deadline'
                                         }),
            'isAgreed': CheckboxInput(attrs={'type': 'checkbox',
                                             'name': 'isAgreed', }),
            'price': NumberInput(attrs={'type': 'number',
                                        'name': 'cost',
                                        'id': 'cost'}),

            'category': Select(attrs={'type': 'text', 'name': 'category', 'id': 'selector'})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance.pk  and self.instance.category:
            self.fields['category'].inital = self.instance.category


