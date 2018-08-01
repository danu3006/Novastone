from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Task(models.Model):
    """
    Stores a single task which has relationships with :model:'auth.User' model.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)

    # Fields
    name = models.CharField(max_length=25)
    description = models.TextField(verbose_name='Description')
    status = models.BooleanField(default=False)

    # Relational Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_set')
    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='task_done_by_set', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_status(self):
        """
        Constructs string based of status of task.
        :return: string
        """
        return 'Complete' if self.status else 'Incomplete'


@receiver(pre_save, sender=Task)
def update_done_by(sender, instance, **kwargs):
    if not instance.status and instance.done_by:
        instance.done_by = None
