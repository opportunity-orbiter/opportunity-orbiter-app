from django.db import models

# Create your models here.
# Create a simple model for a crawled webpage


class Webpage(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField("date published")

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:100]

    def pub_date_pretty(self):
        return self.date.strftime("%b %e %Y")
