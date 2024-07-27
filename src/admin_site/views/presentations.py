from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from database.forms import PresentationForm
from database.models import Presentation


def add_presentation(request):
    if request.method == "POST":
        form = PresentationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    return redirect("presentations")  # Adjust the redirect as necessary


def update_presentation(request, id):
    if request.method == "POST":
        presentation = Presentation.objects.get(id=id)
        form = PresentationForm(request.POST, request.FILES, instance=presentation)
        if form.is_valid():
            form.save()

    return redirect("presentations")  # Adjust the redirect as necessary


def delete_presentation(request, id):
    presentation = Presentation.objects.get(id=id)
    presentation.delete()

    return redirect("presentations")  # Adjust the redirect as necessary


def presentations_list(request):
    query = request.GET.get("q")
    if query:
        presentations = Presentation.objects.filter(Q(presnter__icontains=query))
    else:
        presentations = Presentation.objects.all()

    paginator = Paginator(presentations, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for p in page_obj:
        p.picture_url = p.picture.url if p.picture else ""
        p.document_url = p.document.url if p.document else ""

    form = PresentationForm()

    return render(
        request,
        "presentations_list.html",
        {"page_obj": page_obj, "query": query, "form": form},
    )
