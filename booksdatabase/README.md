# booksdatabase

## Description

This app is a simple rest api that allows you to create, read, update and delete books from BookBuffet database.

## Usage

### Retrieve all books

```http
GET /books
```

### Retrieve book by id

```http
GET /books/${id}
```

### Create a new book

```http
POST /books
```

```body
{
    "authors": [], // list of authors
    "categories": [], // list of categories
    "title": "", // title of the book
    "subtitle": "", // subtitle of the book (optional)
    "publisher": "", // publisher of the book (optional)
    "published_date": date, // published date of the book (optional)
    "description": "", // description of the book (optional)
    "page_count": int, // number of pages in the book (optional)
    "language": "", // language of the book (optional)
    "preview_link": "", // preview link of the book (optional)
    "cover": image, // cover of the book (optional)
    "industry_identifiers": json // industry identifiers of the book (optional)
}
```

### Update a book

```http
PUT /books/${id}
```

```body
{
    "authors": [], // list of authors
    "categories": [], // list of categories
    "title": "", // title of the book
    "subtitle": "", // subtitle of the book (optional)
    "publisher": "", // publisher of the book (optional)
    "published_date": date, // published date of the book (optional)
    "description": "", // description of the book (optional)
    "page_count": int, // number of pages in the book (optional)
    "language": "", // language of the book (optional)
    "preview_link": "", // preview link of the book (optional)
    "cover": image, // cover of the book (optional)
    "industry_identifiers": json // industry identifiers of the book (optional)
}
```

### Delete a book

```http
DELETE /books/${id}
```

## Retrieve all authors

```http
GET /authors
```

## Retrieve all categories

```http
GET /categories
```
