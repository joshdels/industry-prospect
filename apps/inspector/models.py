from django.db import models


class ProspectInput(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)

    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business",
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="business",
    )

    def __str__(self):
        return self.name


class Prospect(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        REPLIED = "replied", "Replied"
        LEARNED = "learned", "Learned"

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="prospects",
    )

    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)

    # LinkedIn information
    profile_text = models.TextField()

    # AI-generated discovery preparation
    discovery_target = models.TextField(blank=True)
    opening_question = models.TextField(blank=True)
    outreach_message = models.TextField(blank=True)

    # Most important: what you actually learned
    findings = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
