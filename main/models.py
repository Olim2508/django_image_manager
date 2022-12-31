from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ImageModel(BaseModel):
    image = models.ImageField(upload_to='images')
    geo_location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # todo add people field which contains the people in image ["aleks", "john"]

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.description


# class Person(BaseModel):
#     name = models.CharField(max_length=255)
#     image = models.ForeignKey(ImageModel, related_name='person', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name_plural = 'People'
