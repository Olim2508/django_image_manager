from typing import List

from main.models import ImageModel, Person


class ImageService:
    @staticmethod
    def add_bulk_people_to_image(people: List[str], image: ImageModel):
        people: list = [Person(image=image, name=p_name) for p_name in people]
        Person.objects.bulk_create(people)
