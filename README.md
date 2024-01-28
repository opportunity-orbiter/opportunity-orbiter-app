# Opportunity Orbiter

## Link

<https://plankton-app-ire4u.ondigitalocean.app/>

## Beschreibung

Unser Projekt umfasst die Entwicklung einer Django-App mit einem integrierten Webcrawler, der speziell auf die Bewertung von Jobanzeigen aus dem IT-Sektor im Berliner Raum abzielt, darunter Start-ups, Unternehmen und Beratungen. Wir möchten die Themen Web Crawling, Datenhaltung, Analytics und Webinterface bearbeiten. Eine besondere Herausforderung wird es sein, Unternehmensseiten zu crawlen. Zusätzlich planen wir, ein Large Language Model (LLM) einzubeziehen, speziell ein frei verfügbares Modell wie LeoLM/leo-hessianai-13b-chat · Hugging Face, um die erhobenen Daten zu analysieren.
In unserem Projekt konzentrieren wir uns darauf, makroökonomische Trends und Entwicklungen in der IT-Branche, wie im Bereich Data Engineering, anhand der analysierten Jobanzeigen zu erfassen und zu verstehen. Wir gehen davon aus, dass wir möglicherweise schnelle Veränderungen in den Jobanzeigen feststellen können, die auf wirtschaftliche Schwankungen oder politische Entscheidungen, wie Investitionen der Bundesregierung in die Infrastruktur, zurückzuführen sind.

## Perspektive

Ferner überlegen wir, ob unser Projekt nicht nur zur Analyse genutzt werden könnte, sondern auch als Grundlage für die Bereitstellung von Open Data, womit wir die gesammelten Daten der Öffentlichkeit zugänglich machen würden.

## Teammitglieder

Alexander (Werner) Krüger
Quirin Johannes Koch

## Technologien

Das Projekt basiert auf einer Paketzusammenstellung von Petr Stribny <petr@stribny.name> im Rahmen seines [Sidewinder-Starter-Projekts](https://stribny.github.io/sidewinder/). Folgende Technologien werden in unserem Projekt primär eingesetzt:

### Backend

- Python 3.12
- Django 5.0
- Django REST Framework 3.14.0 (noch nicht implementiert)
- huey 2.4.5 (noch nicht implementiert)

### Crawling

- playwright 1.40.0
- beautifulsoup4 4.12.2
- langchain 0.1.0
- langchain-openai 0.0.2.post1

### Frontend

- DaisyUI 2.6.0
- TailwindCSS 3.0.23
- HTMX 1.6.1
