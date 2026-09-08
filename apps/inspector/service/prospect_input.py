from apps.inspector.models import ProspectInput


def get_pending_inputs():
    pending_prospect = ProspectInput.objects.filter(status=ProspectInput.Status.PENDING)

    print(pending_prospect)

    return pending_prospect


def process_pending_inputs():
    raw_prospects = get_pending_inputs()

    for prospect_input in raw_prospects:
        prospect_input.status = ProspectInput.Status.PROCESSING
        prospect_input.save(update_fields=["status"])
