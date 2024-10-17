from django.db import models

# Create your models here.
class TALTutorAppModel(models.Model):
    section_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    video_url = models.URLField()
    session_key = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.section_name} created on {self.created} and last modified on {self.modified}"

class ChatMessage(models.Model):
    app = models.ForeignKey(TALTutorAppModel, related_name='messages', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)  # 'user' or 'assistant'
    content = models.TextField()

    def __str__(self):
        return f"{self.role}: {self.content[:30]}..."