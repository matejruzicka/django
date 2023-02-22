from faker import Faker
import django

django.setup()
faker = Faker()

from app.models import Blog, Comment, Category

print(faker.name())
print(faker.first_name())

# hue: 'monochrome', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', and 'pink'
# luminosity: 'bright', 'dark', 'light', or 'random'
print(faker.color(hue='blue', luminosity='bright'))

print(faker.paragraph(nb_sentences=12))


# for _ in range(0, 500):
#     Blog.objects.create(title=faker.sentence(), body=faker.paragraph(nb_sentences=12))

# for blog in Blog.objects.iterator():
#     comments = [Comment(text=faker.paragraph(), blog=blog) for _ in range(0, 3)]
#     Comment.objects.bulk_create(comments)

print(Comment.objects.count())

Category.objects.create(name='Web development')
Category.objects.create(name='Databases')
Category.objects.create(name='Data science')
Category.objects.create(name='Security')
Category.objects.create(name='Python')
Category.objects.create(name='Django')
