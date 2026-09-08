from apps.inspector.models import (
    ProspectInput,
    Industry,
    Tag,
)

from apps.inspector.services import (
    create_prospect_from_analysis,
)

from apps.mcp.prompts import (
    PROSPECT_INSTRUCTIONS,
    DISCOVERY_INSTRUCTIONS,
    CLASSIFICATION_INSTRUCTIONS,
)


def register_prospect_tools(mcp):

    @mcp.tool()
    def get_pending_prospects() -> list[dict]:
        """
        Get all prospect inputs that are still waiting
        for AI analysis.

        Process prospects one at a time.
        """

        prospect_inputs = ProspectInput.objects.filter(
            status=ProspectInput.Status.PENDING
        ).order_by("created_at")

        return [
            {
                "id": prospect_input.id,
                "content": prospect_input.content,
                "profile_url": prospect_input.profile_url,
                "status": prospect_input.status,
            }
            for prospect_input in prospect_inputs
        ]

    # ============================================================
    # GET PROSPECT INPUT
    # ============================================================

    @mcp.tool()
    def get_prospect_input(input_id: int) -> dict:
        """
        Get a specific prospect input for analysis.

        Returns the prospect information and the instructions
        Claude should follow when researching and preparing
        the prospect.
        """

        prospect_input = ProspectInput.objects.get(id=input_id)

        return {
            "instructions": {
                "prospect": PROSPECT_INSTRUCTIONS,
                "discovery": DISCOVERY_INSTRUCTIONS,
            },
            "prospect": {
                "id": prospect_input.id,
                "content": prospect_input.content,
                "profile_url": prospect_input.profile_url,
                "status": prospect_input.status,
            },
        }

    @mcp.tool()
    def get_industries_and_tags() -> dict:
        """
        Get existing industries and tags.

        Reuse existing values whenever possible.
        Avoid creating duplicate or synonymous values.
        """

        industries = Industry.objects.order_by("name")
        tags = Tag.objects.order_by("name")

        return {
            "instructions": CLASSIFICATION_INSTRUCTIONS,
            "industries": [
                {
                    "id": industry.id,
                    "name": industry.name,
                    "description": industry.description,
                }
                for industry in industries
            ],
            "tags": [
                {
                    "id": tag.id,
                    "name": tag.name,
                }
                for tag in tags
            ],
        }

    @mcp.tool()
    def create_prospect(
        input_id: int,
        name: str,
        role: str,
        business_name: str,
        industry_name: str,
        tags: list[str],
        profile_text: str,
        discovery_target: str,
        opening_question: str,
        big_3_questions: list[str],
        outreach_message: str,
        research_notes: str,
    ) -> dict:
        """
        Create a prospect after the AI has completed
        research and discovery preparation.

        This tool stores the analysis.

        It does not create customer findings.
        """

        prospect_input = ProspectInput.objects.get(id=input_id)

        result = {
            "name": name,
            "role": role,
            "business_name": business_name,
            "industry_name": industry_name,
            "tags": tags,
            "profile_text": profile_text,
            "discovery_target": discovery_target,
            "opening_question": opening_question,
            "big_3_questions": big_3_questions,
            "outreach_message": outreach_message,
            "research_notes": research_notes,
        }

        prospect = create_prospect_from_analysis(
            prospect_input,
            result,
        )

        return {
            "id": prospect.id,
            "name": prospect.name,
            "role": prospect.role,
            "business": prospect.business.name,
            "status": prospect.status,
            "message": "Prospect created successfully.",
        }
