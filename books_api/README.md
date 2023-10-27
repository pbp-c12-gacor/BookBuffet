# BOOKS API

## Description

This is a simple helper class to make it easier to work with the Google Books API.

## Initialization

```
from books_api import BooksAPIHelper

# If you have an API key at your environment variables
books_api = BooksAPIHelper()

# If you want to pass the API key as a parameter
books_api = BooksAPIHelper(api_key=YOUR_API_KEY)
```

## Usage

### Search for books

```
books_api.search_books(query='harry potter')
```

### Scrape books from a list of queries

```
books_api.scrape_books(list_of_query=['harry potter', 'lord of the rings'])
```