from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
        unique_together = ("user", "slug")

    def __str__(self):
        return self.name


class UserScheduleMapping(models.Model):
    DAYS_OF_WEEK = [
        (0, "Sunday"),
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedule_mappings",
    )
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("user", "day_of_week")
        ordering = ["day_of_week"]

    def __str__(self):
        return f"{self.user.username}'s {self.get_day_of_week_display()} -> {self.category}"


class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    instructions = models.TextField(
        help_text="One step per line.",
    )
    prep_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Preparation time in minutes.",
    )
    cook_time = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Cooking time in minutes.",
    )
    servings = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of servings.",
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="recipes",
    )
    public = models.BooleanField(
        default=False,
        help_text="Make this recipe visible to all users.",
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Recipe rating (1-5 stars).",
    )
    image = models.ImageField(
        upload_to="recipes/",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    @property
    def total_time(self):
        prep = self.prep_time or 0
        cook = self.cook_time or 0
        return prep + cook if (self.prep_time or self.cook_time) else None

    @property
    def instruction_steps(self):
        """Return instructions split into a list of steps."""
        return [s.strip() for s in self.instructions.split("\n") if s.strip()]


class RecipeIngredient(models.Model):
    UNIT_CHOICES = [
        ("", "-- Unit --"),
        ("grams", "grams"),
        ("kilograms", "kilograms"),
        ("cups", "cups"),
        ("tsp", "tsp"),
        ("tbsp", "tbsp"),
        ("piece", "piece"),
    ]

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    name = models.CharField(max_length=200)
    quantity = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text='e.g. "2 cups", "a pinch"',
    )
    quantity_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    quantity_unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        blank=True,
        default="",
    )
    aisle = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Supermarket aisle (e.g. Produce, Dairy).",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        from decimal import Decimal

        if self.quantity_value and self.quantity_unit:
            try:
                d = Decimal(str(self.quantity_value)).normalize()
                q = f"{d:f}"
            except Exception:
                q = self.quantity_value
            return f"{q} {self.quantity_unit} {self.name}"
        if self.quantity:
            return f"{self.quantity} {self.name}"
        return self.name
