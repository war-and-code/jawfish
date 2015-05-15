from django.db import models

class Attempt(models.Model):
    target = models.CharField(max_length=200)
    addr = models.CharField(max_length=200)
    vuln_var = models.CharField(max_length=200)
    method = models.CharField(max_length=200)
    goal_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.target
    