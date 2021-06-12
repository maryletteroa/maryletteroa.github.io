---
layout: post
title: Retrieving records using Europe PMC API
categories:
- blog
---


Understandably, going through a lot of publications is ~~a necessary evil~~ part of every researcher's life. I've been wondering how to go about filtering through search results and get as much information from papers. Fortunately, databases like the [Europe PMC](https://europepmc.org) have made available APIs to facilitate access to their records, including [annotations](https://europepmc.org/Annotations) of literature (e.g. the organisms and chemical structures mentioned in the paper, as well as links to datasets).

I only have a vague idea how to retrieve information through APIs so this was a good exercise. The first order of business is go through the [documentation](https://europepmc.org/RestfulWebService).

Checking the instructions for GET `/search`, the URL to construct the query from is:

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=parameters
```

For example, searching for the string "sloth genomics" and setting format into JSON (everything else defaults), the request URL is:

<!--more-->

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=sloth%20genomics&resultType=lite&cursorMark=*&pageSize=25&format=json
```

If you [access the link](https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=sloth%20genomics&resultType=lite&cursorMark=*&pageSize=25&format=json) in a browser (I'm using Firefox version 67.0), it can render the JSON file in a way that makes it easy to scrutinize by eye.

This results indicate that there are 131 records matching the query term (as of June 2, 2019). Further, all sorts of information about the records are made available such as the id of the article, which repository it was from (e.g. MED means the article is available in PubMED and if there is a PMCid means that the full-text is available online), as well as details about the authors, title, journal it was publised, year, etc.

A simple way to go about this in Python is to use the [`request`](https://2.python-requests.org//en/master/) library, coupled with `json` and `pprint` (pretty print). The idea is to create a message containing the address (request URL) and the details about the information you're interested in (parameter values), use the `request` library to make and send the request (HTTP request) and get the response to and from the Europe PMC database, and then use `json` and `pprint` to render it nicely in the terminal.

```python
import requests
import json
from pprint import pprint

URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
data = {"query": "sloth genomics",
        "resultType" : "lite", 
        "synonymn": "",
        "cursorMark": "*",
        "pageSize": "25",
        "sort": "",
        "format": "json",
        "callback": "",
        "email": "",
        }
response = requests.get(URL, params=data)
results = json.loads(response.text[1:-1])
pprint(results)
```

Similarly, I can construct a script to retrieve interesting annotations within an article using the [Annotations API](https://europepmc.org/AnnotationsApi).

The base URL is:

```
https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds
```

So to retrieve the annotations about organisms for the PubMED article with id 31031962 will go something like this:

```python
import requests
import json
from pprint import pprint

URL = "https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?"
data = {
    "articleIds" : "MED:31031962",
    "type" : "Organism",
    "section" : "",
    "provider" : "",
    "format" : "",
}
response = requests.get(URL, params=data)
results = json.loads(response.text[1:-1])
pprint(results)

```

The entire request URL is below and could be similarly [accessed](https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds=MED%3A31031962&type=Organisms&format=JSON) using the browser.

```
https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds=MED%3A31031962&type=Organisms&format=JSON
```

This results in information about what organism-terms are in the article (e.g. "mammals", "Homo sapiens") and which part of the article they were mentioned. It might be possible, for example, to use these data to prioritize papers according to how they could be more valuable to your research.

While visually, the results may look a lot, I can now further process (parse) the variable `results` (using the `json` library) to print only the values of the tags I was interested in. Further extensions to this script could include: 

- error-handling (e.g. connection timeouts)
- capturing the date of the query
- formatting the results into a table (e.g. tsv or csv)
- printing the results to a file
- processing annotation results for multiple IDs
- retrieving inputs for parameter values from the commandline or a file (e.g. YAML or JSON)
- further filtering of the results
- integrating two or more of the functionalities in order to have a flexible query space

Some sample scripts are in this [repository](https://github.com/maryletteroa/europmc-scripts).

My take away from this exercise is that it's possible to mine the information from articles through APIs, and make your life easier with regards to retrieving as much information from published papers. :grin:

