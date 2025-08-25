from django.db import models
import uuid

class Resignation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    notice_period = models.IntegerField()
    resignation_date = models.DateField()
    branch = models.CharField(max_length=100)
    last_working_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} ({self.employee_id})"
