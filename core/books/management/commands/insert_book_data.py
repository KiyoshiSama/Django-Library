import random
from faker import Faker
from django.core.management.base import BaseCommand
from books.models import Author, Book, Category, Publisher

category_list = ["hi-fi", "crime", "thriller", "horror"]


class Command(BaseCommand):
    help = "Creating book info..."

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        authors_list = []

        # Create 5 authors
        for _ in range(5):
            author = Author.objects.create(name=self.fake.name())
            authors_list.append(author)

        for name in category_list:
            Category.objects.get_or_create(name=name)

        for _ in range(5):
            publisher = Publisher.objects.create(
                name=self.fake.company(),
                address=self.fake.address()
            )
            category = Category.objects.get(name=random.choice(category_list))
            book = Book.objects.create(
                title=self.fake.sentence(),
                description=self.fake.paragraph(nb_sentences=5),
                publisher=publisher,
                category=category,
                publish_date=self.fake.date(),
                page_number=self.fake.random_int(min=100, max=1000),
                is_available=True,
            )
            # Randomly assign between 1 to 3 authors to each book
            book.authors.set(random.sample(authors_list, random.randint(1, 3)))

