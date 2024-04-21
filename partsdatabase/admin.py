from django.contrib import admin
from .models import (Kit, KitHardwareKit, KitHardwareAssembly, Part, KitPartAssembly,
                     HardwareKitAssembly, HardwareKit, Hardware, PartHKAssembly)

# Register your models here.
admin.site.register(Kit)
admin.site.register(KitHardwareKit)
admin.site.register(KitHardwareAssembly)
admin.site.register(Part)
admin.site.register(KitPartAssembly)
admin.site.register(HardwareKit)
admin.site.register(HardwareKitAssembly)
admin.site.register(Hardware)
admin.site.register(PartHKAssembly)
