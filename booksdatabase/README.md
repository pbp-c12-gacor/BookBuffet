# booksdatabase

## Description

This app is a simple rest api that allows you to create, read, update and delete books from BookBuffet database.

## Usage

### Retrieve all books

```http
GET /api/books
```

### Retrieve book by id

```http
GET /api/books/${id}
```

### Create a new book

```http
POST /api/books
```

```body
{
    "authors": [
        {
            "name": "", // name of the author
        }
    ],
    "categories": [
        {
            "name": "", // name of the category
        }
    ],
    "title": "", // title of the book
    "subtitle": "", // subtitle of the book (optional)
    "publisher": "", // publisher of the book (optional)
    "published_date": date, // published date of the book (optional)
    "description": "", // description of the book (optional)
    "page_count": int, // number of pages in the book (optional)
    "language": "", // language of the book (optional)
    "preview_link": "", // preview link of the book (optional)
    "cover": image, // cover of the book (optional)
    "isbn_10": "", // isbn 10 of the book (optional)
    "isbn_13": "", // isbn 13 of the book (optional)
}
```

### Update a book

```http
PUT /api/books/${id}
```

```body
{
    "authors": [
        {
            "name": "", // name of the author
        }
    ],
    "categories": [
        {
            "name": "", // name of the category
        }
    ],
    "title": "", // title of the book
    "subtitle": "", // subtitle of the book (optional)
    "publisher": "", // publisher of the book (optional)
    "published_date": date, // published date of the book (optional)
    "description": "", // description of the book (optional)
    "page_count": int, // number of pages in the book (optional)
    "language": "", // language of the book (optional)
    "preview_link": "", // preview link of the book (optional)
    "cover": image, // cover of the book (optional)
    "isbn_10": "", // isbn 10 of the book (optional)
    "isbn_13": "", // isbn 13 of the book (optional)
}
```

### Delete a book

```http
DELETE /api/books/${id}
```

## Retrieve all authors

```http
GET /api/authors
```

## Retrieve all categories

```http
GET /api/categories
```

## Retrieve all books by author

```http
GET /api/authors/${id}/books
```

## Retrieve all books by category

```http
GET /api/categories/${id}/books
```

## Retrieve all books by author and category

```http
GET /api/authors/${id}/categories/${id}/books
```

## Retrieve book by isbn (10 or 13)

```http
GET /api/books/isbn/${isbn}
```

## Search books

```http
GET /api/books/search/?search=${query}
```

## Search books by author

```http
GET /api/search/?search=${query},author:${author}
or
GET /api/search/?search=author:${author}
```

## Search books by title

```http
GET /api/search/?search=title:${title}
or
GET /api/search/?search=${title}
```

## Search books by category

```http
GET /api/search/?search=category:${category}
```
