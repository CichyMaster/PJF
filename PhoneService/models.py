from django.db import models


class Phones(models.Model):
    id_phone = models.AutoField(primary_key=True)
    producer = models.CharField(max_length=10)
    model = models.CharField(max_length=25)
    designation = models.CharField(max_length=15)

    def __str__(self):
        return self.model

    class Meta:
        managed = False
        db_table = 'Phones'


class Workers(models.Model):
    id_worker = models.AutoField(primary_key=True)
    acronym = models.CharField(max_length=4)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)

    def __str__(self):
        return self.acronym

    class Meta:
        managed = False
        db_table = 'Workers'


class Repairs(models.Model):
    id_repair = models.AutoField(primary_key=True)
    id_phone = models.ForeignKey(Phones, on_delete=models.CASCADE, db_column='id_phone')
    id_worker = models.ForeignKey(Workers, on_delete=models.CASCADE, db_column='id_worker')
    nr_case = models.CharField(max_length=9)
    imei = models.BigIntegerField(default=0)
    admission_date = models.DateField("data przyjęcia")
    operator = models.CharField(max_length=15)
    end_date = models.DateField("data zakonczenia")
    status = models.CharField(max_length=15)

    def __str__(self):
        return self.nr_case

    class Meta:
        managed = False
        db_table = 'Repairs'
