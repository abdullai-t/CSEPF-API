import uuid
from datetime import datetime

from django.db import models


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_deleted = models.BooleanField(default=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	info = models.JSONField(default=dict)
	
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
	picture = models.ImageField(upload_to='user_profile_pictures', null=True, blank=True)
	phone_number = models.CharField(max_length=20, null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	
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
			"cohort": self.cohort
		})
		return data
	
	class Meta:
		verbose_name = 'Application'
		verbose_name_plural = 'Applications'
		db_table = "applications"
		ordering = ['-created_at']


class Fellow(BaseModel):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	is_completed = models.BooleanField(default=False)
	cohort = models.CharField(max_length=255, default=datetime.now().year)
	program = models.CharField(max_length=255)
	school = models.CharField(max_length=255)
	
	def __str__(self) -> str:
		return self.user.full_name + " - " + self.cohort
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"user": self.user.to_json(),
			"is_completed": self.is_completed,
			"cohort": self.cohort,
			"program": self.program,
			"school": self.school
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
		return self.title
	
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


class Testimonial(BaseModel):
	user = models.ForeignKey(Fellow, on_delete=models.CASCADE, related_name='testimonials')
	content = models.TextField()
	media = models.ImageField(upload_to='testimonials', null=True, blank=True)
	tags = models.ManyToManyField(PolicySubTopic)
	is_published = models.BooleanField(default=False)
	is_featured = models.BooleanField(default=False)
	
	def __str__(self) -> str:
		return self.user.full_name + " - " + self.content[:10]
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"user": self.user.to_json(),
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
	content = models.TextField(blank=True, null=True)
	media = models.FileField(upload_to='presentations')
	tags = models.ManyToManyField(PolicySubTopic, related_name='presentations')
	presenter = models.CharField(max_length=255)
	is_published = models.BooleanField(default=False)
	link = models.URLField(blank=True, null=True)
	is_featured = models.BooleanField(default=False)
	
	def __str__(self) -> str:
		return self.title
	
	def to_json(self, full=False, tiny_info=False) -> dict:
		data = super().to_json()
		data.update({
			"title": self.title,
			"media": self.media.url,
			"tags": [tag.to_json() for tag in self.tags.all()],
			"is_published": self.is_published,
			"link": self.link,
			"presenter": self.presenter,
			"is_featured": self.is_featured,
			"content": self.content,
		})
		return data
	
	class Meta:
		verbose_name = 'Presentation'
		verbose_name_plural = 'Presentations'
		db_table = "presentations"
		ordering = ['-created_at']