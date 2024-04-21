from django import forms
from .models import (Kit, KitHardwareAssembly, KitPartAssembly,
                     KitHardwareKit, Hardware, Part, HardwareKit, HardwareKitAssembly, PartHKAssembly)
from django.utils.safestring import mark_safe

from django.utils.html import format_html


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ['name', 'description', 'location', 'quantity', 'reorder_quantity', 'unit_price']


class KitHKAssemblyForm(forms.ModelForm):

    def __init__(self, *args, kit=None, **kwargs):
        super().__init__(*args, **kwargs)
        if kit:
            kit_id = Kit.objects.get(pk=kit)
            used_hk = KitHardwareKit.objects.filter(kit=kit_id).values_list('hardware_kit', flat=True)
            available_hk = HardwareKit.objects.exclude(pk__in=used_hk)
            self.fields['hardware_kit'].choices = [('', 'Choose a Hardware Kit')] + [
                (hw.id, f"{hw.name}: {hw.description}")
                for hw in available_hk]

    class Meta:
        model = KitHardwareKit
        fields = '__all__'
        widgets = {
            'kit': forms.HiddenInput(),
            'hardware_kit': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control fw-semibold fs-5 text-center'})
        }


class KitHardwareAssemblyForm(forms.ModelForm):

    def __init__(self, *args, kit=None, **kwargs):
        super().__init__(*args, **kwargs)
        if kit:
            kit_id = Kit.objects.get(pk=kit)
            used_hw = KitHardwareAssembly.objects.filter(kit=kit_id).values_list('hardware', flat=True)
            available_hw = Hardware.objects.exclude(pk__in=used_hw)
            self.fields['hardware'].choices = [('', 'Choose a Hardware')] + [
                (hw.id, f"{hw.name}: {hw.description}")
                for hw in available_hw]


    class Meta:
        model = KitHardwareAssembly
        fields = '__all__'
        widgets = {
            'kit': forms.HiddenInput(),
            'hardware': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control fw-semibold fs-5 text-center'})
        }


class KitPartAssemblyForm(forms.ModelForm):

    def __init__(self, *args, kit=None, **kwargs):
        super().__init__(*args, **kwargs)
        if kit:
            kit_id = Kit.objects.get(pk=kit)
            used_parts = KitPartAssembly.objects.filter(kit=kit_id).values_list('part', flat=True)
            available_parts = Part.objects.exclude(pk__in=used_parts)
            self.fields['part'].choices = [('', 'Choose a Part')] + [
                (part.id, f"{part.name}: {part.description}")
                for part in available_parts]

    class Meta:
        model = KitPartAssembly
        fields = '__all__'
        widgets = {
            'kit': forms.HiddenInput(),
            'part': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control fw-semibold fs-5 text-center'})
        }


class HardwareForm(forms.ModelForm):
    class Meta:
        model = Hardware
        fields = '__all__'


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'
        widgets = {
        }


class HardwareKitForm(forms.ModelForm):
    class Meta:
        model = HardwareKit
        fields = '__all__'
        exclude = ['hardware', 'part']


class HardwareKitAssemblyForm(forms.ModelForm):

    def __init__(self, *args, hardware_kit=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hardware_kit:
            hk = HardwareKit.objects.get(pk=hardware_kit)
            used_hw = HardwareKitAssembly.objects.filter(hardware_kit=hk).values_list('hardware', flat=True)
            available_hw = Hardware.objects.exclude(pk__in=used_hw)
            self.fields['hardware'].choices = [('', 'Choose a Hardware')] + [
                (hw.id, f"{hw.name}: {hw.description}")
                for hw in available_hw]

    class Meta:
        model = HardwareKitAssembly
        fields = '__all__'
        widgets = {
            'hardware_kit': forms.HiddenInput(),
            'hardware': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control fw-semibold fs-5 text-center'})
        }


class PartHKAssemblyForm(forms.ModelForm):

    def __init__(self, *args, hardware_kit=None, **kwargs):
        super().__init__(*args, **kwargs)
        if hardware_kit:
            hk = HardwareKit.objects.get(pk=hardware_kit)
            used_parts = PartHKAssembly.objects.filter(hardware_kit=hk).values_list('part', flat=True)
            available_parts = Part.objects.exclude(pk__in=used_parts)
            self.fields['part'].choices = [('', 'Choose a Part')] + [
                (part.id, f"{part.name}: {part.description}")
                for part in available_parts]



    class Meta:
        model = PartHKAssembly
        fields = '__all__'
        widgets = {'hardware_kit': forms.HiddenInput(),
                   'part': forms.Select(attrs={'class': 'form-control'}),
                   'quantity': forms.NumberInput(attrs={'class': 'form-control fw-semibold fs-5 text-center'})
                   }
