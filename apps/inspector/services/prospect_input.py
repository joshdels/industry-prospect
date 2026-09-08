from apps.inspector.models import (
    ProspectInput,
    Prospect,
    Business,
    Industry,
    Tag,
)


def get_pending_inputs():
    return ProspectInput.objects.filter(status=ProspectInput.Status.PENDING)


def create_prospect_from_analysis(prospect_input, result):

    prospect_input.status = ProspectInput.Status.PROCESSING
    prospect_input.save(update_fields=["status"])

    try:

        business, _ = Business.objects.get_or_create(name=result["business_name"])

        industry_name = result.get("industry_name", "").strip()

        if industry_name:

            industry, _ = Industry.objects.get_or_create(name=industry_name)

            business.industry = industry
            business.save(update_fields=["industry"])

        for tag_name in result.get("tags", []):

            tag_name = tag_name.strip()

            if not tag_name:
                continue

            tag, _ = Tag.objects.get_or_create(name=tag_name)

            business.tags.add(tag)

        prospect = Prospect.objects.create(
            business=business,
            name=result["name"],
            role=result.get("role", ""),
            profile_url=prospect_input.profile_url,
            profile_text=result.get("profile_text", ""),
            discovery_target=result.get("discovery_target", ""),
            opening_question=result.get("opening_question", ""),
            big_3_questions=result.get("big_3_questions", []),
            outreach_message=result.get("outreach_message", ""),
            research_notes=result.get("research_notes", ""),
        )

        prospect_input.status = ProspectInput.Status.COMPLETED
        prospect_input.save(update_fields=["status"])

        return prospect

    except Exception:

        prospect_input.status = ProspectInput.Status.FAILED
        prospect_input.save(update_fields=["status"])

        raise
