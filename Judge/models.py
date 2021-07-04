from django.db import models


class EmailUser(models.Model):
    user = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = "emailuser"
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.user


class EmailContent(models.Model):
    send_user = models.CharField(max_length=32)
    receive = models.CharField(max_length=32)
    content = models.TextField()
    category = models.SmallIntegerField(default=0)
    email_title = models.CharField(max_length=128)
    datatime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "emailcontent"
        verbose_name = "邮件"
        verbose_name_plural = "邮件"

    def __str__(self):
        return self.email_title
