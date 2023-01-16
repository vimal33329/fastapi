<p align="center">
  <img width="480" height="100" src="https://github.com/venkateshs865/capital_guardians_account_summary_api/blob/master/screenshots/logo-removebg-preview.png?raw=true">
</p>

# Capital Guardians Account Summary API build
In this project, we build a account summary page using FastAPI
<p align="center">
  <img width="400" height="150" src="https://upload.wikimedia.org/wikiversity/en/8/8c/FastAPI_logo.png">
</p>

# INTRODUCTION TO FASTAPI
Documentation: https://fastapi.tiangolo.com
Source Code: https://github.com/tiangolo/fastapi

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
The key features are:
- Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
- Fast to code: Increase the speed to develop features by about 200% to 300%. *
- Fewer bugs: Reduce about 40% of human (developer) induced errors. *
- Intuitive: Great editor support. Completion everywhere. Less time debugging.
- Easy: Designed to be easy to use and learn. Less time reading docs.
- Short: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- Robust: Get production-ready code. With automatic interactive documentation.
- Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema

## Installation

Basic Requirement 
- Python 3.7 +
- Pycharm Editor or VS code

## FastAPI Folder Structure
| Project (Main Folder) |  |
| ------ | ------ |
| Sub Folder |  |
|  | - `API` |
|  | - `Model` |
|  | - `Service` |
| main.py |  |
| config.env |  |
| requirements.txt |  |
| readme |  |

## Steps to setup your project on Local
- Download Source code from repository or Clone the project using this command on git bash
```sh
git clone https://github.com/venkateshs865/capital_guardians_account_summary_api.git
```
## Database Setup
- To setup database, Install Microsoft MySQL Workbench
- Create a Database, name it as cg_app
- Import the following Tables
```sh
https://drive.google.com/file/d/1fwihvxy87OBmo9klDsOQBXj26RQMb9az/view?usp=sharing
https://drive.google.com/file/d/1Bi78fyHDCahAXLVDWNMfeG_bxqNGeXC8/view?usp=sharing
```
- Download these two SQL files and import it on cg_app database
- It takes about 3 - 4 hours to Import

## Step 1 - 
To step on your local follow the steps
- Clone our project on your local
- Open Pycharm and open cloned project
- Then Open file requirement.txt
- Open Terminal 
- To install the dependencies and packages, run the below command.
```sh
pip install -r .\requirement.txt
```
It Install the following dependencies and packages,
- fastapi~=0.84.0
- http-exceptions~=0.2.10
- mysql-connector-python~=8.0.31
- pydantic~=1.10.2
- python-dotenv~=0.21.0
- python-multipart~=0.0.5
- starlette~=0.19.1
- uvicorn~=0.20.0

## Step 2 -
- Open the main.py file from the directory
- Then load the command, To run server
```sh
 uvicorn main:app --reload
```
- The command uvicorn main:app refers to:
main: the file main.py (the Python "module").
app: the object created inside of main.py with the line app = FastAPI().
reload: make the server restart after code changes. Only use for development.
- It starts the application and copy that url and run it on chrome 

![](https://github.com/venkateshs865/capital_guardians_account_summary_api/blob/master/screenshots/app-load.PNG?raw=true)
## Step 3 - Call API on Swagger UI
- To execute API hit the below URL 
```sh
http://127.0.0.1:8000/docs
```
- It shows a swagger UI
![](https://github.com/venkateshs865/capital_guardians_account_summary_api/blob/master/screenshots/swagger.PNG?raw=true)
- In the /account_summary/, Select `Try it out`
![](https://github.com/venkateshs865/capital_guardians_account_summary_api/blob/master/screenshots/swagger_ui.PNG?raw=true)
- Then it shows editable textbox and `Execute` button
![](https://github.com/venkateshs865/capital_guardians_account_summary_api/blob/master/screenshots/api_request.PNG?raw=true)
- Then give the required parameters and Click `Execute`
![](https://github.com/venkateshs865/capital_guardians_account_summary_api/blob/master/screenshots/api_response.PNG?raw=true)
- It gives a response in json format.
## API
````sh
API - account_summary/
````
## Methods
There is three main methods used to return data
**get_ndis**
>This method used to find that the account was ndis or non-ndis using `rsf_id`. 
>By checking this condition, if it true it goes to `get_account_ndis` method
>If the condition was false then it goes to `get_acc_details` function

**get_acc_details**
>This method returns account details for Homecare accounts, By passing `rsf_id`. 
>It returns Account Holder Name, Unapproved transaction count and Balance amount

**get_account_ndis**
>This method returns account details for NDIS accounts, By passing `rsf_id`. 
>It returns Account Holder Name, Unapproved transaction count, Chart & Balance amount

**get_account_by_user_id**
>This method returns account details for NDIS accounts, By passing `user_id`. 
>It returns Account Holder Name, Unapproved transaction count, Chart & Balance amount

## Request
Login user will request for following fields and it returns response,
Account data fetch by two main fields, rsf_id & user_id
- rsf_id (integer)          : `262`
- user_id (integer)         : 
- search_by_lname (string)  : `sah`
- starts_with (string)      : `s`
- offset (integer)          : `0`
- limit (integer)           : `20`

## Request Body
```sh
http://127.0.0.1:8000/account_summary/?rsf_id=262&search_by_lname=sah&starts_with=s&offset=0&limit=20
```

## Response
```sh
{
  "result": [
    {
      "id": 42598,
      "lname": "Sahota",
      "fname": "Arjun",
      "rsf_id": 262,
      "unapp_count": 0,
      "deposits": 31106.17,
      "paid": 30936.96,
      "balance": 169.21,
      "allocated_amount": 70272.44,
      "spent_amount": 20433.99,
      "remaining_amount": 49838.45,
      "core_allocated_amount": 4283.3,
      "core_spent_amount": 1159.11,
      "core_remaining_amount": 3124.19,
      "capacity_allocated_amount": 65989.14,
      "capacity_spent_amount": 19274.88,
      "capacity_remaining_amount": 46714.26,
      "capital_allocated_amount": null,
      "capital_spent_amount": null,
      "capital_remaining_amount": null
    }
  ],
  "budget_date": {
    "result": [
      {
        "id": 42598,
        "start_date": "2021-07-01T00:00:00",
        "end_date": "2023-07-01T00:00:00"
      }
    ]
  },
  "total_count": {
    "result": [
      {
        "total_count": 1
      }
    ]
  },
  "community": "ndis"
}
```
<p align="center">
  <img width="400" height="150" src="https://ml.globenewswire.com/Resource/Download/c83c4886-b215-4cf0-a973-64b8f65e7003">
</p>

## Docker
**OVERVIEW**
>Build and run an image as a container
Share images using Docker Hub
Deploy Docker applications using multiple containers with a database
Run applications using Docker Compose
Before you get to the hands on part of the guide, you should learn about containers and images.

**What is a container?**
Simply put, a container is a sandboxed process on your machine that is isolated from all other processes on the host machine. That isolation leverages kernel namespaces and cgroups, features that have been in Linux for a long time. Docker has worked to make these capabilities approachable and easy to use. To summarize, a container:
is a runnable instance of an image. You can create, start, stop, move, or delete a container using the DockerAPI or CLI. It can be run on local machines, virtual machines or deployed to the cloud.
is portable (can be run on any OS).
is isolated from other containers and runs its own software, binaries, and configurations.

**What is a container image?**
When running a container, it uses an isolated filesystem. This custom filesystem is provided by a container image. Since the image contains the container’s filesystem, it must contain everything needed to run an application - all dependencies, configurations, scripts, binaries, etc. The image also contains other configuration for the container, such as environment variables, a default command to run, and other metadata.

## FastAPI Application docker build
To build a FastAPI application in Docker, you will need to have Docker installed on your machine. You can then create a Dockerfile that defines how your application's image should be built. Here is an example Dockerfile that you can use as a starting point:
```sh
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/accountsummary

COPY ./accountsummary /app/accountsummary
COPY ./main.py /app/accountsummary/main.py
COPY ./db.py /app/accountsummary/db.py
COPY ./config.env /app/accountsummary/config.env
COPY ./requirements.txt /app/accountsummary/requirements.txt

RUN pip install -r /app/accountsummary/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```
This Dockerfile uses the tiangolo/uvicorn-gunicorn-fastapi image as a base, copies your application code into the image, installs any required Python packages, and then sets the default command to run the application using uvicorn.
To build the Docker image, navigate to the directory containing your Dockerfile and run the following command:
```sh
docker build -t my-fastapi-app .
```
Replace my-fastapi-app with the desired name for your image. This will build the Docker image and give it the specified name.
Once the image is built, you can then run it as a Docker container using the following command:
```sh
docker run -p 80:80 my-fastapi-app
```
This will start a new container and bind the container's 80 port to the host machine's 80 port, so that you can access the application at http://localhost.
