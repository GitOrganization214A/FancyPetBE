from django.core.management.base import BaseCommand
from FancyPet.models import Article


class Command(BaseCommand):
    help = 'Populate initial data for Article model'

    def handle(self, *args, **kwargs):
        # Your data initialization logic
        Article.objects.create(
            openid='ob66w612B_fnXnoIqnIGPvfy6HxY',
            title='hello',
            content='想做zzgg的狗',
            image="example_image.jpg",
            like=10,
            comment=5,
            read=100
        )

        # Add more entries as needed
