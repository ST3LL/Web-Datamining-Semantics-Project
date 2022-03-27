# web_datamining_and_semantics

ESILV - Web Datamining & Semantics - project 2022

## Motivation
School Project from the Web Datamining & Semantics course, taught as part of the ESILV master's degree.

## Main Objective

- Make a (Optional: Web) application that integrates different point of interest (POI) which are geospatial data from mutiple sources, including dynamic data.
- Define a knowledge model (that is, an ontology) that describes the types of entities that are stored in the knowledge base.
- Optional: Display information on Web pages together with structured data, for best search engine optimisation.

# Solution

We created a web application allowing the user to search for all the forgotten objects of the French National Railway Company (SNCF).

## Dataset/API used
Link :

- https://ressources.data.sncf.com/explore/dataset/objets-trouves-restitution/export/?sort=date

- https://ressources.data.sncf.com/explore/dataset/referentiel-gares-voyageurs/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B


# Setup

```
pip install requirements.txt
```

## Installation

The installation is simple. Run ```app.py``` and go to ```localhost:5000``` with a web browser.

Data is stored on the ```data``` repository of the project.
