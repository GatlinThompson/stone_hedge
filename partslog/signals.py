from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Log
from partsdatabase.models import Kit, Part, Hardware, HardwareKit


@receiver(post_save, sender=Log)
def log_approved(sender, instance, created, **kwargs):
    """
    Checks if item name is real and then adds to the database
    Subtracts parts/hardware/hardwareKit from the other table that belong to the kit/hardware kit
    """
    if not created and instance.approved:
        name = instance.name
        try:
            kit = Kit.objects.get(name=name)
            kit.quantity += instance.quantity
            kit.save()

            for kit_part in kit.kitpartassembly_set.all():
                part_qty = kit_part.quantity * instance.quantity
                part = Part.objects.get(id=kit_part.part.id)
                part.quantity -= part_qty
                part.save()

            for kit_hw in kit.kithardwareassembly_set.all():
                hw_qty = kit_hw.quantity * instance.quantity
                hardware = Hardware.objects.get(id=kit_hw.hardware.id)
                hardware.quantity -= hw_qty
                hardware.save()

            for kit_hk in kit.kithardwarekit_set.all():
                hk_qty = kit_hk.quantity * instance.quantity
                hardware_kit = HardwareKit.objects.get(id=kit_hk.hardware_kit.id)
                hardware_kit.quantity -= hk_qty
                hardware_kit.save()

        except Kit.DoesNotExist:
            try:
                hardware_kit = HardwareKit.objects.get(name=name)
                hardware_kit.quantity += instance.quantity
                hardware_kit.save()

                for hk_part in hardware_kit.parthkassembly_set.all():
                    part_qty = hk_part.quantity * instance.quantity
                    part = Part.objects.get(id=hk_part.part.id)
                    part.quantity -= part_qty
                    part.save()

                for hk_hardware in hardware_kit.hardwarekitassembly_set.all:
                    hk_qty = hk_hardware.quantity * instance.quantity
                    hardware = Hardware.objects.get(id=hk_hardware.hardware.id)
                    hardware.quantity -= hk_qty
                    hardware.save()


            except HardwareKit.DoesNotExist:
                try:
                    part = Part.objects.get(name=name)
                    part.quantity += instance.quantity
                    part.save()

                except Part.DoesNotExist:
                    try:
                        hardware = Hardware.objects.get(name=name)
                        hardware.quantity += instance.quantity
                        hardware.save()

                    except Hardware.DoesNotExist:
                        print (f"{instance.name} has no associated item to it.")
