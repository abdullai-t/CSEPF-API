from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from database.models import Application
from django.db.models import Q
import random


def applications_list(request):
    query = request.GET.get("q")
    if query:
        applications = Application.objects.filter(
            Q(full_name__icontains=query) | Q(email__icontains=query)
        )
    else:
        applications = Application.objects.all()

    paginator = Paginator(applications, 15)  # Show 10 applications per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "applications_list.html", {"page_obj": page_obj, "query": query}
    )


def update_status(request):
    if request.method == "POST":
        application_id = request.POST.get("application_id")
        status = request.POST.get("status")
        application = Application.objects.get(id=application_id)
        application.status = status
        #TODO: create a fellow on status success and send email or send a rejection email
        application.save()
        return redirect("applications")


def delete_application(request, id):
    application = Application.objects.get(id=id)
    application.delete()
    return redirect("applications")
