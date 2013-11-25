from django.db import models


class Simple(models.Model):

    str_attr = models.CharField(max_length=20)
    int_attr = models.IntegerField()
    date_attr = models.DateTimeField()


class Key(models.Model):

    f_key = models.ForeignKey('Simple', related_name='key')
    m2m = models.ManyToManyField('Simple', related_name='keys')
