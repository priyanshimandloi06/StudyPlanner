from django import forms
from .models import Slot


class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['weekday', 'subject', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        data = super().clean()
        s, e = data.get('start_time'), data.get('end_time')
        if s and e and e <= s:
            raise forms.ValidationError('End time must be later than the start time.')
        return data
