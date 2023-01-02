from django.db import models


class ImageModel(models.Model):
    image = models.ImageField(upload_to="images")
    geo_location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.description


class Person(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.id}-{self.name} -- {self.image.description}"

    class Meta:
        verbose_name_plural = "People"
