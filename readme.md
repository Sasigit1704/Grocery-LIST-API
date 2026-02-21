# Grocery List API

## Description
This is a FastAPI-based Grocery List Editor.
It supports adding, updating, deleting items and managing the whole list.
Data is stored in a JSON file.

## Features
- Add item
- Update item (PUT)
- Partial update (PATCH)
- Delete single item
- Delete entire list
- Get total quantity
- JSON file storage
- Proper error handling

## Tech Stack
- FastAPI
- Pydantic
- Uvicorn
- JSON storage

## How to Run

pip install -r requirements.txt

uvicorn main:app --reload

Open:
http://127.0.0.1:8000/docs