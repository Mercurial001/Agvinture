from django.db import models


class Trees(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Lot(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlantedStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Geolocation(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    date = models.DateField()
    date_time = models.DateTimeField()
    tree = models.ForeignKey(Trees, related_name='tree_type', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='section', on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, related_name='lot', on_delete=models.CASCADE)
    status = models.ForeignKey(PlantedStatus, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-date_time']
