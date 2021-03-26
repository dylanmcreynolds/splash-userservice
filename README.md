# Purpose


This project is intended to serve as an API for Scientific User Facilities to 
have a common way to access user and group information. 

It is intended that the code in [models](./userworld/models.py) and [api](./userworld/api.py) would be the front-end interface, and facility-specific APIs would could then write specific code that maps to those model classes.

A fastapi server is included just because it docuemnts APIs so well. You can start it up and browse to the OpenAPI page that it generates:

    pip install -e .
    uvicorn userworld.api:app

Once started, you can navigate to the page at `http://localhost:8000/docs`

This project in a very early stage. Te (NSLS-II Scipy Cookiecutter)[https://github.com/NSLS-II/scientific-python-cookiecutter] was used to start the project, but much is not yet being taken advantage of (especially documentation).
