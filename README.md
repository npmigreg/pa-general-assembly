# Pennsylvania General Assembly - Web Scraping Project

View this project by visiting the following link: https://pa-generalassembly-gk.herokuapp.com/

## Introduction

This site serves as a data science portfolio project to display an understanding of web development, web scraping, data visualization, natural language processing, and database management with a variety of packages. The site was built primarily in Python using the [Django web framework](https://www.djangoproject.com/).

An overview of the site's functionality includes:
* Scraping data on Senate and House Bills and Resolutions from the [PA General Assembly website](https://www.legis.state.pa.us/ "Pennsylvania General Assembly")
* Storing the scraped data in a PostgreSQL database and rendering the most recent data on list pages
* Analyzing the data and creating charts and tables that update dynamically and display bill & resolution sponsor information
* Using Natural Language Processing (NLP) to perform topic analysis on bill & resolution descriptions

The subsequent sections in this document provide details about each of the above-mentioned functionalities.

## Web Scraping

As mentioned in the introduction, data on Senate and Pennsylvania House Bills and Resolutions is collected via web scraping in this project. For each type of document scraped, the following information is collected (when available):
* Bill/Resolution number
* Date introduced
* General Assembly session
* Short title (description)
* Prime sponsor (name & URL)
* All sponsors (names)
* Last action
* Memo (title & URL)
* Bill text (URL)

Functions for scraping this data (available in [main/tasks.py](https://github.com/AI-gregking/pa-general-assembly/blob/main/main/tasks.py)) were created using the [Requests](https://requests.readthedocs.io/en/master/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) libraries. To run these tasks asynchronously, [Celery](https://docs.celeryproject.org/en/stable/) is used in combination with [CloudAMQP](https://www.cloudamqp.com/docs/index.html) (RabbitMQ service) for a task queue and message broker system.

As this project is hosted via [Heroku](https://devcenter.heroku.com/), the scraped data is saved to tables in a Heroku PostgreSQL database and rendered on the "View Bills" and "View Analysis" pages on the project site for various purposes.

## Data Visualization

Each of the document types has a series of analysis pages available by clicking "View Analysis" underneath its corresponding section on the project homepage. The initial page features interactive charts rendered using the Javascript library [Chart.js](https://www.chartjs.org/) as well as tables. The charts and tables display information about the most frequent total and prime sponsors of bills or resolutions to determine which Senators or Representatives have been the most active with recent legislation.

To make the data available for use in the charts and tables on these pages, the [Django REST Framework](https://www.django-rest-framework.org/) is used to build an API endpoint that the figures connect to via AJAX calls (view in main/templates/... .html, example [here](https://github.com/AI-gregking/pa-general-assembly/blob/main/main/templates/main/hb-dashboard.html))

## Natural Language Processing (NLP)

On the "View Analysis" pages, a second page is available in the navigation bar with the link "Text Analysis." Opening this page runs a function for a Latent Dirichlet Allocation (LDA) model to perform topic analyis on the Bill/Resolution short title (description) attributes. Since the function runs when the page loads, you can refresh the page to run the model again and obtain new topic results - view the code for these functions [here](https://github.com/AI-gregking/pa-general-assembly/blob/main/main/views.py).

The Python NLP library [NLTK](https://www.nltk.org/) is used in combination with [Gensim](https://radimrehurek.com/gensim/) to perform the text processing and topic modelling. In addition to regular stop words, exclusion lists specific to the Bills/Resolutions were created in the functions to remove frequently repeated words that do not contribute to topic understanding.

Thank you for reading!