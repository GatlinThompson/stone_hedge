from django.core.validators import MinValueValidator
from django.db import models


class Hardware(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=10, unique=True)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=10, default='A01', blank=True)
    quantity = models.IntegerField()
    reorder_quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)


class Part(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=10, default='A01', blank=True)
    quantity = models.IntegerField()
    reorder_quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)


class HardwareKit(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)
    reorder_quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)
    hardware = models.ManyToManyField(Hardware, through='HardwareKitAssembly')
    part = models.ManyToManyField(Part, through='PartHKAssembly')


# Kits consist of either parts, hardware, and/or hardware kits
class Kit(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=10, unique=True)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=10)
    quantity = models.IntegerField()
    reorder_quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2, max_digits=20)
    hardware = models.ManyToManyField(Hardware, through='KitHardwareAssembly', blank=True)
    hardware_kit = models.ManyToManyField(HardwareKit, through='KitHardwareKit', blank=True)
    part = models.ManyToManyField(Part, through='KitPartAssembly', blank=True)


# Joint Table for Kit and Prat
class KitPartAssembly(models.Model):

    class Meta:
        unique_together = [('kit', 'part')]
        ordering = ['kit', 'part']

    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


# Joint Table for Kit and Hardware
class KitHardwareAssembly(models.Model):

    def __str__(self):
        return f'{self.kit.name}-{self.hardware.name}: {self.quantity}'

    class Meta:
        unique_together = [('kit', 'hardware')]
        ordering = ['kit', 'hardware']

    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


# Joint Table for Kit and HardwareKit
class KitHardwareKit(models.Model):

    class Meta:
        unique_together = [('kit', 'hardware_kit')]
        ordering = ['kit', 'hardware_kit']

    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    hardware_kit = models.ForeignKey(HardwareKit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


"""
Hardware Kit Joint Tables
"""


# Joint Table for HardwareKit and Hardware
class HardwareKitAssembly(models.Model):

    class Meta:
        unique_together = [('hardware_kit', 'hardware')]
        ordering = ['hardware']

    hardware_kit = models.ForeignKey(HardwareKit, on_delete=models.CASCADE)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


# Joint Table for HardwareKit and Part
class PartHKAssembly(models.Model):

    class Meta:
        unique_together = [('hardware_kit', 'part')]
        ordering = ['part']

    hardware_kit = models.ForeignKey(HardwareKit, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])


