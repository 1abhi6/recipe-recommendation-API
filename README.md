# 🍳 Recipe Recommendation API

Day 2 | AutoGen Project

## Overview

A simple API that recommends recipes based on input ingredients.

## Tech Stack

- AutoGen
- FastAPI
- Docker
- AWS (optional)

## Quick Start

```
git clone https://github.com/1abhi6/recipe-recommendation-API.git
cd recipe-recommendation-api
pip install -r requirements.txt
uvicorn app:app --reload
```

## API Usage

- **POST** `/recommendations`
  Send `{ "ingredients": ["tomato", "onion"] }` to get recipes.
