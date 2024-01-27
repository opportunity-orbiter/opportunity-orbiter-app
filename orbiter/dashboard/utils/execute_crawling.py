import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async


from orbiter.dashboard.models import Job, Company, Location


async def run_playwright(site):
    data = ""
    page_source = ""
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        # wait until page is loaded

        page = await browser.new_page()
        await page.goto(site, wait_until="networkidle")

        # scroll to bottom of page
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # wait until page is loaded
        # await page.wait_for_load_state("networkidle")

        # page_source = await page.content()
        # get all links from page source including their titles
        links = await page.query_selector_all("a")

        # add the base url to the links because at the moment playwright only returns the relative path
        links = [await link.get_attribute("href") for link in links]
        links = [site + link for link in links if link is not None]

        soup = BeautifulSoup(page_source, "html.parser")

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        data = "\n".join(chunk for chunk in chunks if chunk)

        await browser.close()
    return data, page_source, links


def execute_crawling_function():
    # @aethersonata mit aysncio.run können asyncrhone funktionen zu synchronen funtkioneren
    output = asyncio.run(
        run_playwright("https://www.tesla.com/de_DE/careers/search/?site=DE")
    )
    print(output)
    # aus dem https://www.tesla.com/de_DE/careers/search/?site=DE müssten alle JOb-Anzeigen links rausgezoigen

    # hier müsste nun das ganze langchain ding im Loop uber die gecrawlten Jobanzeigen rein bastenl
    # TODO hier müsste man zuerst die passende company_id und location_id finden
    # Job_Url muss aus playwright_script.py kommen
    # query company and location form database where the name includes "Tesla"
    company = Company.objects.get(name__icontains="Tesla")
    location = Location.objects.get(name__icontains="Berlin")

    json = {
        "job_url": "https://www.tesdadla.com/de_DE/careers/job/maintenance-planner-body-white-mwd-gigafactory-berlin-brandenburg-0",
        "title": "Maintenance Planner, Body in White (m/w/d) - Gigafactory Berlin Brandenburg",
        "category": "Manufacturing",
        "company": company,
        "location": location,
        "type_of_contract": "Full-time",
        "short_summary": "Maintenance planner position at Tesla's Gigafactory in Berlin-Brandenburg",
        "tasks_and_responsibilities": [
            "Managing workload and prioritizing work",
            "Reviewing line-builder and OEM documentation",
            "Implementing predictive maintenance projects",
            "Leading root cause analysis teams",
            "Auditing PM execution and accuracy",
            "Supporting weekend and shutdown planning activities",
            "Managing spares and spare parts inventory",
        ],
        "non_tech_skill_requirements": [
            "Superior verbal and written communication skills"
        ],
        "tech_skill_requirements": [
            "Data analysis and risk-based decision-making",
            "TPM and/or autonomous maintenance knowledge",
        ],
        "minimal_experience_in_years": 3,
        "maximal_experience_in_years": 5,
        "salary_lower_bound": 0,
        "salary_upper_bound": 0,
        "start_date": "2021-10-01",
        "leadership_role": False,
        "team_size": 0,
        "benefits": [
            "Competitive salary",
            "Tesla shares or bonuses",
            "30 vacation days",
            "Occupational pension",
            "Employee life and disability insurances",
            "Free EV charging",
            "Product discounts",
            "Various transportation benefits",
        ],
        "full_text": "Maintenance Planner, Body in White (m/w/d) - Gigafactory Berlin Brandenburg... (full job ad text)",
    }
    print(json)
    job = Job(**json)
    job.save()
    return json
