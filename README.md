# Pennsylvania General Assembly - Web Scraping Project
This site serves as a data science portfolio project to display an understanding of web development, web scraping, data visualization, natural language processing, and database management with a variety of packages. The site was built primarily in Python using the [Django web framework](https://www.djangoproject.com/ "Django").

An overview of the site's functionality includes:
* Scraping data on Senate and House Bills and Resolutions from the [PA General Assembly website](https://www.legis.state.pa.us/ "Pennsylvania General Assembly")
* Storing the scraped data in a PostgreSQL database and rendering the most recent data on list pages
* Analyzing the data and creating charts and tables that update dynamically and display bill & resolution sponsor information
* Using Natural Language Processing (NLP) to perform topic analysis on bill & resolution descriptions

The subsequent sections in this document provide details about each of the above-mentioned functionalities.