from django import forms
from .models import *

class TrainForms(forms.ModelForm):
    class Meta:
        model = Train
        fields = '__all__'
        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
        }





class StationAddForms(forms.ModelForm):
    class Meta:
        model = Station
        fields = '__all__'
        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
        }


class TicketAddForm(forms.ModelForm): 
    class Meta: 
        model = Ticket 
        fields = "__all__" 
        widgets = { 
            'train': forms.Select(attrs={'class': 'form-control'}), 
            'starting_station': forms.Select(attrs={'class': 'form-control'}), 
            'destination_station': forms.Select(attrs={'class': 'form-control'}), 
            'ticket_price_inr': forms.NumberInput(attrs={'class': 'form-control'}),
            'train_time': forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}), 
            'ticket_name': forms.TextInput(attrs={'class': 'form-control'}), 
        }
# class DateInput(forms.DateInput):
#     input_type='date'
#     class TicketAddForm(forms.ModelForm):
#         model=TicketAddForm
#         fields='__all__'
#         widgets={
#             'train_time':DateInput()
#         }

        
class TwoFieldSearchForm(forms.Form):
    field1 = forms.CharField(max_length=100, required=False, label='Field 1')
    field2 = forms.CharField(max_length=100, required=False, label='Field 2')
