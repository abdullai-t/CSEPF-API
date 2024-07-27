import uuid
from datetime import datetime

from django.db import models


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_deleted = models.BooleanField(default=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	info = models.JSONField(default=dict, blank=True, null=True) #json of social media names and links, etc
	
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
			"info": self.info
		}


class UserProfile(BaseModel):
	full_name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	picture = models.FileField(upload_to='user_profile_pictures', null=True, blank=True)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	def __str__(self):
		return self.full_name + " - " + self.email
	
	def to_json(self, full=False, tiny_info=False):
		data = super().to_json()
		data.update({
			"full_name": self.full_name,
			"email": self.email,
			"picture": self.picture.url if self.picture else None,
			"phone_number": self.phone_number,
			"bio": self.bio
		})
		return data
	
	class Meta:
		verbose_name = 'User Profile'
		verbose_name_plural = 'User Profiles'
		db_table = "user_profiles"



class Application(BaseModel):
	full_name = models.CharField(max_length=255)
	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=20)
	school = models.CharField(max_length=255)
	program = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	status = models.CharField(max_length=255, default='pending')
	cohort = models.CharField(max_length=255, default=datetime.now().year)
	resume = models.FileField(upload_to='resumes', null=True, blank=True)
	picture = models.ImageField(upload_to='applicant_pictures', null=True, blank=True)
	motivation = models.TextField(blank=True, null=True)
	
	def __str__(self) -> str:
		return self.full_name + " - " + self.email
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
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
			"motivation": self.motivation
		})
		return data
	
	class Meta:
		verbose_name = 'Application'
		verbose_name_plural = 'Applications'
		db_table = "applications"
		ordering = ['-created_at']


class Fellow(BaseModel):
	user = models.ForeignKey(Application, on_delete=models.CASCADE)
	bio = models.TextField(blank=True, null=True)
	is_completed = models.BooleanField(default=False)
	# cohort = models.CharField(max_length=255, default=datetime.now().year)
	# program = models.CharField(max_length=255)
	# school = models.CharField(max_length=255)
	# resume = models.FileField(upload_to='resumes', null=True, blank=True)
	
	def __str__(self) -> str:
		return self.user.full_name + " - " + self.user.cohort
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"user": self.user.to_json(),
			"is_completed": self.is_completed,
			# "cohort": self.cohort,
			# "program": self.program,
			# "school": self.school
		})
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
		verbose_name = 'Policy Topic'
		verbose_name_plural = 'Policy Topics'
		db_table = "policy_topics"


class PolicySubTopic(BaseModel):
	topic = models.ForeignKey(PolicyTopic, on_delete=models.CASCADE, related_name='sub_topics')
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	
	def __str__(self) -> str:
		return self.title + " (" + self.topic.title + ")"
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"topic": self.topic.to_json(),
			"title": self.title,
			"description": self.description
		})
		return data
	
	class Meta:
		verbose_name = 'Policy Sub Topic'
		verbose_name_plural = 'Policy Sub Topics'
		db_table = "policy_sub_topics"
		

class Project(BaseModel):
	fellow = models.ForeignKey(Fellow, on_delete=models.CASCADE, related_name='projects')
	title = models.CharField(max_length=255)
	summary = models.TextField(blank=True, null=True)
	document = models.FileField(upload_to='projects', null=True, blank=True)
	topics = models.ManyToManyField(PolicySubTopic, related_name='projects')
	is_featured = models.BooleanField(default=False)
	
	def __str__(self) -> str:
		return self.title
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"title": self.title,
			"description": self.summary,
			"media": self.media.url if self.media else None,
			"tags": [tag.to_json() for tag in self.tags.all()],
			"is_published": self.is_published,
			"is_featured": self.is_featured
		})
		return data
	
	class Meta:
		verbose_name = 'Project'
		verbose_name_plural = 'Projects'
		db_table = "projects"
		ordering = ['-created_at']


class Testimonial(BaseModel):
	fellow = models.ForeignKey(Fellow, on_delete=models.CASCADE, related_name='testimonials')
	content = models.TextField()
	media = models.FileField(upload_to='testimonials', null=True, blank=True)
	tags = models.ManyToManyField(PolicySubTopic)
	is_published = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	
	def __str__(self) -> str:
		return self.fellow.user.full_name + " - " + self.content[:10]
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"user": self.fellow.to_json(),
			"content": self.content,
			"tags": [tag.to_json() for tag in self.tags.all()],
			"is_published": self.is_published,
			"is_featured": self.is_featured,
			"media": self.media.url if self.media else None
		})
		return data
	
	class Meta:
		verbose_name = 'Testimonial'
		verbose_name_plural = 'Testimonials'
		db_table = "testimonials"
		ordering = ['-created_at']
	

class Staff(BaseModel):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	role = models.CharField(max_length=255)
	bio = models.TextField(blank=True, null=True)
	is_featured = models.BooleanField(default=False)
	
	def __str__(self) -> str:
		return self.user.full_name + " - " + self.role
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"user": self.user.to_json(),
			"role": self.role,
			"bio": self.bio,
			"is_featured": self.is_featured
		})
		return data
	
	class Meta:
		verbose_name = 'Staff'
		verbose_name_plural = 'Staff'
		db_table = "staff"
		ordering = ['-created_at']


class Presentation(BaseModel):
	title = models.CharField(max_length=255)
	summary = models.TextField(blank=True, null=True)
	document = models.FileField(upload_to='presentations', null=True, blank=True)
	presenter = models.CharField(max_length=255)
	email = models.EmailField(blank=True, null=True)
	picture = models.ImageField(upload_to='presenter_pictures', null=True, blank=True)
	cohort = models.CharField(max_length=255, default=datetime.now().year)
	is_published = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	
	def __str__(self) -> str:
		return self.title
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"title": self.title,
			"media": self.document.url,
			"is_published": self.is_published,
			"presenter": self.presenter,
			"email": self.email,
			"picture": self.picture.url if self.picture else None,
			"is_featured": self.is_featured,
			"summary": self.summary,
		})
		return data
	
	class Meta:
		verbose_name = 'Presentation'
		verbose_name_plural = 'Presentations'
		db_table = "presentations"
		ordering = ['-created_at']
		
		
class SiteTrip(BaseModel):
	location = models.CharField(max_length=255)
	date = models.DateField()
	summary = models.TextField(blank=True, null=True)
	cohort = models.CharField(max_length=255, default=datetime.now().year)
	
	def __str__(self) -> str:
		return self.location + " - " + str(self.date)
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"location": self.location,
			"date": self.date,
			"summary": self.summary,
			"cohort": self.cohort,
			"images": [image.to_json() for image in self.images.all()]
		})
		
		
class SiteTripImage(BaseModel):
	trip = models.ForeignKey(SiteTrip, on_delete=models.CASCADE, related_name='images')
	image = models.FileField(upload_to='site_trip_images')
	
	def __str__(self) -> str:
		return self.trip.location + " - " + self.image.url
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"trip": self.trip.to_json(),
			"image": self.image.url
		})