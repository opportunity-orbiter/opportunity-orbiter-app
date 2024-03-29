import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.prompts import BasePromptTemplate, ChatPromptTemplate, PromptTemplate
import datetime

from orbiter.dashboard.models import Job, Company, Location
import asyncio

from typing import List
import json
from numpy import short
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.callbacks.tracers import ConsoleCallbackHandler

from orbiter.settings import OPENAI_KEY


async def crawl_links_from_portal(job_portal_url):
    print("runplaywright")
    data = ""
    page_source = ""
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        # wait until page is loaded

        page = await browser.new_page()
        await page.goto(job_portal_url, wait_until="networkidle")

        # scroll to bottom of page
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # wait until page is loaded
        # await page.wait_for_load_state("networkidle")

        # page_source = await page.content()
        # get all links from page source including their titles
        links = await page.query_selector_all("a")

        # add the base url to the links because at the moment playwright only returns the relative path
        links = [await link.get_attribute("href") for link in links]
        links = [job_portal_url + link for link in links if link is not None]

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
    print(links)
    return data, page_source, links


# def crawl_links_from_portal(job_portal_url):
#     # @aethersonata mit aysncio.run können asyncrhone funktionen zu synchronen funtkioneren
#     output = asyncio.run(run_playwright(job_portal_url))
#     print("output:")
#     print(output)


async def check_if_job_link(links):
    llm = ChatOpenAI(
        temperature=0.7, model="gpt-3.5-turbo-1106", openai_api_key=OPENAI_KEY
    )

    structured_schema = {
        "properties": {
            "title": {"type": "string", "description": "The title of the job"},
            "url": {"type": "string", "description": "The url of the job"},
            "link_is_an_individual_job_ad": {
                "type": "boolean",
                "description": "True if the link is teasering an individual job role, false otherwise",
            },
        },
        "required": ["url", "title", "link_is_an_individual_job_ad"],
    }

    # parser nutzen um die links zu extrahieren

    extraction_chain = create_extraction_chain(
        structured_schema,
        llm,
        verbose=True,
    )

    # check the extraction chain on the first 5 objects in output[2]

    # job_urls = extraction_chain.invoke(links[2][0:5])
    job_urls = extraction_chain.invoke(links[2][70:80])
    print(job_urls)

    # only return job_urls where link_is_an_individual_job_ad is true
    # print every link that is not an individual job ad value
    print("Das sind die Links, die ein Job sind")

    job_urls_is_an_individual_job_ad = [
        job for job in job_urls["text"] if job["link_is_an_individual_job_ad"] == True
    ]
    print(job_urls_is_an_individual_job_ad)

    # print the opposite
    print("Das sind die Links, die kein Job sind")
    job_urls_is_not_an_individual_job_ad = [
        job for job in job_urls["text"] if job["link_is_an_individual_job_ad"] == False
    ]
    print(job_urls_is_not_an_individual_job_ad)

    return job_urls_is_an_individual_job_ad


async def crawl_job(url):
    async with async_playwright() as p:
        print("crawl job")
        browser = await p.firefox.launch(headless=True)

        page = await browser.new_page()
        await page.goto(url)

        page_source = await page.content()
        soup = BeautifulSoup(page_source, "html.parser")

        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        job_text = "\n".join(chunk for chunk in chunks if chunk)

        await browser.close()

    return job_text, url


async def process_job_text(job_text, url):
    model = ChatOpenAI(
        temperature=0.7,
        model="gpt-3.5-turbo-1106",
        openai_api_key=OPENAI_KEY,
    )

    # Define your desired data structure.
    class JobProfile(BaseModel):
        title: str = Field(
            description="The title of the job",
        )
        company: str = Field(
            description="The company of the job",
        )

        category: str = Field(
            description="The category of the job",
        )
        location: str = Field(
            description="The location of the job",
        )
        type_of_contract: str = Field(
            description="The type of contract of the job",
        )
        short_summary: str = Field(
            description="A short summary of the job in one sentence",
        )
        tasks_and_responsibilities: List[str] = Field(
            description="The tasks and responsibilities of the job",
        )
        non_tech_skill_requirements: List[str] = Field(
            description="The non-technology skill requirements of the job as a bulletpoint list",
        )
        tech_skill_requirements: List[str] = Field(
            description="The technology skill requirements of the job as a bulletpoint list",
        )

        minimal_experience_in_years: int = Field(
            description="The minimal experience in years for the job or the most important skill of the job"
        )
        maximal_experience_in_years: int = Field(
            description="The ideal maximal experience in years for the job or the most important skill of the job."
        )
        salary_lower_bound: int = Field(
            description="The lower bound of the salary for the job",
        )
        salary_upper_bound: int = Field(
            description="The upper bound of the salary for the job",
        )

        start_date: str = Field(
            description="The starting date of the job, only use a format to like YYYY-MM-DD to fill it in",
        )

        leadership_role: bool = Field(
            description="True if the job is a leadership role, false otherwise",
        )

        team_size: int = Field(
            description="The size of the team",
        )

        benefits: List[str] = Field(
            description="What we offer as bulletpoints",
        )

        full_text: str = Field(
            description="The complete text of the job ad",
        )

    # And a query intented to prompt a language model to populate the data structure.
    quality_evaluation_query = f"""Du analysierst die Stellenanzeige und bewertest die Qualität der Stelle. Deine Ergebnisse fasst Du kurz zusammen. Beachte dazu die Hinweise in den descriptons der properties.
    Passage:"""

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=JobProfile)

    prompt = PromptTemplate(
        template="Du bist ein genauer Job-Such-Experte und hast die Stellenanzeige genau gelesen. \n{format_instructions}\n{query}{input}\n",
        input_variables=["query", "input"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    job_json = chain.invoke(
        {"query": quality_evaluation_query, "input": job_text},
        # config={"callbacks": [ConsoleCallbackHandler()]},
    )

    print("das ist die url aus process_job_text function " + url)
    print(job_json)
    return job_json, url


def save_job_from_json(job_json, url):
    # Map JSON values to Job attributes

    # new_job = Job(
    #     title = job_json["title"],
    #     job_url = url,
    #     category = job_json["category"],
    #     short_summary = job_json["short_summary"],
    #     tasks_and_responsibilities = job_json["tasks_and_responsibilities"],
    #     tech_skill_requirements = job_json["tech_skill_requirements"],
    #     non_tech_skill_requirements = job_json["non_tech_skill_requirements"],
    #     salary_lower_bound = job_json["salary_lower_bound"],
    #     salary_upper_bound = job_json["salary_upper_bound"],
    #     # vacant_since = timezone.now().date(),
    #     # start_date = datetime.now().date(),
    #     # offline_since = datetime.now().date(),
    #     benefits = job_json["benefits"],
    #     minimal_experience_in_years = job_json["minimal_experience_in_years"],
    #     maximal_experience_in_years = job_json["maximal_experience_in_years"],
    #     leadership_role = job_json["leadership_role"],
    #     team_size = job_json["team_size"],
    #     full_text = job_json["full_text"],
    #     type_of_contract = job_json["type_of_contract"],
    #     # location_id=1,  # Replace with the actual ID of the location
    #     company = Company.objects.get(name__icontains="Tesla"),
    #     location = Location.objects.get(name__icontains="Berlin")

    # )

    company = Company.objects.get(name__icontains="Tesla")
    location = Location.objects.get(name__icontains="Berlin")
    # json = {
    #     "job_url": "https://www.tesdadla.com/de_DE/careers/job/maintenance-planner-body-white-mwd-gigafactory-berlin-brandenburg-0",
    #     "title": "Maintenance Planner, Body in White (m/w/d) - Gigafactory Berlin Brandenburg",
    #     "category": "Manufacturing",
    #     "company": company,
    #     "location": location,
    #     "type_of_contract": "Full-time",
    #     "short_summary": "Maintenance planner position at Tesla's Gigafactory in Berlin-Brandenburg",
    #     "tasks_and_responsibilities": [
    #         "Managing workload and prioritizing work",
    #         "Reviewing line-builder and OEM documentation",
    #         "Implementing predictive maintenance projects",
    #         "Leading root cause analysis teams",
    #         "Auditing PM execution and accuracy",
    #         "Supporting weekend and shutdown planning activities",
    #         "Managing spares and spare parts inventory",
    #     ],
    #     "non_tech_skill_requirements": [
    #         "Superior verbal and written communication skills"
    #     ],
    #     "tech_skill_requirements": [
    #         "Data analysis and risk-based decision-making",
    #         "TPM and/or autonomous maintenance knowledge",
    #     ],
    #     "minimal_experience_in_years": 3,
    #     "maximal_experience_in_years": 5,
    #     "salary_lower_bound": 0,
    #     "salary_upper_bound": 0,
    #     "start_date": "2021-10-01",
    #     "leadership_role": False,
    #     "team_size": 0,
    #     "benefits": [
    #         "Competitive salary",
    #         "Tesla shares or bonuses",
    #         "30 vacation days",
    #         "Occupational pension",
    #         "Employee life and disability insurances",
    #         "Free EV charging",
    #         "Product discounts",
    #         "Various transportation benefits",
    #     ],
    #     "full_text": "Maintenance Planner, Body in White (m/w/d) - Gigafactory Berlin Brandenburg... (full job ad text)",
    # }

    print("DAs hier ist das durch das LLM Modell erstellt Job JSON")
    print(job_json)

    print("Das hier ist das durch das LLM Modell übergebene URL")
    print(url)
    job_json = job_json[0]
    # url = job_json[1]

    job_json["company"] = company
    job_json["location"] = location
    job_json["start_date"] = "2021-10-01"
    # reset start date if it not uses the format YYYY-MM-DD
    try:
        datetime.datetime.strptime(job_json["start_date"], "%Y-%m-%d")
    except ValueError:
        job_json["start_date"] = datetime.datetime.now().date()
    # fill start_date with today's date
    # job_json["start_date"] = datetime.datetime.now().date()
    job_json["job_url"] = url
    job_json["vacant_since"] = "2021-10-01"

    job = Job(**job_json)

    job.save()


def start_crawl_and_save(job_portal_url):
    links = asyncio.run(crawl_links_from_portal(job_portal_url))
    job_links = asyncio.run(check_if_job_link(links))

    for job in job_links[:2]:  # 2 iterations for testing. <---
        url = job.get("url", "")
        job_text = asyncio.run(crawl_job(url))
        job_json = asyncio.run(process_job_text(job_text, url))
        # task = asyncio.create_task(save_job_from_json(job_json))
        # tasks.append(task)
        print("Das ist die URL aus der Start_Crawl_and_save Funktion")
        print(url)
        save_job_from_json(job_json, url)

    print("All jobs saved in the database")
