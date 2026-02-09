from tasks.models import Task
from django.db.models.signals import post_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
#new part start 
#signals
@receiver(m2m_changed,sender=Task.assigned_to.through)
def notify_employee_on_task_creation(sender,instance,action,**kwargs):
    if action == 'post_add':
        assigned_emails=[emp.email for emp in instance.assigned_to.all()]
       

        send_mail(
            'New task assigned',
            f'You have been assigned to the task: {instance.title}',
            'mdarmanislam20021@gmail.com',        # From
            assigned_emails,        # To
            
)

@receiver(post_delete,sender=Task)
def delete_assosiate_details(sender,instance,**kwargs):
    if instance.details:
        print(instance)
        instance.details.delete()
        print("deleted successfully")
