from django import forms

from partsdatabase.models import Kit, HardwareKit, Part, Hardware
from .models import Log


class LogForm(forms.ModelForm):

    class Meta:
        model = Log
        fields = '__all__'
        widgets = {
            'created_by': forms.HiddenInput(),
            'approved': forms.HiddenInput(),
            'approved_by': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'time': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # Validates item name is in the database
    def clean_name(self):
        name = self.cleaned_data['name']

        try:
            Kit.objects.get(name=name)
        except Kit.DoesNotExist:
            try:
                HardwareKit.objects.get(name=name)
            except HardwareKit.DoesNotExist:
                try:
                    Part.objects.get(name=name)
                except Part.DoesNotExist:
                    try:
                        Hardware.objects.get(name=name)
                    except Hardware.DoesNotExist:
                        raise forms.ValidationError("Item does not exist.")

        return name


