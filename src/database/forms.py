from django import forms

from _main_.utils.constants import SCHOOLS

from .models import (
    Fellow,
    Presentation,
    Project,
    SiteTrip,
    Testimonial,
    UserProfile,
    SiteTripImage,
)


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["fellow", "content", "media", "is_featured", "tags"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 5}),
            "tags": forms.CheckboxSelectMultiple(),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["fellow", "title", "summary", "document", "is_featured", "topics"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 5}),
            "topics": forms.CheckboxSelectMultiple(),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["full_name", "email", "picture"]


class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = [
            "title",
            "presenter",
            "email",
            "picture",
            "cohort",
            "summary",
            "document",
            "is_featured",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 5}),
        }


class SiteTripForm(forms.ModelForm):
    class Meta:
        model = SiteTrip
        fields = ["location", "summary", "date", "cohort"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 5}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class SiteTripImageForm(forms.ModelForm):
    class Meta:
        model = SiteTripImage
        fields = ["trip", "image"]


class FellowForm(forms.ModelForm):
    class Meta:
        model = Fellow
        fields = ["full_name", "email", "picture", "bio", "school","program", "cohort", "address", "phone_number", "resume", "has_completed"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "bio": forms.Textarea(attrs={"rows": 5}),
            "school": forms.Select(choices=[(school, school) for school in SCHOOLS]),
            "program": forms.TextInput(attrs={"placeholder": "Ms. Computer Science"}),
            "cohort": forms.TextInput(attrs={"placeholder": "2020"}),
        }
