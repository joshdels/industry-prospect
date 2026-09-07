from django.test import TestCase
from django.urls import reverse

from apps.inspector.models import (
    Prospect,
    ProspectInput,
    Business,
)


class ProspectViewTests(TestCase):

    def setUp(self):
        self.business = Business.objects.create(
            name="Test Business",
        )

        self.prospect = Prospect.objects.create(
            business=self.business,
            name="John Doe",
            profile_text="Test profile",
        )

    def test_dashboard_loads(self):
        response = self.client.get(
            reverse("prospect_dashboard")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_dashboard_contains_prospect(self):
        response = self.client.get(
            reverse("prospect_dashboard")
        )

        self.assertContains(
            response,
            "John Doe",
        )

    def test_prospect_detail_loads(self):
        response = self.client.get(
            reverse(
                "prospect_detail",
                kwargs={"pk": self.prospect.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_prospect_detail_contains_name(self):
        response = self.client.get(
            reverse(
                "prospect_detail",
                kwargs={"pk": self.prospect.pk},
            )
        )

        self.assertContains(
            response,
            "John Doe",
        )

    def test_add_new_prospect_creates_input(self):
        response = self.client.post(
            reverse("add_new_prospect"),
            {
                "user_input": "Find the GIS manager at ABC Utility",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            ProspectInput.objects.count(),
            1,
        )

        self.assertEqual(
            ProspectInput.objects.first().content,
            "Find the GIS manager at ABC Utility",
        )

    def test_add_new_prospect_rejects_empty_input(self):
        response = self.client.post(
            reverse("add_new_prospect"),
            {
                "user_input": "",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            ProspectInput.objects.count(),
            0,
        )
