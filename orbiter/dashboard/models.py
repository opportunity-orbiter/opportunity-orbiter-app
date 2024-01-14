import re
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Webpage(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField("date published")

    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:100]

    def pub_date_pretty(self):
        return self.date.strftime("%b %e %Y")


# a company class to store company information, including name,  description,
# website_url, business_fields, employee_count, employee_reviews, job_portal_url,
# locations field referencing a one to many relationship with the location class,
# competitor as a self-referencing one-to-many field and last_crawled_at field


class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    website_url = models.URLField(max_length=200)
    # business_fields as an array of strings
    business_fields = models.JSONField(null=True, blank=True)
    employee_count = models.IntegerField()
    employee_reviews_rating = models.FloatField()
    job_portal_url = models.URLField(max_length=200)

    competitor = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="competitors",
    )
    last_crawled_at = models.DateTimeField(auto_now=True)

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
    active = models.BooleanField()
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
    job_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    job_url = models.URLField()
    category = models.CharField(max_length=100)

    tech_skills = models.JSONField(blank=True, null=True)
    non_tech_skills = models.JSONField(blank=True, null=True)

    salary_lower_end = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    salary_upper_end = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    vacant_since = models.DateField()
    start_date = models.DateField()
    offline_since = models.DateField(blank=True, null=True)

    benefits = models.JSONField(blank=True, null=True)

    experience_in_years_lower_end = models.PositiveIntegerField()
    experience_in_years_upper_end = models.PositiveIntegerField()

    leadership_role = models.BooleanField(default=False)
    team_size = models.PositiveIntegerField()

    full_text = models.TextField()
    employment_type = models.CharField(max_length=100)

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
