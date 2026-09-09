from apps.inspector.models import Prospect


def get_prospect_dashboard_queryset(search=None, status=None):
    queryset = (
        Prospect.objects.select_related("business")
        .prefetch_related("business__tags")
        .only(
            "id",
            "name",
            "status",
            "business__industry",
        )
        .order_by("-created_at")
    )

    if search:
        queryset = queryset.filter(
            name__icontains=search,
        )

    if status:
        queryset = queryset.filter(
            status=status,
        )

    return queryset
