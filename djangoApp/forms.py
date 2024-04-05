from django import forms
from django.forms import ModelForm, DateInput, NumberInput, FileInput, ModelMultipleChoiceField, Textarea, TextInput, CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

#from .models import Order


#class OrderForm(ModelForm):
    #class Meta:
        #model = Order
        #fields ='__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']

class JournalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)
        self.fields['Training_Date'].widget = DateInput(attrs={'type': 'date'})
        self.fields['Duration'].widget = NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'})
        self.fields['image'].widget = FileInput(attrs={'class': 'form-control-file'})
        self.fields['video'].widget = FileInput(attrs={'class': 'form-control-file'})
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # Set the user field to the current user
        if commit:
            instance.save()
        return instance
    class Meta:
        model = TrainingLogEntry
        fields = ['Training_Date', 'Techniques', 'Notes', 'Duration', 'image', 'video']

class TechniqueForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the user from the kwargs
        super().__init__(*args, **kwargs)
        self.fields['image'].widget = FileInput(attrs={'class': 'form-control-file'})
        self.fields['video'].widget = FileInput(attrs={'class': 'form-control-file'})


    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # Set the user field to the current user
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = TechniqueLibraryEntry
        fields = ['Technique_Name', 'Description','Status', 'image', 'video']

class TechniqueSeriesForm(ModelForm):
    techniques = ModelMultipleChoiceField(
        queryset=TechniqueLibraryEntry.objects.all(),
        widget=CheckboxSelectMultiple,  # Directly use the widget without additional attrs
        required=False 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure other fields as needed
        self.fields['SeriesName'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['Description'].widget = Textarea(attrs={'class': 'form-control', 'rows': 3})

    class Meta:
        model = TechniqueSeriesEntry
        fields = ['SeriesName', 'Description', 'Techniques']
