from django.db.models.signals import post_save
from django.dispatch import receiver
from BindingCourse.models import BindingCourse
from Course.models import Course
from BindingBook.models import BindingBook
from Book.models import Book
from Course.models import StudentCourseRank
from django.db.models import Avg
from BindingMeeting.models import BindingMeeting
from Meeting.models import Meeting
from django.db.models.signals import post_delete


# @receiver(post_save, sender=BindingCourse)
# def create_or_update_course(sender, instance, created=False, **kwargs):
#     if instance.approved:
#         # Check if a corresponding Course object already exists
#         try:
#             course = Course.objects.get(binding_course=instance)
#             course.title = instance.title
#             course.description = instance.description
#             course.created_by = instance.created_by
#             course.price = instance.price
#             course.imageURL = instance.imageURL
#             course.videoFile = instance.videoFile
#             course.category = instance.category
#             course.demo = instance.demo
#             course.videos.set(instance.videos)
#             course.save()
#         except Course.DoesNotExist:
#             # If it doesn't exist, create a new Course object
#             course = Course.objects.create(
#                 title=instance.title,
#                 description=instance.description,
#                 created_by=instance.created_by,
#                 price=instance.price,
#                 imageURL=instance.imageURL,
#                 videoFile=instance.videoFile,
#                 category=instance.category,
#                 demo=instance.demo,
#                 videos=instance.videos,
#                 binding_course=instance  # assuming Course model has a ForeignKey to BindingCourse
#             )
from django.db.models.signals import post_save
from django.dispatch import receiver

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
            course.videos.set(instance.videos.all())  # Use .all() to get all related videos
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
            course.videos.set(instance.videos.all())  # Set the many-to-many relationship

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
@receiver(post_save, sender=StudentCourseRank)
def update_course_rank(sender, instance, created, **kwargs):
    course = instance.course
    average_rank = course.student_ranks.aggregate(Avg('rank'))['rank__avg']
    course.average_rank = average_rank
    course.save()

       



@receiver(post_save, sender=BindingMeeting)
def create_or_update_meeting(sender, instance, created=False, **kwargs):

    if instance.approved:
        print('yes approved')
        # Check if a corresponding Course object already exists
        try:
            meeting = Meeting.objects.get(binding_meeting=instance)
            meeting.date_time = instance.date_time
            meeting.student = instance.student
            meeting.employee = instance.employee
            meeting.message = instance.message
            meeting.accepted=True
            meeting.save()
            print(instance.approved)
        except Meeting.DoesNotExist:
            print('new')

            meeting = Meeting.objects.create(
                date_time=instance.date_time,
                student=instance.student,
                employee=instance.employee,
                message=instance.message,
                accepted=True,
                binding_meeting=instance  # assuming Course model has a ForeignKey to BindingCourse
            )
            meeting.save()


@receiver(post_delete, sender=BindingMeeting)
def create_meeting_on_deletion(sender, instance, **kwargs):
    # Since the original BindingMeeting is deleted, you cannot link the new Meeting to it.
    # You can still create a new Meeting possibly related to another BindingMeeting or without any direct link.
    
    # Create a new Meeting object with default or specified attributes
    if instance.approved==False:
        new_meeting = Meeting.objects.create(
            date_time=instance.date_time if hasattr(instance, 'date_time') else None,
            student=instance.student if hasattr(instance, 'student') else None,
            employee=instance.employee if hasattr(instance, 'employee') else None,
            message=instance.message,
            accepted=False,
            
            # Do not link binding_meeting as the original is deleted
        )
        new_meeting.save()
    
    # Optionally, if your model allows nullable or default BindingMeeting, you might set it here
    # new_meeting.binding_meeting = some_default_binding_meeting
    # new_meeting.save()


# @receiver(post_delete, sender=BindingMeeting)
# def create_or_update_new_meeting(sender, instance, created=False, **kwargs):
#     if instance.approved==False and created==False:
#         print('false')

#         try:
#             meeting = Meeting.objects.get(binding_meeting=instance)
#             meeting.date_time = instance.date_time
#             meeting.student = instance.student
#             meeting.employee = instance.employee
#             meeting.message = instance.message
#             meeting.accepted=False
#             meeting.save()
#         except Meeting.DoesNotExist:
#             # If it doesn't exist, create a new Course object
#             meeting = Meeting.objects.create(
#                 date_time=instance.date_time,
#                 student=instance.student,
#                 employee=instance.employee,
#                 message=instance.message,
#                 accepted=False,
#                 binding_meeting=instance  # assuming Course model has a ForeignKey to BindingCourse
#             )
#             meeting.save()