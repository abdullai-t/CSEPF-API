import uuid
from datetime import datetime

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    info = models.JSONField(
        default=dict, blank=True, null=True
    )  # json of social media names and links, etc

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    def to_json(self, full=False, tiny_info=False):
        return {
            "id": str(self.pk),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_deleted": self.is_deleted,
            "info": self.info,
        }


class UserProfile(BaseModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    picture = models.FileField(upload_to="user_profile_pictures", null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.full_name + " - " + self.email

    def to_json(self, full=False, tiny_info=False):
        data = super().to_json()
        data.update(
            {
                "full_name": self.full_name,
                "email": self.email,
                "picture": self.picture.url if self.picture else None,
                "phone_number": self.phone_number,
            }
        )
        return data

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        db_table = "user_profiles"


class Application(BaseModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    school = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="pending")
    cohort = models.CharField(max_length=255, default=datetime.now().year)
    resume = models.FileField(upload_to="resumes", null=True, blank=True)
    picture = models.ImageField(upload_to="applicant_pictures", null=True, blank=True)
    motivation = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.full_name + " - " + self.email

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update(
            {
                "full_name": self.full_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "school": self.school,
                "program": self.program,
                "address": self.address,
                "status": self.status,
                "cohort": self.cohort,
                "resume": self.resume.url if self.resume else None,
                "picture": self.picture.url if self.picture else None,
                "motivation": self.motivation,
            }
        )
        return data

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        db_table = "applications"
        ordering = ["-created_at"]


class Fellow(BaseModel):
    bio = models.TextField(blank=True, null=True)
    has_completed = models.BooleanField(default=False)
    school = models.CharField(max_length=255, blank=True, null=True)
    program = models.CharField(max_length=255, blank=True, null=True)
    cohort = models.CharField(max_length=255, default=datetime.now().year)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    address = models.CharField(max_length=255,blank=True, null=True)
    resume = models.FileField(upload_to="resumes", null=True, blank=True)
    picture = models.ImageField(upload_to="fellow_pictures", null=True, blank=True)
    motivation = models.TextField(blank=True, null=True)

	
    def __str__(self) -> str:
        return self.full_name + " - " + self.email + " - " + self.cohort
	
    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update(
            {
                "bio": self.bio,
                "has_completed": self.has_completed,
                "school": self.school,
                "program": self.program,
                "cohort": self.cohort,
                "full_name": self.full_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "address": self.address,
                "resume": self.resume.url if self.resume else None,
                "picture": self.picture.url if self.picture else None,
                "motivation": self.motivation,
                "project": Project.objects.filter(fellow=self).first().to_json() if Project.objects.filter(fellow=self).first() else None,
            }
        )
        return data
	
    class Meta:
        verbose_name = 'Fellow'
        verbose_name_plural = 'Fellows'
        db_table = "fellows"
        ordering = ['-created_at']


class PolicyTopic(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update({"title": self.title, "description": self.description})
        return data

    class Meta:
        verbose_name = "Policy Topic"
        verbose_name_plural = "Policy Topics"
        db_table = "policy_topics"


class PolicySubTopic(BaseModel):
    topic = models.ForeignKey(
        PolicyTopic, on_delete=models.CASCADE, related_name="sub_topics"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title + " (" + self.topic.title + ")"

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update(
            {
                "topic": self.topic.to_json(),
                "title": self.title,
                "description": self.description,
            }
        )
        return data

    class Meta:
        verbose_name = "Policy Sub Topic"
        verbose_name_plural = "Policy Sub Topics"
        db_table = "policy_sub_topics"


class Project(BaseModel):
    fellow = models.ForeignKey(
        Fellow, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to="projects", null=True, blank=True)
    topics = models.ManyToManyField(PolicySubTopic, related_name="projects")
    is_featured = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update(
            {
                "title": self.title,
                "summary": self.summary,
                "document": self.document.url if self.document else None,
                "topics": [tag.to_json() for tag in self.topics.all()],
                "is_featured": self.is_featured,
                "fellow": {
                    "full_name":self.fellow.full_name,
                    "email":self.fellow.email,
                    "picture":self.fellow.picture.url if self.fellow.picture else None,
                    "id":str(self.fellow.pk),
                    "program":self.fellow.program,
                },
            }
        )
        return data

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        db_table = "projects"
        ordering = ["-created_at"]


class Testimonial(BaseModel):
    fellow = models.ForeignKey(
        Fellow, on_delete=models.CASCADE, related_name="testimonials"
    )
    content = models.TextField()
    media = models.FileField(upload_to="testimonials", null=True, blank=True)
    tags = models.ManyToManyField(PolicySubTopic)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.fellow.full_name + " - " + self.content[:10]

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update(
            {
                "user": self.fellow.to_json(),
                "content": self.content,
                "tags": [tag.to_json() for tag in self.tags.all()],
                "is_published": self.is_published,
                "is_featured": self.is_featured,
                "media": self.media.url if self.media else None,
            }
        )
        return data

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        db_table = "testimonials"
        ordering = ["-created_at"]


class Presentation(BaseModel):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to="presentations", null=True, blank=True)
    presenter = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    picture = models.ImageField(upload_to="presenter_pictures", null=True, blank=True)
    cohort = models.CharField(max_length=255, default=datetime.now().year)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update(
            {
                "title": self.title,
                "media": self.document.url if self.document else None,
                "is_published": self.is_published,
                "presenter": self.presenter,
                "email": self.email,
                "picture": self.picture.url if self.picture else None,
                "is_featured": self.is_featured,
                "summary": self.summary,
            }
        )
        return data

    class Meta:
        verbose_name = "Presentation"
        verbose_name_plural = "Presentations"
        db_table = "presentations"
        ordering = ["-created_at"]


class SiteTrip(BaseModel):
    location = models.CharField(max_length=255)
    date = models.DateField()
    summary = models.TextField(blank=True, null=True)
    cohort = models.CharField(max_length=255, default=datetime.now().year)

    def __str__(self) -> str:
        return self.location + " - " + str(self.date)

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update(
            {
                "location": self.location,
                "date": self.date,
                "summary": self.summary,
                "cohort": self.cohort,
                "images": [image.to_json() for image in self.images.all()],
            }
        )
        return data


class SiteTripImage(BaseModel):
    trip = models.ForeignKey(SiteTrip, on_delete=models.CASCADE, related_name="images")
    image = models.FileField(upload_to="site_trip_images")

    def __str__(self) -> str:
        return self.trip.location + " - " + self.image.url

    def to_json(self, full=False, tiny_info=False) -> dict:
        data = super().to_json()
        data.update({"image": self.image.url})
        return data
