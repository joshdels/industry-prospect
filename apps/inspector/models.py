from django.db import models


class ProspectInput(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    content = models.TextField()

    profile_url = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]


class Industry(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

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
        related_name="businesses",
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="businesses",
    )

    def __str__(self):
        return self.name


class Prospect(models.Model):

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        REPLIED = "replied", "Replied"
        LEARNED = "learned", "Learned"
        GHOSTED = "ghosted", "Ghosted"
        WEAK_INFORMANT = "weak informat", "Weak Informant"

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="prospects",
    )

    name = models.CharField(max_length=255)

    role = models.CharField(
        max_length=255,
        blank=True,
    )

    profile_url = models.URLField(blank=True)

    # LinkedIn / profile information
    profile_text = models.TextField(blank=True)

    # --------------------------------------------------
    # AI-GENERATED DISCOVERY PREPARATION
    # --------------------------------------------------

    discovery_target = models.TextField(
        blank=True,
        help_text="What we want to learn from this prospect.",
    )

    opening_question = models.TextField(
        blank=True,
        help_text="The initial question used to start discovery.",
    )

    big_3_questions = models.JSONField(
        default=list,
        blank=True,
        help_text=(
            "Three Mom Test-style questions for digging into "
            "the prospect's real workflow and problems."
        ),
    )

    outreach_message = models.TextField(
        blank=True,
        help_text="AI-generated outreach message.",
    )

    research_notes = models.TextField(
        blank=True,
        help_text=("AI research and hypotheses. " "Not confirmed customer findings."),
    )

    # --------------------------------------------------
    # HUMAN / ACTUAL DISCOVERY
    # --------------------------------------------------

    findings = models.TextField(
        blank=True,
        help_text=("What was actually learned from talking " "to the prospect."),
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional manual notes.",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name
