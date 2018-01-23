from django.db import models

class Situation(models.Model):
    title = models.CharField(max_length=30)
    situation_text = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Choice(models.Model):
    situation = models.ForeignKey(Situation, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    next_situation = models.ForeignKey(Situation, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.choice_text
