# Task Two:  Crud Operation

This is a simple REST API capable of CRUD operations on a "person" resource, interfacing with any relational Database.

## Description

This is a basic REST API designed for CRUD operations on a "person" resource. It's notable for its versatility as it can interface with any relational database, providing a consistent means to Create, Read, Update, and Delete person records. The API adheres to RESTful principles, utilizing HTTP methods to interact with the resource efficiently. This simplicity and adaptability make it a practical choice for developers seeking a standardized solution for managing person-related data across different database systems.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

>Clone this repository to your local machine.


>Navigate to the project directory: cd TaskTwo.

> Run "python -m venv env" to create a virtual Environment.

> Run "env/Scripts/activate" to activate virtual Enviroment.

>Run "pip install -r requirements.txt" to install project dependencies.

>Run "flask run" in terminal to start the development server.

>Open http://localhost:5000 in a web browser to view the project.

## Features

* The GET request requires an attribute name and its corresponding value, and it retrieves a person from the database if it exists.
* The POST request accepts an attribute name along with its corresponding value and utilizes this information to create a new person entry within the database.
* The PUT request receives two attributes: 'attribute_name' and 'new_name,' and utilizes them to update a person's name to the 'new_name' value.
* The DELETE request requires an attribute name and its corresponding value, and if a matching person exists in the database, it proceeds to delete that person.
 