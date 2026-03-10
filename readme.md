# Grocery List API

## Overview

This project is a FastAPI-based Grocery List API. Initially, the project stored data using a JSON file. In the MongoDB integration task, the API was extended to store and manage data using MongoDB.

## Technologies Used

* FastAPI
* Python
* MongoDB
* PyMongo
* MongoDB Compass

## Features

* Create grocery lists
* Add items to lists
* Update items
* Delete items
* Delete entire lists
* Input validation using Pydantic
* CORS support
* MongoDB database integration

## Database Design

Two MongoDB collections are used:

### grocery_lists

Stores the complete grocery lists including items.

Example:
{
"listId": 1,
"listName": "Fruits",
"items": [
{"id": 1, "name": "Apple", "quantity": 5}
]
}

### lists_metadata

Stores only list identifiers and names to track existing lists.

Example:
{
"listId": 1,
"listName": "Fruits"
}

## Running the Project

1. Install dependencies
   pip install -r requirements.txt

2. Start MongoDB

3. Run FastAPI server
   uvicorn main:app --reload

4. Open Swagger UI
   http://127.0.0.1:8000/docs
