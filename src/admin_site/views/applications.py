import datetime
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from _main_.utils.utils import send_universal_email
from database.models import Application, Fellow
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
        # create a fellow if status is accepted and send a success email else send a rejection email
        if status.lowercase() == "approved":
            # create a fellow
            # fellow = Fellow.objects.create(
                
            # )
            # send a success email
            send_universal_email(
                [application.email],
                f"CSEPF {datetime.now().year} Application Decision",
                "application_approval_email.html",
                {
                    "full_name": application.full_name,
                    "email": application.email,
                    "status": status,
                },
            )
        else:
            # send a rejection email
            send_universal_email(
                [application.email],
                f"CSEPF {datetime.now().year} Application Decision",
                "application_rejection_email.html",
                {
                    "full_name": application.full_name,
                    "email": application.email,
                    "status": status,
                },
            )
            
        application.status = status
        application.save()
        return redirect("applications")


def delete_application(request, id):
    application = Application.objects.get(id=id)
    application.delete()
    return redirect("applications")
