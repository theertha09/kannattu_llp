from django.db import models

# Create your models here.
from django.db import models
from login.models import Account
from roles.models import Role
from django.utils.timezone import now

class hr(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('deactivated', 'Deactivated')], default='active')
    created_date = models.DateTimeField(default=now)
    created_by = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_telecallers')

    def delete(self, *args, **kwargs):
        print("Telecaller delete called — also deleting account.")
        account = self.account
        super().delete(*args, **kwargs)
        if account:
            account.delete()



    def __str__(self):
        return self.name
