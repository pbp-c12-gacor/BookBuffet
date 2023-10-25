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
    "industry_identifiers": json // industry identifiers of the book (optional)
}
```

### Update a book

```http
PUT /books/${id}
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

## Retrieve all books by author

```http
GET /authors/${id}/books
```

## Retrieve all books by category

```http
GET /categories/${id}/books
```

## Retrieve all books by author and category

```http
GET /authors/${id}/categories/${id}/books
```

## Retrieve book by isbn (10 or 13)

```http
GET /books/isbn/${isbn}
```

## Search books

```http
GET /books/search/?search=${query}
```

## Search books by author

```http
GET /books/search/?search=${query},author:${author}
or
GET /books/search/?search=author:${author}
```

## Search books by title

```http
GET /books/search/?search=title:${title}
or
GET /books/search/?search=${title}
```

## Search books by category

```http
GET /books/search/?search=category:${category}
```
