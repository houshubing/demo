from django.db import models

from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    @property
    def auth(self):
        if  not hasattr(self, '_auth'):  # hasattr检查有没有('_auth)属性
            self._auth = User.objects.get(id=self.uid)
        return self._auth

