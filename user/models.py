from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('U', '保密'),
    )
    nickname = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    icon = models.ImageField()
    plt_icon = models.CharField(max_length=256, default='') #存储微博头像地址

    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=8, choices=SEX)
    perm_id = models.IntegerField()

    @property
    def avatar(self):
        if self.icon:
            return self.icon.url
        else:
            return self.plt_icon

    @property
    def perm(self):
        if not hasattr(self, '_perm'):  # hasattr检查有没有('_perm)属性
            self._perm = Permission.objects.get(id=self.perm_id)
        return self._perm

    def has_perm(self, perm_name):
        need_perm = Permission.objects.get(name=perm_name)
        return self.perm.level >= need_perm.level


class Permission(models.Model):
    level = models.IntegerField()
    name = models.CharField(max_length=16, unique=True)