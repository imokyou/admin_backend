# coding=utf8
from django.db import models


class User(models.Model):
    
    """
    网站的注册用户表
    """
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'user'


class ApiKey(models.Model):
    
    """
    接口的apikey表
    """
    owner =  models.CharField(max_length=128)
    key = models.CharField(max_length=128)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'apikey'