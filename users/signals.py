from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


# New Users are in Employee Group
@receiver(post_save, sender=User)
def default_employee_group_user(sender, instance, created, **kwargs):
    if created:
        user = instance
        user.set_password(instance.password)
        user.groups.add(Group.objects.get(name="Employee"))
        user.save()

