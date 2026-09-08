from django.shortcuts import render, redirect, get_object_or_404

from apps.inspector.models import Prospect, ProspectInput


def prospect_dashboard(request):
    prospects = Prospect.objects.all()

    context = {
        "prospects": prospects,
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


def update_prospect_status(request, pk):
    pass


def update_prospect_findings_notes(request, pk):
    pass
