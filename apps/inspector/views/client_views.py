from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator


from apps.inspector.models import Prospect, ProspectInput
from apps.inspector.selectors import get_prospect_dashboard_queryset


def prospect_dashboard(request):
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    prospects = get_prospect_dashboard_queryset(
        search=search,
        status=status,
    )

    paginator = Paginator(prospects, 25)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "prospects": page_obj,
        "search": search,
        "status": status,
        "status_choices": Prospect.Status.choices,
    }

    return render(
        request,
        "inspector/dashboard.html",
        context,
    )


def prospect_detail(request, pk):
    prospect = get_object_or_404(
        Prospect,
        pk=pk,
    )

    context = {
        "prospect": prospect,
    }

    return render(
        request,
        "inspector/prospect_details.html",
        context,
    )


def add_new_prospect(request):
    if request.method == "POST":
        user_input = request.POST.get(
            "user-input",
            "",
        ).strip()

        profile_link = request.POST.get(
            "profile-link",
            "",
        ).strip()

        if user_input and profile_link:
            ProspectInput.objects.create(
                content=user_input,
                profile_url=profile_link,
            )

            return redirect("prospect_dashboard")

    return render(
        request,
        "inspector/new_prospect.html",
    )


def update_prospect(request, pk):
    prospect = get_object_or_404(
        Prospect,
        pk=pk,
    )

    if request.method == "POST":
        prospect.findings = request.POST.get(
            "findings",
            "",
        ).strip()

        prospect.notes = request.POST.get(
            "notes",
            "",
        ).strip()

        status = request.POST.get("status")

        if status in Prospect.Status.values:
            prospect.status = status

        prospect.save()

        return redirect(
            "prospect_detail",
            pk=prospect.pk,
        )

    return render(
        request,
        "inspector/update_prospect.html",
        {
            "prospect": prospect,
        },
    )
