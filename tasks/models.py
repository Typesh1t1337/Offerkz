from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    time_created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isAgreed = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.PROTECT,null=True, blank=True)


    def __str__(self):
        return self.title

class AssignedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='assigned_task')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,default="Assigned",choices=[('Assigned','Assigned'), ('Not Assigned','not assigned'),("completed","Completed"),("In Progress","In Progress")])
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['task', 'user'], name='unique_assigned_task')
        ]

class Category(models.Model):
    type = models.CharField(max_length=100,db_index=True)

    def __str__(self):
        return self.type


class Chat(models.Model):
     first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False,related_name="chats_as_first_user_id")
     second_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False,related_name="chats_as_second_user_id")
     latest_message = models.TextField(null=True)
     task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='chats', null=True)



     def __str__(self):
         return f"Message between {self.first_user_id} and {self.second_user_id}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="sender_id")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="receiver_id")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='messages',null=True,blank=True)

    def __str__(self):
        return self.message













