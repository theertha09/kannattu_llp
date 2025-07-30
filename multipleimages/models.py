# models.py
from django.db import models
import os
import uuid
from personaldetails.models import PersonalDetails

def upload_to(instance, filename):
    """Generate unique filename for uploaded images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/images/', filename)

class DocumentUpload(models.Model):
    """Main document upload model"""
    user = models.OneToOneField(PersonalDetails, on_delete=models.CASCADE, related_name='document_uploads')
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Documents for {self.user.full_name} - {self.title or 'Untitled'}"

class DocumentImage(models.Model):
    """Model to store multiple images for a document"""
    DOCUMENT_TYPES = [
        ('passport', 'Passport Size Photo'),
        ('aadhaar_front', 'Aadhaar Card Front'),
        ('aadhaar_back', 'Aadhaar Card Back'),
        ('pan', 'PAN Card'),
        ('voter_id', 'Voter ID Card'),
        ('sslc', 'sslc Certificate'),
        ('plustwo', 'Plus Two Certificate'),
        ('ug', 'Undergraduate Certificate'),
        ('pg', 'Postgraduate Certificate'),
        ('experience', 'Experience Letter'),
        ('police_clearance', 'Police Clearance Certificate'),
        ('cibil_report', 'CIBIL Report'),
    ]
    
    document_upload = models.ForeignKey(
        DocumentUpload, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to=upload_to)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()  # in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.document_type} - {self.original_filename}"
