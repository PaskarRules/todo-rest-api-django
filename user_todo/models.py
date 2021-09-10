from django.db import models

from user_management.models import User


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="todos")
    title = models.CharField(max_length=250)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.title}"

    class Meta:
        db_table = "todo"
