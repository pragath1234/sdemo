from django.db import models


class Person(models.Model):
    RIN = models.CharField(max_length=100, blank=True)
    GSTN = models.CharField(max_length=100, blank=True)
    INVOICEDATE = models.CharField(max_length=100, blank=True)
    TOTALGST = models.CharField(max_length=100, blank=True)
    MonthofPayment = models.CharField(max_length=100, blank=True)
