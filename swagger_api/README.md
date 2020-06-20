 <img src="https://img.shields.io/badge/application-REST%20API-yellow.svg?style=flat-square" alt="application API">  <img src="https://img.shields.io/badge/Python-3.6-green.svg?style=flat-square" alt="made with Python"> <img src="https://img.shields.io/badge/package-FastAPI-blue.svg?style=flat" alt="made with fastapi">

# :rocket: Instructions 

- Simple [Swagger](https://swagger.io/) based `API` generation for general machine learning tasks. The best part is the **API documentation**, that's generated in this process and is quite helpful for users while using the APIs.
- The Swagger UI is generated using the `fast`, `light-weight` python package [FastAPI](https://fastapi.tiangolo.com/).

The final version looks like this:

<center>
<img src="assets/swagger_apip_look.png" width="600" alt="image">
</center>

## :star: Start the `api` server

- `cd swagger_api`
- `uvicorn ml_api:app --reload --port 8032 --host 0.0.0.0`

This will start 3 APIs, `/preprocess`, `/train`, `/predict`

Then check the swagger based API documentation at: 
- link 1: [http://0.0.0.0:8032/docs](http://0.0.0.0:8032/docs)
- link 2: [http://0.0.0.0:8032/redoc](http://0.0.0.0:8032/redoc)

# :bookmark_tabs: FastAPI Important Documentation

- [Request body](https://fastapi.tiangolo.com/tutorial/body/)
- [Add project description](https://fastapi.tiangolo.com/tutorial/metadata/)
- [Add API Description](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)
- [Add API example value](https://fastapi.tiangolo.com/tutorial/schema-extra-example/)

----