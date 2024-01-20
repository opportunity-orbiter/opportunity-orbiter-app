from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.


# a company class to store company information, including name,  description,
# website_url, business_fields, employee_count, employee_reviews, job_portal_url,
# locations field referencing a one to many relationship with the location class,
# competitor as a self-referencing one-to-many field and last_crawled_at field


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    website_url = models.URLField(max_length=200)
    # business_fields as an array of strings
    business_fields = models.JSONField(null=True, blank=True)
    employee_count = models.PositiveBigIntegerField(null=True, blank=True)
    employee_reviews_rating = models.FloatField(null=True, blank=True)
    job_portal_url = models.URLField(max_length=200)

    competitor = models.ForeignKey(
        "self",
        # TODO check if this is clever, or if we should use a different on_delete
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="competitors",
    )
    #last_crawled_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # define plural
    class Meta:
        verbose_name_plural = "companies"


# create a location class to store location information including name,
# size, business_fields, street, street_number, postal_code, city, state, country,
# active and referecing a many-to-one relationship with the company class


class Location(models.Model):
    name = models.CharField(max_length=200)
    size = models.IntegerField()
    business_fields = models.JSONField(null=True, blank=True)
    street = models.CharField(max_length=200)
    street_number = models.PositiveIntegerField()
    postal_code = models.PositiveIntegerField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    # related_name='locations': This is an optional argument that allows you to access the related Location instances from a Company instance more intuitively. For example, if you have a Company instance named company, you can access its locations with company.locations.all()
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="locations",
    )

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=200)
    job_url = models.URLField()
    category = models.CharField(max_length=100)
    short_summary = models.TextField(null=True, blank=True)

    # TODO das sollte irgendwann durch eine sich selbst pflegende Datenbank ersetzt werden
    tasks_and_responsibilities = models.JSONField(blank=True, null=True)

    # TODO das sollte irgendwann durch eine sich selbst pflegende Datenbank ersetzt werden
    tech_skill_requirements = models.JSONField(blank=True, null=True)

    # TODO das sollte irgendwann durch eine sich selbst pflegende Datenbank ersetzt werden
    non_tech_skill_requirements = models.JSONField(blank=True, null=True)

    salary_lower_bound = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    salary_upper_bound = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    # vacant since is the date on created on which the job was first posted
    vacant_since = models.DateField(auto_now_add=True)

    start_date = models.DateField(blank=True, null=True)
    offline_since = models.DateField(blank=True, null=True)

    # TODO das sollte irgendwann durch eine sich selbst pflegende Datenbank ersetzt werden
    benefits = models.JSONField(blank=True, null=True)

    minimal_experience_in_years = models.PositiveIntegerField()
    maximal_experience_in_years = models.PositiveIntegerField()

    leadership_role = models.BooleanField(default=False)
    team_size = models.PositiveIntegerField()

    full_text = models.TextField()

    # TODO das sollte irgendwann durch eine sich selbst pflegende Datenbank ersetzt werden
    type_of_contract = models.CharField(max_length=100)
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="jobs"
    )
    location = models.ForeignKey(
        "Location", on_delete=models.CASCADE, related_name="jobs"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-vacant_since"]  # Order by recent vacancies

