import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.prompts import BasePromptTemplate, ChatPromptTemplate

from orbiter.dashboard.models import Job, Company, Location
import asyncio


async def run_playwright(job_portal_url):
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
    return data, page_source, links


def execute_crawling_function(job_portal_url):
    # @aethersonata mit aysncio.run können asyncrhone funktionen zu synchronen funtkioneren
    output = asyncio.run(run_playwright(job_portal_url))
    print("output:")
    print(output)

    # llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-1106", openai_api_key=OPENAI_KEY)

    # structured_schema = {
    #     "properties": {
    #         "title": {"type": "string", "description": "The title of the job"},
    #         "url": {"type": "string", "description": "The url of the job"},
    #         "link_is_an_individual_job_ad": {
    #             "type": "boolean",
    #             "description": "True if the link is teasering an individual job role, false otherwise",
    #         },
    #     },
    #     "required": ["url", "title", "link_is_an_individual_job_ad"],
    # }

    # # parser nutzen um die links zu extrahieren

    # extraction_chain = create_extraction_chain(
    #     structured_schema,
    #     llm,
    #     verbose=True,
    # )

    # # check the extraction chain on the first 20 objects in output[2]
    # print("text:")
    # text = extraction_chain.invoke(output[2][0:5], verbose=True)
    # print(text)

    llm = ChatOpenAI(
        temperature=0, model="gpt-3.5-turbo-1106", openai_api_key=OPENAI_KEY
    )
    structured_schema = {
        "properties": {
            "video_name": {"type": "string"},
            "views": {"type": "integer"},
        },
        "required": ["video_name", "views"],
    }

    # write a structured schema that extracts all links as enmus from the page giving the text of the link and the url

    structured_schema = {
        "properties": {
            "jobs": {
                "type": "array",
                "description": "All jobs and their links on the page",
                "items": {
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the job",
                        },
                        "url": {"type": "string", "description": "The url of the job"},
                    },
                },
            },
            "required": ["url", "title"],
        }
    }

    structured_schema = {
        "properties": {
            "title": {"type": "string", "description": "The title of the job"},
            "url": {"type": "string", "description": "The url of the job"},
        },
        "required": ["url", "title"],
    }

    # parser nutzen um die links zu extrahieren

    extraction_chain = create_extraction_chain(
        structured_schema,
        llm,
        verbose=True,
    )

    print("Extraction chain created")
    text = extraction_chain.invoke(output[2], verbose=True)
    print(text)


async def run_playwright(site):
    data = ""
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)

        page = await browser.new_page()
        await page.goto(site)

        page_source = await page.content()
        soup = BeautifulSoup(page_source, "html.parser")

        # for script in soup(
        #     ["script", "style"]
        # ):  # remove all javascript and stylesheet code
        #     script.extract()
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        data = "\n".join(chunk for chunk in chunks if chunk)

        await browser.close()
    return data


output = run_playwright(
    "https://www.tesla.com/de_DE/careers/search/job/maintenance-planner-body-in-white-m-w-d-gigafactory-berlin-brandenburg-214973"
)
print("hsdhdshdshdshdsh")
print(output)
