# posts/models.py

from __future__ import unicode_literals

from django.db import models

class Post(models.Model):
  name = models.CharField(max_length=224, null=False, blank=False)
  content = models.TextField(max_length=254, null=False, blank=False)
  author = models.ForeignKey('users', on_delete= models.CASCADE)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)

  def __getData__(self):
    postData = "%s %s" % (self.name, self.content)
    return postData

#ondelete child data will be deleted wwhen the parent data deleted