from tasks.models import Task
from django.db.models.signals import post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
#new part start 
#signals
@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employee_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in instance.assigned_to.all() if emp.email]
        
        if assigned_emails: # Only try to send if there are recipients
            send_mail(
                'New task assigned',
                f'You have been assigned to the task: {instance.title}',
                'mdarmanislam20021@gmail.com',
                assigned_emails,
                fail_silently=True, # Recommended for production
            )

            
@receiver(post_delete, sender=Task)
def delete_assosiate_details(sender, instance, **kwargs):
    # hasattr safely checks if the 'details' relation exists
    if hasattr(instance, 'details'):
        instance.details.delete()
        print(f"Details for {instance.title} deleted successfully")
    else:
        print(f"No details found for {instance.title}, skipping deletion")