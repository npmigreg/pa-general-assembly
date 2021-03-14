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