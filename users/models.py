from django.db import models

# Create your models here.
class User(models.Model):
  firstName = models.CharField(max_length = 50, null = False, blank = False)
  lastName = models.CharField(max_length = 50, null = False, blank = False)
  password = models.CharField(max_length = 50, null = False, blank = False)
  email = models.EmailField()
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)
  
  def __getData__(self):
    postData = "%s %s" % (self.name)
    return postData