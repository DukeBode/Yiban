from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, userid, password=None):
        if not userid:
            raise ValueError('用户必须有一个易班id')
        user = self.model(
            userid = userid
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, password):
        user = self.create_user(
            userid,
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    userid = models.CharField('用户id', max_length=25, unique=True)
    access_token = models.CharField('授权凭证', max_length=100)
    expires = models.IntegerField('截止日期', default=0)
    username = models.CharField('用户名', max_length=50)
    usernick = models.CharField('用户昵称', blank=True, max_length=50)
    sex = models.CharField('性别', blank=True, max_length=1)
    userhead = models.URLField('用户头像', blank=True)
    schoolid = models.CharField('所在学校id', blank=True, max_length=25)
    schoolname = models.CharField('所在学校名称', blank=True, max_length=50)
    is_active = models.BooleanField('激活账号', default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    # 作为唯一标识符的描述用户模型字段名的字符串
    USERNAME_FIELD = 'userid'
    # 当通过命令行 createsuperuser 来创建用户时提示的必填字段列表
    # REQUIRED_FIELDS =
    
    class Meta:verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
