from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Count
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Header
from django.conf import settings
import os
from datetime import datetime
from .models import Resignation
from .serializers import ResignationSerializer


# ✅ Enhanced SendGrid Email Service with Audit Notification
class EmailService:
    def __init__(self):
        # Use your SendGrid API key
        self.sg = sendgrid.SendGridAPIClient(
        )
        self.from_email = Email(""
        ""
        ""
        "@kannattu.com")
        self.hr_email = "theerthakk467@gmail.com"

        self.audit_emails = [
            "theerthakk467@gmail.com",
        ]

    def send_resignation_notification(self, resignation_data):
        """Send email notification to HR when a new resignation is submitted"""
        try:
            to_email = To(self.hr_email)
            subject = f"New Resignation Application - {resignation_data['employee_name']}"
            
            # Enhanced HTML content with forward-safe inline styles and table-based layout
            html_content = f"""
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>Resignation Application - {resignation_data['employee_name']}</title>
                <!--[if mso]>
                <noscript>
                    <xml>
                        <o:OfficeDocumentSettings>
                            <o:PixelsPerInch>96</o:PixelsPerInch>
                        </o:OfficeDocumentSettings>
                    </xml>
                </noscript>
                <![endif]-->
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50; background-color: #f8f9fa;">
                <!-- Main container table for better email client compatibility -->
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; padding: 20px 0;">
                    <tr>
                        <td align="center">
                            <!-- Email container table -->
                            <table border="0" cellpadding="0" cellspacing="0" width="650" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden; max-width: 650px;">
                                
                                <!-- Header Section -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); background-color: #667eea; color: white; padding: 30px; text-align: center;">
                                        <h1 style="margin: 0; font-size: 24px; font-weight: 300; letter-spacing: 1px; font-family: Arial, sans-serif;">Resignation Application</h1>
                                        <div style="font-size: 14px; opacity: 0.9; margin-top: 5px;">Human Resources Department</div>
                                    </td>
                                </tr>
                                
                                <!-- Content Section -->
                                <tr>
                                    <td style="padding: 40px 30px;">
                                        
                                        <!-- Greeting -->
                                        <div style="font-size: 16px; margin-bottom: 25px; color: #34495e; line-height: 1.6;">
                                            Dear HR Team,<br/><br/>
                                            We hope this message finds you well. We would like to inform you that a new resignation application has been submitted through our HR portal and requires your immediate attention for processing.
                                        </div>
                                        
                                        <!-- Employee Information Card -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; margin: 25px 0;">
                                            <tr>
                                                <td style="padding: 25px;">
                                                    <div style="color: #495057; font-size: 18px; font-weight: 600; margin-bottom: 20px; border-bottom: 2px solid #dee2e6; padding-bottom: 10px;">Employee Information</div>
                                                    
                                                    <!-- Employee details table -->
                                                    <table border="0" cellpadding="5" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td width="180" style="font-weight: 600; color: #6c757d; vertical-align: top;">Full Name:</td>
                                                            <td style="color: #495057;">{resignation_data['employee_name']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Employee ID:</td>
                                                            <td style="color: #495057;">{resignation_data['employee_id']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Email Address:</td>
                                                            <td style="color: #495057;">{resignation_data['email']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Branch:</td>
                                                            <td style="color: #495057;">{resignation_data['branch']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Department:</td>
                                                            <td style="color: #495057;">{resignation_data['department']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Current Designation:</td>
                                                            <td style="color: #495057;">{resignation_data['designation']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Notice Period:</td>
                                                            <td style="color: #495057;">{resignation_data['notice_period']} days</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Resignation Date:</td>
                                                            <td style="color: #495057;">{resignation_data['resignation_date']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Proposed Last Working Day:</td>
                                                            <td style="color: #495057;">{resignation_data['last_working_date']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Application Status:</td>
                                                            <td style="color: #495057;">
                                                                <span style="background-color: #17a2b8; color: white; padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">{resignation_data.get('status', 'Pending').title()}</span>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Submission Date:</td>
                                                            <td style="color: #495057;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Reason Section -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; margin: 20px 0;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <div style="font-weight: 600; color: #856404; margin-bottom: 10px;">Reason for Resignation</div>
                                                    <div style="color: #6c5701; font-style: italic; line-height: 1.5;">"{resignation_data['reason']}"</div>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Reference Number -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #e3f2fd; border: 1px solid #bbdefb; border-radius: 4px; margin: 20px 0;">
                                            <tr>
                                                <td style="padding: 15px; text-align: center;">
                                                    <div style="font-size: 12px; color: #1976d2; font-weight: 600; margin-bottom: 5px;">APPLICATION REFERENCE NUMBER</div>
                                                    <div style="font-family: 'Courier New', monospace; font-size: 14px; color: #0d47a1; font-weight: 600;">{resignation_data.get('uuid', 'N/A')}</div>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Action Section -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #e8f5e8; border: 1px solid #c3e6c3; border-radius: 6px; margin: 25px 0;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <div style="color: #155724; font-weight: 600; margin-bottom: 15px;">Recommended Next Steps</div>
                                                    <ul style="color: #155724; margin: 0; padding-left: 20px; line-height: 1.8;">
                                                        <li>Acknowledge receipt of the resignation application</li>
                                                        <li>Review and verify all provided information</li>
                                                        <li>Schedule an exit interview with the employee</li>
                                                        <li>Initiate knowledge transfer and handover procedures</li>
                                                        <li>Update employee records and payroll systems</li>
                                                        <li>Collect and verify return of company assets (e.g., laptop, ID card, access cards)</li>
                                                        <li>Coordinate with relevant departments for replacement planning</li>
                                                        <li>Update the application status in the HR portal</li>
                                                    </ul>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Final Note -->
                                        <div style="color: #495057; font-size: 14px; margin-top: 30px; line-height: 1.6;">
                                            Please treat this matter with appropriate confidentiality and process the application in accordance with company policies and procedures.
                                        </div>
                                        
                                    </td>
                                </tr>
                                
                                <!-- Footer Section -->
                                <tr>
                                    <td style="background-color: #f8f9fa; padding: 25px 30px; border-top: 1px solid #dee2e6; text-align: center;">
                                        <div style="color: #6c757d; font-size: 13px; margin: 0; line-height: 1.5;">
                                            This is an automated notification from the HR Management System.<br/>
                                            Please do not reply to this email. For any queries, please contact the HR department directly.
                                        </div>
                                    </td>
                                </tr>
                                
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            
            # Enhanced plain text version
            plain_text_content = f"""
            ═══════════════════════════════════════════════════════════
                          RESIGNATION APPLICATION NOTIFICATION
            ═══════════════════════════════════════════════════════════
            
            Dear HR Team,
            
            We hope this message finds you well. We would like to inform you that 
            a new resignation application has been submitted through our HR portal 
            and requires your immediate attention for processing.
            
            ┌─────────────────────────────────────────────────────────────┐
            │                    EMPLOYEE INFORMATION                     │
            └─────────────────────────────────────────────────────────────┘
            
            Full Name                 : {resignation_data['employee_name']}
            Employee ID               : {resignation_data['employee_id']}
            Email Address             : {resignation_data['email']}
            Branch                    : {resignation_data['branch']}
            Department                : {resignation_data['department']}
            Current Designation       : {resignation_data['designation']}
            Notice Period             : {resignation_data['notice_period']} days
            Resignation Date          : {resignation_data['resignation_date']}
            Proposed Last Working Day : {resignation_data['last_working_date']}
            Application Status        : {resignation_data.get('status', 'Pending').title()}
            Submission Date           : {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

            ┌─────────────────────────────────────────────────────────────┐
            │                   REASON FOR RESIGNATION                    │
            └─────────────────────────────────────────────────────────────┘
            
            "{resignation_data['reason']}"
            
            ┌─────────────────────────────────────────────────────────────┐
            │                APPLICATION REFERENCE NUMBER                 │
            └─────────────────────────────────────────────────────────────┘
            
            REF: {resignation_data.get('uuid', 'N/A')}
            
            ┌─────────────────────────────────────────────────────────────┐
            │                   RECOMMENDED NEXT STEPS                    │
            └─────────────────────────────────────────────────────────────┘
            
            ✓ Acknowledge receipt of the resignation application
            ✓ Review and verify all provided information
            ✓ Schedule an exit interview with the employee
            ✓ Initiate knowledge transfer and handover procedures
            ✓ Update employee records and payroll systems
            ✓ Collect and verify return of company assets
            ✓ Coordinate with relevant departments for replacement planning
            ✓ Update the application status in the HR portal
            
            Please treat this matter with appropriate confidentiality and process 
            the application in accordance with company policies and procedures.
            
            Best regards,
            HR Management System
            
            ═══════════════════════════════════════════════════════════════
            This is an automated notification from the HR Management System.
            Please do not reply to this email. For any queries, please contact 
            the HR department directly.
            ═══════════════════════════════════════════════════════════════
            """
            
            mail = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=plain_text_content
            )
            
            # Add additional headers for better forwarding compatibility
            from sendgrid.helpers.mail import Header
            mail.add_header(Header("X-Priority", "1"))
            mail.add_header(Header("X-MSMail-Priority", "High"))
            mail.add_header(Header("Importance", "high"))
            
            response = self.sg.send(mail)
            return True, f"Email sent successfully. Status code: {response.status_code}"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

    def send_audit_notification(self, resignation_data):
        """Send professional audit notification to audit team when HR approves resignation"""
        try:
            # Create audit reference number
            audit_ref = f"AUDIT-{resignation_data['employee_id']}-{datetime.now().strftime('%Y%m%d')}"
            
            # Professional HTML email for audit team
            audit_html_content = f"""
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>HR Approval – Audit Instructions for Resigned Employee</title>
                <!--[if mso]>
                <noscript>
                    <xml>
                        <o:OfficeDocumentSettings>
                            <o:PixelsPerInch>96</o:PixelsPerInch>
                        </o:OfficeDocumentSettings>
                    </xml>
                </noscript>
                <![endif]-->
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50; background-color: #f8f9fa;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; padding: 20px 0;">
                    <tr>
                        <td align="center">
                            <table border="0" cellpadding="0" cellspacing="0" width="700" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden; max-width: 700px;">
                                
                                <!-- Header Section -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, #d63031 0%, #e84393 100%); background-color: #d63031; color: white; padding: 30px; text-align: center;">
                                        <h1 style="margin: 0; font-size: 24px; font-weight: 300; letter-spacing: 1px; font-family: Arial, sans-serif;">HR Approval – Audit Instructions</h1>
                                        <div style="font-size: 14px; opacity: 0.9; margin-top: 5px;">Audit & Compliance Department</div>
                                    </td>
                                </tr>
                                
                                <!-- Content Section -->
                                <tr>
                                    <td style="padding: 40px 30px;">
                                        
                                        <!-- Formal Greeting -->
                                        <div style="font-size: 16px; margin-bottom: 25px; color: #34495e; line-height: 1.8;">
                                            Dear Audit & Chennai Team,<br/><br/>
                                            
                                            I trust this message finds you well. Following the recent HR approval of a resignation application, 
                                            we respectfully request your immediate attention to conduct a comprehensive audit as outlined below.
                                        </div>
                                        
                                        <!-- Priority Notice -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #fff3cd; border-left: 4px solid #ffc107; margin: 25px 0;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <div style="color: #856404; font-weight: 600; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">⚠️ Priority Audit Request</div>
                                                    <div style="color: #6c5701; font-style: italic;">This audit requires immediate attention and must be completed within the standard timeframe as per company policy.</div>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Employee Details Card -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; margin: 25px 0;">
                                            <tr>
                                                <td style="padding: 25px;">
                                                    <div style="color: #495057; font-size: 18px; font-weight: 600; margin-bottom: 20px; border-bottom: 2px solid #dee2e6; padding-bottom: 10px;">Subject Employee Information</div>
                                                    
                                                    <table border="0" cellpadding="5" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td width="180" style="font-weight: 600; color: #6c757d; vertical-align: top;">Employee Name:</td>
                                                            <td style="color: #495057; font-weight: 600;">{resignation_data['employee_name']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Employee ID:</td>
                                                            <td style="color: #495057;">{resignation_data['employee_id']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Branch:</td>
                                                            <td style="color: #495057;">{resignation_data['branch']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Department:</td>
                                                            <td style="color: #495057;">{resignation_data['department']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Designation:</td>
                                                            <td style="color: #495057;">{resignation_data['designation']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">Last Working Date:</td>
                                                            <td style="color: #495057;">{resignation_data['last_working_date']}</td>
                                                        </tr>
                                                        <tr>
                                                            <td style="font-weight: 600; color: #6c757d; vertical-align: top;">HR Approval Date:</td>
                                                            <td style="color: #495057;">{datetime.now().strftime('%B %d, %Y')}</td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Audit Instructions -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #e8f4fd; border: 1px solid #bee5eb; border-radius: 6px; margin: 25px 0;">
                                            <tr>
                                                <td style="padding: 25px;">
                                                    <div style="color: #0c5460; font-size: 18px; font-weight: 600; margin-bottom: 20px;">Audit Scope & Instructions</div>
                                                    
                                                    <div style="color: #0c5460; margin-bottom: 20px; line-height: 1.7;">
                                                        As per HR approval, you are hereby instructed to proceed with a detailed and comprehensive 
                                                        audit regarding the recently resigned employee, with particular focus on identified 
                                                        irregularities and any personal loans issued.
                                                    </div>
                                                    
                                                    <div style="color: #0c5460; font-weight: 600; margin-bottom: 15px;">The audit shall encompass the following areas:</div>
                                                    
                                                    <!-- Audit Checklist -->
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 15px 0;">
                                                        <tr>
                                                            <td style="color: #0c5460; padding: 8px 0; border-bottom: 1px solid #bee5eb;">
                                                                <strong>1. Document Verification & Records Review</strong><br/>
                                                                <span style="font-size: 14px; opacity: 0.9;">• Comprehensive verification of all related documents, approvals, and official records<br/>
                                                                • Cross-referencing of digital and physical documentation<br/>
                                                                • Validation of authorization signatures and approval workflows</span>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="color: #0c5460; padding: 8px 0; border-bottom: 1px solid #bee5eb;">
                                                                <strong>2. Policy Compliance Assessment</strong><br/>
                                                                <span style="font-size: 14px; opacity: 0.9;">• Identification of any procedural lapses or deviations<br/>
                                                                • Analysis of policy violations and their severity<br/>
                                                                • Review of internal controls and their effectiveness</span>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="color: #0c5460; padding: 8px 0; border-bottom: 1px solid #bee5eb;">
                                                                <strong>3. Personal Loan Transaction Analysis</strong><br/>
                                                                <span style="font-size: 14px; opacity: 0.9;">• Detailed review of personal loan transaction history<br/>
                                                                • Assessment of repayment status and outstanding balances<br/>
                                                                • Verification of compliance with company loan policies<br/>
                                                                • Analysis of loan approval process and documentation</span>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td style="color: #0c5460; padding: 8px 0;">
                                                                <strong>4. Comprehensive Audit Report</strong><br/>
                                                                <span style="font-size: 14px; opacity: 0.9;">• Preparation of detailed findings with supporting evidence<br/>
                                                                • Risk assessment and impact analysis<br/>
                                                                • Actionable recommendations for remediation<br/>
                                                                • Executive summary with key highlights</span>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Audit Reference & Timeline -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; margin: 25px 0;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td width="50%" style="padding-right: 15px;">
                                                                <div style="font-size: 13px; color: #6c757d; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Audit Reference Number</div>
                                                                <div style="font-family: 'Courier New', monospace; color: #495057; font-weight: 600; font-size: 14px;">{audit_ref}</div>
                                                            </td>
                                                            <td width="50%" style="padding-left: 15px; border-left: 1px solid #dee2e6;">
                                                                <div style="font-size: 13px; color: #6c757d; font-weight: 600; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Expected Completion</div>
                                                                <div style="color: #495057; font-weight: 600;">As per standard audit timeline</div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Additional Instructions -->
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #e8f5e8; border: 1px solid #c3e6c3; border-radius: 6px; margin: 25px 0;">
                                            <tr>
                                                <td style="padding: 20px;">
                                                    <div style="color: #155724; font-weight: 600; margin-bottom: 15px;">Important Guidelines & Considerations</div>
                                                    <ul style="color: #155724; margin: 0; padding-left: 20px; line-height: 1.8;">
                                                        <li>All audit activities must be conducted with strict confidentiality and professionalism</li>
                                                        <li>Please coordinate with the HR department for access to required documentation</li>
                                                        <li>Ensure compliance with all internal audit procedures and protocols</li>
                                                        <li>Any significant findings should be escalated immediately to senior management</li>
                                                        <li>The final audit report should include clear recommendations with implementation timelines</li>
                                                        <li>Please maintain detailed audit trails and preserve all evidence collected during the process</li>
                                                    </ul>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- Closing -->
                                        <div style="color: #495057; margin-top: 30px; line-height: 1.7;">
                                            We appreciate your prompt attention to this matter and look forward to your thorough analysis. 
                                            Should you require any additional information, clarifications, or assistance from the HR department, 
                                            please do not hesitate to reach out to us directly.
                                        </div>
                                        
                                        <div style="color: #495057; margin-top: 25px; line-height: 1.6;">
                                            Thank you for your continued professionalism and dedication to maintaining the highest 
                                            standards of corporate governance and compliance.
                                        </div>
                                        
                                        <div style="color: #495057; margin-top: 30px;">
                                            Best regards,<br/>
                                            <strong>Human Resources Department</strong><br/>
                                            <span style="font-size: 14px; color: #6c757d;">Kannattu Group</span>
                                        </div>
                                        
                                    </td>
                                </tr>
                                
                                <!-- Footer Section -->
                                <tr>
                                    <td style="background-color: #f8f9fa; padding: 25px 30px; border-top: 1px solid #dee2e6; text-align: center;">
                                        <div style="color: #6c757d; font-size: 13px; margin: 0; line-height: 1.5;">
                                            <strong>CONFIDENTIAL AUDIT COMMUNICATION</strong><br/>
                                            This communication contains confidential information intended solely for the audit team.<br/>
                                            Please handle with appropriate confidentiality and security measures.
                                        </div>
                                    </td>
                                </tr>
                                
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
            
            # Professional plain text version
            audit_plain_text = f"""
            ═══════════════════════════════════════════════════════════════════
                           HR APPROVAL – AUDIT INSTRUCTIONS
                              Resigned Employee Irregularities
            ═══════════════════════════════════════════════════════════════════
            
            Dear Audit & Chennai Team,
            
            I trust this message finds you well. Following the recent HR approval of a 
            resignation application, we respectfully request your immediate attention to 
            conduct a comprehensive audit as outlined below.
            
            ⚠️ PRIORITY AUDIT REQUEST
            This audit requires immediate attention and must be completed within the 
            standard timeframe as per company policy.
            
            ┌─────────────────────────────────────────────────────────────────┐
            │                   SUBJECT EMPLOYEE INFORMATION                  │
            └─────────────────────────────────────────────────────────────────┘
            
            Employee Name         : {resignation_data['employee_name']}
            Employee ID           : {resignation_data['employee_id']}
            Branch                : {resignation_data['branch']}
            Department            : {resignation_data['department']}
            Designation           : {resignation_data['designation']}
            Last Working Date     : {resignation_data['last_working_date']}
            HR Approval Date      : {datetime.now().strftime('%B %d, %Y')}
            
            ┌─────────────────────────────────────────────────────────────────┐
            │                     AUDIT SCOPE & INSTRUCTIONS                  │
            └─────────────────────────────────────────────────────────────────┘
            
            As per HR approval, you are hereby instructed to proceed with a detailed 
            and comprehensive audit regarding the recently resigned employee, with 
            particular focus on identified irregularities and any personal loans issued.
            
            The audit shall encompass the following areas:
            
            1. DOCUMENT VERIFICATION & RECORDS REVIEW
               • Comprehensive verification of all related documents, approvals, 
                 and official records
               • Cross-referencing of digital and physical documentation
               • Validation of authorization signatures and approval workflows
            
            2. POLICY COMPLIANCE ASSESSMENT
               • Identification of any procedural lapses or deviations
               • Analysis of policy violations and their severity
               • Review of internal controls and their effectiveness
            
            3. PERSONAL LOAN TRANSACTION ANALYSIS
               • Detailed review of personal loan transaction history
               • Assessment of repayment status and outstanding balances
               • Verification of compliance with company loan policies
               • Analysis of loan approval process and documentation
            
            4. COMPREHENSIVE AUDIT REPORT
               • Preparation of detailed findings with supporting evidence
               • Risk assessment and impact analysis
               • Actionable recommendations for remediation
               • Executive summary with key highlights
            
            ┌─────────────────────────────────────────────────────────────────┐
            │                   AUDIT REFERENCE & TIMELINE                    │
            └─────────────────────────────────────────────────────────────────┘
            
            Audit Reference Number : {audit_ref}
            Expected Completion    : As per standard audit timeline
            
            ┌─────────────────────────────────────────────────────────────────┐
            │                IMPORTANT GUIDELINES & CONSIDERATIONS             │
            └─────────────────────────────────────────────────────────────────┘
            
            • All audit activities must be conducted with strict confidentiality 
              and professionalism
            • Please coordinate with the HR department for access to required 
              documentation
            • Ensure compliance with all internal audit procedures and protocols
            • Any significant findings should be escalated immediately to senior 
              management
            • The final audit report should include clear recommendations with 
              implementation timelines
            • Please maintain detailed audit trails and preserve all evidence 
              collected during the process
            
            We appreciate your prompt attention to this matter and look forward to 
            your thorough analysis. Should you require any additional information, 
            clarifications, or assistance from the HR department, please do not 
            hesitate to reach out to us directly.
            
            Thank you for your continued professionalism and dedication to maintaining 
            the highest standards of corporate governance and compliance.
            
            Best regards,
            Human Resources Department
            Kannattu Group
            
            ═══════════════════════════════════════════════════════════════════
                              CONFIDENTIAL AUDIT COMMUNICATION
            This communication contains confidential information intended solely 
            for the audit team. Please handle with appropriate confidentiality 
            and security measures.
            ═══════════════════════════════════════════════════════════════════
            """
            
            # Send emails to all audit team members
            for audit_email in self.audit_emails:
                audit_mail = Mail(
                    from_email=self.from_email,
                    to_emails=audit_email,
                    subject=f"HR Approval – Audit Instructions for Resigned Employee: {resignation_data['employee_name']} (Ref: {audit_ref})",
                    html_content=audit_html_content,
                    plain_text_content=audit_plain_text
                )
                
                # Add headers for importance
                audit_mail.add_header(Header("X-Priority", "1"))
                audit_mail.add_header(Header("X-MSMail-Priority", "High"))
                audit_mail.add_header(Header("Importance", "high"))
                audit_mail.add_header(Header("X-Audit-Reference", audit_ref))
                
                response = self.sg.send(audit_mail)
            
            return True, f"Audit notification sent successfully to {len(self.audit_emails)} audit team members. Reference: {audit_ref}"
            
        except Exception as e:
            return False, f"Failed to send audit notification: {str(e)}"


# ✅ Custom Pagination Class
class resignDetailsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "code": 200,
            "message": "",
            "data": data,
            "pagination": {
                "total": self.page.paginator.count,
                "page": self.page.number,
                "limit": self.get_page_size(self.request),
                "totalPages": self.page.paginator.num_pages,
            }
        })


# ✅ GET all resignations (paginated) and POST new resignation with email notification
class ResignationListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ResignationSerializer
    pagination_class = resignDetailsPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email_service = EmailService()

    def get_queryset(self):
        queryset = Resignation.objects.all()

        # ✅ Filter by status
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        # ✅ Filter by employee_name
        employee_name = self.request.query_params.get('employee_name')
        if employee_name:
            queryset = queryset.filter(employee_name__icontains=employee_name)

        # ✅ Sort by employee name (A–Z)
        queryset = queryset.order_by('employee_name', '-created_at')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        # ✅ Get counts of each status in the full (unfiltered) queryset
        all_status_counts = Resignation.objects.values('status').annotate(count=Count('status'))
        status_summary = {status['status']: status['count'] for status in all_status_counts}

        # ✅ Add 0 for any missing status
        for key, _ in Resignation.STATUS_CHOICES:
            status_summary.setdefault(key, 0)

        # ✅ Return paginated response with extra field
        response = self.get_paginated_response(serializer.data)
        response.data["status_counts"] = status_summary
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the resignation
            resignation = serializer.save()
            
            # Prepare data for email
            resignation_data = {
                'employee_name': resignation.employee_name,
                'employee_id': resignation.employee_id,
                'email': resignation.email,
                'branch': resignation.branch,
                'department': resignation.department,
                'designation': resignation.designation,
                'notice_period': resignation.notice_period,
                'resignation_date': resignation.resignation_date,
                'last_working_date': resignation.last_working_date,
                'reason': resignation.reason,
                'status': resignation.status,
                'uuid': str(resignation.uuid)
            }
            
            # Send email notification to HR
            email_sent, email_message = self.email_service.send_resignation_notification(resignation_data)
            
            response_data = {
                "code": 201,
                "message": "Resignation submitted successfully.",
                "data": serializer.data,
                "email_notification": {
                    "sent": email_sent,
                    "message": email_message
                }
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        return Response({
            "code": 400,
            "message": "Invalid data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ✅ GET and PATCH resignation by UUID
class ResignationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Resignation.objects.all()
    serializer_class = ResignationSerializer
    lookup_field = 'uuid'  # Changed from 'id' to 'uuid' for consistency

    def get_object(self):
        try:
            return Resignation.objects.get(uuid=self.kwargs['uuid'])
        except Resignation.DoesNotExist:
            raise NotFound("Resignation not found.")

    def get(self, request, *args, **kwargs):
        resignation = self.get_object()
        serializer = self.get_serializer(resignation)
        return Response({
            "code": 200,
            "message": "Resignation details retrieved.",
            "data": serializer.data
        })

    def patch(self, request, *args, **kwargs):
        resignation = self.get_object()
        serializer = self.get_serializer(resignation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 200,
                "message": "Resignation updated successfully.",
                "data": serializer.data
            })
        return Response({
            "code": 400,
            "message": "Update failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ✅ GET resignations by user UUID
class ResignationByUserUUIDAPIView(APIView):
    def get(self, request, user_uuid):
        resignations = Resignation.objects.filter(uuid=user_uuid).order_by('-created_at')

        if not resignations.exists():
            return Response({
                "code": 404,
                "message": "No resignation found for this user.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        paginator = resignDetailsPagination()
        paginated_resignations = paginator.paginate_queryset(resignations, request)
        serializer = ResignationSerializer(paginated_resignations, many=True)

        return paginator.get_paginated_response(serializer.data)


# ✅ Update resignation status with enhanced notifications and audit trigger
class UpdateResignationStatusAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email_service = EmailService()
    
    def patch(self, request, uuid):
        try:
            resignation = Resignation.objects.get(uuid=uuid)
        except Resignation.DoesNotExist:
            return Response({
                "code": 404,
                "message": "Resignation not found.",
            }, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        valid_statuses = dict(Resignation.STATUS_CHOICES).keys()

        if new_status not in valid_statuses:
            return Response({
                "code": 400,
                "message": f"Invalid status. Allowed values: {', '.join(valid_statuses)}."
            }, status=status.HTTP_400_BAD_REQUEST)

        old_status = resignation.status
        resignation.status = new_status
        resignation.save()

        # Prepare resignation data for notifications
        resignation_data = {
            'employee_name': resignation.employee_name,
            'employee_id': resignation.employee_id,
            'email': resignation.email,
            'branch': resignation.branch,
            'department': resignation.department,
            'designation': resignation.designation,
            'notice_period': resignation.notice_period,
            'resignation_date': resignation.resignation_date,
            'last_working_date': resignation.last_working_date,
            'reason': resignation.reason,
            'status': resignation.status,
            'uuid': str(resignation.uuid)
        }

        # Initialize audit notification variables
        audit_sent = False
        audit_message = "Audit notification not triggered"
        
        # Send status update notification and handle audit trigger
        if old_status != new_status:
            try:
                # Send status update notification to employee
                status_update_html = f"""
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                    <title>Resignation Status Update</title>
                    <!--[if mso]>
                    <noscript>
                        <xml>
                            <o:OfficeDocumentSettings>
                                <o:PixelsPerInch>96</o:PixelsPerInch>
                            </o:OfficeDocumentSettings>
                        </xml>
                    </noscript>
                    <![endif]-->
                </head>
                <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; line-height: 1.6; color: #2c3e50; background-color: #f8f9fa;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; padding: 20px 0;">
                        <tr>
                            <td align="center">
                                <table border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden; max-width: 600px;">
                                    
                                    <!-- Header -->
                                    <tr>
                                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); background-color: #667eea; color: white; padding: 30px; text-align: center;">
                                            <h1 style="margin: 0; font-size: 22px; font-weight: 300; font-family: Arial, sans-serif;">Resignation Status Update</h1>
                                        </td>
                                    </tr>
                                    
                                    <!-- Content -->
                                    <tr>
                                        <td style="padding: 40px 30px;">
                                            
                                            <!-- Greeting -->
                                            <div style="font-size: 16px; margin-bottom: 25px; color: #34495e; line-height: 1.6;">
                                                Dear {resignation.employee_name},<br/><br/>
                                                We hope this message finds you well. We are writing to inform you about an update regarding your resignation application.
                                            </div>
                                            
                                            <!-- Employee Details -->
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; margin: 25px 0;">
                                                <tr>
                                                    <td style="padding: 20px;">
                                                        <div style="font-size: 14px; color: #6c757d; margin-bottom: 15px;">
                                                            <strong>Employee ID:</strong> {resignation.employee_id}<br/>
                                                            <strong>Branch:</strong> {resignation.branch}<br/>
                                                            <strong>Department:</strong> {resignation.department}
                                                        </div>
                                                    </td>
                                                </tr>
                                            </table>
                                            
                                            <!-- Status Update Section -->
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #e8f5e8; border: 1px solid #c3e6c3; border-radius: 6px; margin: 25px 0;">
                                                <tr>
                                                    <td style="padding: 25px; text-align: center;">
                                                        <div style="color: #155724; font-size: 18px; font-weight: 600; margin-bottom: 20px;">Application Status Updated</div>
                                                        
                                                        <!-- Status Change Display -->
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                            <tr>
                                                                <td align="center">
                                                                    <table border="0" cellpadding="10" cellspacing="0" style="margin: 20px auto;">
                                                                        <tr>
                                                                            <td style="padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; background-color: #ffeaa7; color: #6c5701;">{old_status.replace('_', ' ').title()}</td>
                                                                            <td style="padding: 0 15px; font-size: 20px; color: #00b894;">→</td>
                                                                            <td style="padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; background-color: #00b894; color: white;">{new_status.replace('_', ' ').title()}</td>
                                                                        </tr>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            
                                            <!-- Reference Number -->
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; margin: 25px 0;">
                                                <tr>
                                                    <td style="padding: 20px;">
                                                        <div style="font-size: 13px; color: #6c757d; font-weight: 600; margin-bottom: 8px;">APPLICATION REFERENCE NUMBER</div>
                                                        <div style="font-family: 'Courier New', monospace; color: #495057; font-weight: 600;">{str(resignation.uuid)}</div>
                                                    </td>
                                                </tr>
                                            </table>
                                            
                                            <!-- Message -->
                                            <div style="color: #495057; margin-top: 30px; line-height: 1.6;">
                                                If you have any questions regarding this update or need any clarification about your resignation process, 
                                                please feel free to reach out to the HR department. We are here to assist you throughout this transition.
                                            </div>
                                            
                                            <div style="color: #495057; margin-top: 20px;">
                                                Thank you for your understanding and cooperation.
                                            </div>
                                            
                                            <div style="color: #495057; margin-top: 30px;">
                                                Best regards,<br/>
                                                <strong>Human Resources Team</strong>
                                            </div>
                                            
                                        </td>
                                    </tr>
                                    
                                    <!-- Footer -->
                                    <tr>
                                        <td style="background-color: #f8f9fa; padding: 25px 30px; border-top: 1px solid #dee2e6; text-align: center;">
                                            <div style="color: #6c757d; font-size: 13px; margin: 0; line-height: 1.5;">
                                                This is an automated notification from the HR Management System.<br/>
                                                Please do not reply to this email. For any queries, please contact the HR department directly.
                                            </div>
                                        </td>
                                    </tr>
                                    
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
                </html>
                """
                
                employee_mail = Mail(
                    from_email=self.email_service.from_email,
                    to_emails=resignation.email,
                    subject=f"Resignation Application Status Update - {resignation.employee_name}",
                    html_content=status_update_html,
                    plain_text_content=f"""
                    RESIGNATION STATUS UPDATE
                    ========================
                    
                    Dear {resignation.employee_name},
                    
                    We hope this message finds you well. We are writing to inform you about 
                    an update regarding your resignation application.
                    
                    EMPLOYEE DETAILS
                    ---------------
                    Employee ID: {resignation.employee_id}
                    Branch:      {resignation.branch}
                    Department:  {resignation.department}
                    
                    APPLICATION STATUS UPDATED
                    -------------------------
                    Previous Status: {old_status.replace('_', ' ').title()}
                    Current Status:  {new_status.replace('_', ' ').title()}
                    
                    APPLICATION REFERENCE NUMBER
                    ---------------------------
                    {str(resignation.uuid)}
                    
                    If you have any questions regarding this update or need any clarification 
                    about your resignation process, please feel free to reach out to the HR 
                    department. We are here to assist you throughout this transition.
                    
                    Thank you for your understanding and cooperation.
                    
                    Best regards,
                    Human Resources Team
                    
                    ---
                    This is an automated notification from the HR Management System.
                    Please do not reply to this email. For any queries, please contact 
                    the HR department directly.
                    """
                )
                self.email_service.sg.send(employee_mail)
                
                # 🚨 TRIGGER AUDIT NOTIFICATION WHEN STATUS IS APPROVED
                if new_status.lower() == 'approved':
                    audit_sent, audit_message = self.email_service.send_audit_notification(resignation_data)
                
            except Exception as e:
                # Log the error but don't fail the status update
                print(f"Failed to send status update email: {str(e)}")
                
        # Special case: If status changed directly to approved without email sending
        elif new_status.lower() == 'approved':
            audit_sent, audit_message = self.email_service.send_audit_notification(resignation_data)

        response_data = {
            "code": 200,
            "message": "Resignation status updated successfully.",
            "data": {
                "uuid": str(resignation.uuid),
                "status": resignation.status,
                "previous_status": old_status
            }
        }
        
        # Add audit notification info to response if it was triggered
        if new_status.lower() == 'approved':
            response_data["audit_notification"] = {
                "sent": audit_sent,
                "message": audit_message
            }

        return Response(response_data, status=status.HTTP_200_OK)


# ✅ Delete resignation
class DeleteResignationAPIView(APIView):
    def delete(self, request, user_uuid):
        try:
            resignation = Resignation.objects.get(uuid=user_uuid)
        except Resignation.DoesNotExist:
            return Response({
                "code": 404,
                "message": "Resignation not found."
            }, status=status.HTTP_404_NOT_FOUND)

        resignation.delete()

        return Response({
            "code": 200,
            "message": "Resignation deleted successfully."
        }, status=status.HTTP_200_OK)