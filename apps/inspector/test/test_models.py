from django.test import TestCase

from apps.inspector.models import (
    ProspectInput,
    Industry,
    Tag,
    Business,
    Prospect,
)


class ProspectInputModelTests(TestCase):

    def test_default_status_is_pending(self):
        prospect_input = ProspectInput.objects.create(
            content="Find the GIS manager at ABC Utility",
        )

        self.assertEqual(
            prospect_input.status,
            ProspectInput.Status.PENDING,
        )

    def test_string_representation(self):
        prospect_input = ProspectInput.objects.create(
            content="This is a test prospect input",
        )

        self.assertEqual(
            str(prospect_input),
            "This is a test prospect input",
        )


class IndustryModelTests(TestCase):

    def test_string_representation(self):
        industry = Industry.objects.create(
            name="Utilities",
        )

        self.assertEqual(
            str(industry),
            "Utilities",
        )


class TagModelTests(TestCase):

    def test_string_representation(self):
        tag = Tag.objects.create(
            name="GIS",
        )

        self.assertEqual(
            str(tag),
            "GIS",
        )


class BusinessModelTests(TestCase):

    def setUp(self):
        self.industry = Industry.objects.create(
            name="Utilities",
        )

        self.tag = Tag.objects.create(
            name="GIS",
        )

        self.business = Business.objects.create(
            name="Test Utility",
            website="https://example.com",
            industry=self.industry,
        )

        self.business.tags.add(self.tag)

    def test_string_representation(self):
        self.assertEqual(
            str(self.business),
            "Test Utility",
        )

    def test_industry(self):
        self.assertEqual(
            self.business.industry,
            self.industry,
        )

    def test_tags(self):
        self.assertIn(
            self.tag,
            self.business.tags.all(),
        )


class ProspectModelTests(TestCase):

    def setUp(self):
        self.business = Business.objects.create(
            name="Test Utility",
        )

        self.prospect = Prospect.objects.create(
            business=self.business,
            name="John Doe",
            role="GIS Manager",
            profile_text="Works with utility GIS.",
        )

    def test_default_status_is_new(self):
        self.assertEqual(
            self.prospect.status,
            Prospect.Status.NEW,
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.prospect),
            "John Doe",
        )

    def test_business_relationship(self):
        self.assertEqual(
            self.prospect.business,
            self.business,
        )
