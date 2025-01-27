from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    users = models.ManyToManyField(User, related_name="Chats")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        users = ", ".join([user.username for user in self.users.all()])

        return f"Chat entre: {users}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="Messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ["-timestamp"]

    def __str__(self):
        return f"{self.sender.username}: {self.content}"
