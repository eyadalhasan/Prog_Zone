from django.db.models.signals import post_save
from django.dispatch import receiver
from BindingCourse.models import BindingCourse
from Course.models import Course
from BindingBook.models import BindingBook
from Book.models import Book

@receiver(post_save, sender=BindingCourse)
def create_or_update_course(sender, instance, created=False, **kwargs):
    if instance.approved:
        # Check if a corresponding Course object already exists
        try:
            course = Course.objects.get(binding_course=instance)
            course.title = instance.title
            course.description = instance.description
            course.created_by = instance.created_by
            course.price = instance.price
            course.imageURL = instance.imageURL
            course.videoFile = instance.videoFile
            course.category = instance.category
            course.demo = instance.demo
            course.save()
        except Course.DoesNotExist:
            # If it doesn't exist, create a new Course object
            course = Course.objects.create(
                title=instance.title,
                description=instance.description,
                created_by=instance.created_by,
                price=instance.price,
                imageURL=instance.imageURL,
                videoFile=instance.videoFile,
                category=instance.category,
                demo=instance.demo,
                binding_course=instance  # assuming Course model has a ForeignKey to BindingCourse
            )
@receiver(post_save, sender=BindingBook)
def create_or_update_book(sender, instance, created=False, **kwargs):
    if instance.approved:
        # Check if a corresponding book object already exists
        try:
            book = Book.objects.get(binding_book=instance)
            book.course = instance.course
            book.title = instance.title
            book.author = instance.author
            book.link = instance.link
            book.binding_book = instance

            book.save()
        except Book.DoesNotExist:
            # If it doesn't exist, create a new book object
            book = Book.objects.create(
                course=instance.course,
                title=instance.title,
                author=instance.author,
                link=instance.link,
                binding_book=instance,
            )
       
