"""
Google Books API Helper Module
by Pras (https://github.com/andhikapraa)
"""

__version__ = "0.1.0"

import os
from io import BytesIO
import base64
import json
import requests


class BooksAPIHelper:
    """
    This class contains helper functions for the Books API.
    This class is using Google Books API.
    """

    def __init__(self, api_key=os.environ.get("GOOGLE_BOOKS_API_KEY")):
        """
        This is the constructor for the BooksAPIHelper class.

        Args:
            api_key (str): The API key to be used for the Google Books API.
        """
        self.api_key = api_key
        if not self.api_key:
            raise BooksAPIHelperError("API key is not set. Please set the API key.")
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def search_books(self, query, max_results=10):
        """
        This function is used to search for books using the Google Books API.

        Args:
            query (str): The search query to be used.
            max_results (int): The maximum number of results to be returned.

        Returns:
            dict: The response from the Google Books API.
        """
        params = {"q": query, "maxResults": max_results, "key": self.api_key}
        while True:
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                if response.status_code != 200:
                    raise BooksAPIHelperError(f"Error {response.status_code}: {response.text}")
            except BooksAPIHelperError as e:
                print(e)
                print("Retrying...")
            return response.json()

    def search_books_by_author(self, author, max_results=10):
        """
        This function is used to search for books by author using the Google Books API.

        Args:
            author (str): The author to be used.
            max_results (int): The maximum number of results to be returned.

        Returns:
            dict: The response from the Google Books API.
        """
        query = f"inauthor:{author}"
        return self.search_books(query, max_results=max_results)

    def get_books_title(self, query, max_results=10):
        """
        This function is used to get the books title using the Google Books API.

        Args:
            query (str): The search query to be used.
            max_results (int): The maximum number of results to be returned.

        Returns:
            list: The books title from the Google Books API.
        """
        response = self.search_books(query, max_results=max_results)
        return [item["volumeInfo"]["title"] for item in response["items"]]

    def get_first_result(self, query):
        """
        This function is used to get the first result from the Google Books API.

        Args:
            query (str): The search query to be used.

        Returns:
            dict: The first result from the Google Books API.
        """
        response = self.search_books(query, max_results=1)
        return response["items"][0]

    def get_book_by_isbn(self, isbn):
        """
        This function is used to get the book information from the Google Books API.

        Args:
            isbn (str): The ISBN to be used.

        Returns:
            dict: The book information from the Google Books API.
        """
        query = f"isbn:{isbn}"
        return self.get_book_info(query)

    def get_book_id(self, query):
        """
        This function is used to get the book ID from the Google Books API.

        Args:
            query (str): The search query to be used.

        Returns:
            str: The book ID from the Google Books API.
        """
        response = self.get_first_result(query)
        return response["id"]

    def get_book_info(self, query):
        """
        This function is used to get the book information from the Google Books API.

        Args:
            query (str): The search query to be used.

        Returns:
            dict: The book information from the Google Books API.
        """
        response = self.get_first_result(query)
        return response["volumeInfo"]

    def scrape_book(self, query):
        """
        This function is used to scrape book information from the Google Books API.

        Args:
            query (str): The search query to be used.

        Returns:
            dict: The book information from the Google Books API.
        """
        attributes = [
            "title",
            "subtitle",
            "authors",
            "publisher",
            "publishedDate",
            "description",
            "pageCount",
            "categories",
            "language",
            "previewLink",
            "imageLinks",
            "industryIdentifiers",
        ]

        # Search for books
        search_result = self.search_books(query)
        print(f"Search result for {query}: ")

        # Print the search result
        for i in range (len(search_result["items"])):
            item = search_result["items"][i]
            title = item["volumeInfo"]["title"] if "title" in item["volumeInfo"] else ""
            author = ", ".join(item["volumeInfo"]["authors"]) if "authors" in item["volumeInfo"] else ""
            category = ", ".join(item["volumeInfo"]["categories"]) if "categories" in item["volumeInfo"] else ""
            subtitle = item["volumeInfo"]["subtitle"] if "subtitle" in item["volumeInfo"] else ""
            published_date = item["volumeInfo"]["publishedDate"][0:4] if "publishedDate" in item["volumeInfo"] else ""
            try:
                res = [str(x) for x in published_date]
                if res != [""]:
                    published_date = int("".join(res))
                else:
                    published_date = ""
            except ValueError:
                published_date = ""
            missing = [attribute for attribute in attributes if attribute not in item["volumeInfo"]]
            print(f"{i+1}. {title} by {author} ({category}) ({published_date})")
            print(f"    {subtitle}")
            print(f"    Missing attributes: {missing}")
        print("0. Skip this book")

        # Choose which book to scrape
        while True:
            try:
                print("Choose which book you want to scrape:")
                choice = int(input("Choice (0-10): "))
                if choice < 0 or choice > len(search_result["items"]):
                    raise ValueError
                if choice == 0:
                    return None
                break
            except ValueError:
                print("Invalid choice. Please try again.")

        # Scrape the book information
        item = search_result["items"][choice-1]
        result = dict()
        result["authors"] = [{"name": author} for author in item["volumeInfo"]["authors"]]
        if "categories" in item["volumeInfo"]:
            result["categories"] = [{"name": category} for category in item["volumeInfo"]["categories"]]
        result["title"] = item["volumeInfo"]["title"]
        result["subtitle"] = item["volumeInfo"]["subtitle"] if "subtitle" in item["volumeInfo"] else ""
        result["publisher"] = item["volumeInfo"]["publisher"] if "publisher" in item["volumeInfo"] else ""
        published_date = item["volumeInfo"]["publishedDate"][0:4] if "publishedDate" in item["volumeInfo"] else "",
        res = [str(x) for x in published_date]
        if res != [""]:
            published_date = int("".join(res))
        else:
            published_date = ""
        result["published_date"] = published_date
        result["description"] = item["volumeInfo"]["description"] if "description" in item["volumeInfo"] else ""
        result["page_count"] = item["volumeInfo"]["pageCount"] if "pageCount" in item["volumeInfo"] else None
        result["language"] = item["volumeInfo"]["language"] if "language" in item["volumeInfo"] else ""
        result["preview_link"] = item["volumeInfo"]["previewLink"] if "previewLink" in item["volumeInfo"] else ""
        result["cover"] = item["volumeInfo"]["imageLinks"]["thumbnail"] if "imageLinks" in item["volumeInfo"] else None
        # Get the cover image and save it to a BytesIO object
        #if "imageLinks" in item["volumeInfo"]:
        #    tumbnail = item["volumeInfo"]["imageLinks"]["thumbnail"]
        #    try:
        #        cover = requests.get(tumbnail, timeout=10)
        #        cover_data = BytesIO(cover.content)
        #        result["cover"] = cover_data
        #        if cover.status_code != 200:
        #            raise BooksAPIHelperError(f"Error {cover.status_code}: {cover.text}")
        #    except BooksAPIHelperError as e:
        #        print(e)
        #        result["cover"] = None
        #else:
        #    result["cover"] = None

        # Get the ISBN
        result["isbn_10"] = ""
        result["isbn_13"] = ""
        if "industryIdentifiers" in item["volumeInfo"]:
            for identifier in item["volumeInfo"]["industryIdentifiers"]:
                if identifier["type"] == "ISBN_10":
                    result["isbn_10"] = identifier["identifier"]
                elif identifier["type"] == "ISBN_13":
                    result["isbn_13"] = identifier["identifier"]
        return result

    def scrape_books(self, list_of_query):
        """
        This function is used to scrape books information from the Google Books API.

        Args:
            list_of_query (list): The list of search query to be used.

        Returns:
            list: The list of books information from the Google Books API.
            list: The list of skipped books.
        """
        results = []
        skipped = []

        # Scrape the books information
        print("Scraping books...")
        for i, query in enumerate(list_of_query):
            print(f"Progress: {i+1}/{len(list_of_query)}")
            result = self.scrape_book(query)

            # Add the result to the list of results
            if result:
                print(f"Scraped {result['title']}")
                results.append(result)
                with open("results.json", "w", encoding="utf-8") as file:
                    json.dump(results, file, indent=4)
            else: # Skip the book
                skipped.append(query)
        return results, skipped

    def scrape_and_post_books(self, list_of_query, url):
        """
        This function is used to scrape books information from the Google Books API and post it to the API.

        Args:
            list_of_query (list): The list of search query to be used.
            url (str): The URL of the API to be used.

        Returns:
            list: The list of books information from the Google Books API.
            list: The list of skipped books.
        """
        # Scrape the books information
        results, skipped = self.scrape_books(list_of_query)
        print("Posting to API...")
        input("Press enter to continue...")

        # Post the books information to the API
        for i, result in enumerate(results):
            print(f"Progress: {i+1}/{len(results)}")
            try:
                # Get the authors and categories
                authors_data = []
                for author in result["authors"]:
                    print(f"Searching for '{author['name']}'...")
                    existing_author = requests.get(url + "/authors/", timeout=10)
                    if existing_author.status_code != 200:
                        raise BooksAPIHelperError(f"Error {existing_author.status_code}: {existing_author.text}")

                    # Check if the author already exists
                    existing_author = existing_author.json()
                    if not existing_author:
                        print("No existing author found.")
                        authors_data.append(author)
                        continue
                    existing_author_list = [item["name"] for item in existing_author]
                    if author["name"] in existing_author_list:
                        print(f"Found existing author for '{author['name']}'.")
                        authors_data.append(author)
                        continue
                    print(f"No existing author found for '{author['name']}'.")
                    print("0. Create new author")
                    for j, existing_author_name in enumerate(existing_author_list):
                        print(f"{j+1}. {existing_author_name}")
                    while True:
                        try:
                            choice = int(input(f"Choice (0-{len(existing_author_list)}): "))
                            if choice < 0 or choice > len(existing_author_list):
                                raise ValueError
                            break
                        except ValueError:
                            print("Invalid choice. Please try again.")
                    if choice == 0:
                        print(f"Creating new author for '{author['name']}'...")
                        authors_data.append(author)
                    else:
                        print(f"Using existing author '{existing_author[choice-1]['name']}' for '{author['name']}'...")
                        authors_data.append({"name": existing_author[choice-1]["name"]})
                result["authors"] = authors_data
                categories_data = []
                for category in result["categories"]:
                    print(f"Searching for '{category['name']}'...")
                    existing_category = requests.get(url + "/categories/", timeout=10)
                    if existing_category.status_code != 200:
                        raise BooksAPIHelperError(f"Error {existing_category.status_code}: {existing_category.text}")
                    existing_category = existing_category.json()
                    if not existing_category:
                        print("No existing category found.")
                        categories_data.append(category)
                        continue
                    existing_category_list = [item["name"] for item in existing_category]
                    if category["name"] in existing_category_list:
                        print(f"Found existing category for '{category['name']}'.")
                        categories_data.append(category)
                        continue
                    print(f"No existing category found for '{category['name']}'.")
                    print("-1. Create new category")
                    print(f"0. Create new category for {category['name']}")
                    for j, existing_category_name in enumerate(existing_category_list):
                        print(f"{j+1}. {existing_category_name}")
                    while True:
                        try:
                            choice = int(input(f"Choice (0-{len(existing_category_list)}): "))
                            if choice < -1 or choice > len(existing_category_list):
                                raise ValueError
                            break
                        except ValueError:
                            print("Invalid choice. Please try again.")
                    if choice == -1:
                        print(f"Creating new category for '{result['title']}'...")
                        new_category = input("Enter the new category: ")
                        categories_data.append({"name": new_category})
                    if choice == 0:
                        print(f"Creating new category for '{category['name']}'...")
                        categories_data.append(category)
                    else:
                        print(f"Using existing category '{existing_category[choice-1]['name']}' for '{category['name']}'...")
                        categories_data.append({"name": existing_category[choice-1]["name"]})
                while True:
                    try:
                        choice = input("Do you want to add a new category? (y/n): ")
                        if choice not in ["y", "n"]:
                            raise ValueError
                        if choice == "y":
                            new_category = input("Enter the new category: ")
                            categories_data.append({"name": new_category})
                        if choice == "n":
                            break
                    except ValueError:
                        print("Invalid choice. Please try again.")
                result["categories"] = categories_data

                # Get the cover image
                if result["cover"]:
                    print("Getting cover image...")
                    cover = requests.get(result["cover"], timeout=10)
                    if cover.status_code != 200:
                        raise BooksAPIHelperError(f"Error {cover.status_code}: {cover.text}")
                    cover_data = BytesIO(cover.content)
                    result["cover"] = cover_data
                else:
                    result["cover"] = None

                # Post the book information to the API
                files = {"cover": (f"{result['title']}.jpg", result.pop("cover"))} if result["cover"] else None
                headers = {"Content-Type": "application/json"}
                print(f"Posting {result['title']}...")
                response = requests.post(url + "/books/", headers=headers, data=json.dumps(result), timeout=10)
                if response.status_code != 201:
                    raise BooksAPIHelperError(f"Error {response.status_code}: {response.text}")
                if response.status_code == 201:
                    print(f"Posted {result['title']}")
                    book_id = response.json()["id"]
                    book_url = f"{url}/books/{book_id}/"
                    print(f"Posting cover for {result['title']}...")
                    response = requests.patch(book_url, files=files, timeout=10)
                    if response.status_code != 200:
                        raise BooksAPIHelperError(f"Error {response.status_code}: {response.text}")
                    print(f"Posted cover for {result['title']}")
                print(f"Succesfully posted {result['title']} to {url}/books/{book_id}/")
            except BooksAPIHelperError as e:
                print(e)
                skipped.append(result["title"])
        return results, skipped

    def post_book(self, book, url):
        """
        This function is used to post a book information to the API.

        Args:
            book (dict): The book information to be posted.
            url (str): The URL of the API to be used.

        Returns:
            dict: The book information from the Google Books API.
        """
        # Get the authors and categories
        authors_data = []
        for author in book["authors"]:
            print(f"Searching for '{author['name']}'...")
            existing_author = requests.get(url + "/authors/", timeout=10)
            if existing_author.status_code != 200:
                raise BooksAPIHelperError(f"Error {existing_author.status_code}: {existing_author.text}")

            # Check if the author already exists
            existing_author = existing_author.json()
            if not existing_author:
                print("No existing author found.")
                authors_data.append(author)
                continue
            existing_author_list = [item["name"] for item in existing_author]
            if author["name"] in existing_author_list:
                print(f"Found existing author for '{author['name']}'.")
                authors_data.append(author)
                continue
            print(f"No existing author found for '{author['name']}'.")
            print("0. Create new author")
            for j, existing_author_name in enumerate(existing_author_list):
                print(f"{j+1}. {existing_author_name}")
            while True:
                try:
                    choice = int(input(f"Choice (0-{len(existing_author_list)}): "))
                    if choice < 0 or choice > len(existing_author_list):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please try again.")
            if choice == 0:
                print(f"Creating new author for '{author['name']}'...")
                authors_data.append(author)
            else:
                print(f"Using existing author '{existing_author[choice-1]['name']}' for '{author['name']}'...")
                authors_data.append({"name": existing_author[choice-1]["name"]})
        book["authors"] = authors_data
        categories_data = []
        for category in book["categories"]:
            print(f"Searching for '{category['name']}'...")
            existing_category = requests.get(url + "/categories/", timeout=10)
            if existing_category.status_code != 200:
                raise BooksAPIHelperError(f"Error {existing_category.status_code}: {existing_category.text}")
            existing_category = existing_category.json()
            if not existing_category:
                print("No existing category found.")
                categories_data.append(category)
                continue
            existing_category_list = [item["name"] for item in existing_category]
            if category["name"] in existing_category_list:
                print(f"Found existing category for '{category['name']}'.")
                categories_data.append(category)
                continue
            print(f"No existing category found for '{category['name']}'.")
            print("-1. Create new category")
            print(f"0. Create new category for {category['name']}")
            for j, existing_category_name in enumerate(existing_category_list):
                print(f"{j+1}. {existing_category_name}")
            while True:
                try:
                    choice = int(input(f"Choice (-1-{len(existing_category_list)}): "))
                    if choice < -1 or choice > len(existing_category_list):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please try again.")
            if choice == -1:
                print(f"Creating new category for '{book['title']}'...")
                new_category = input("Enter the new category: ")
                categories_data.append({"name": new_category})
            if choice == 0:
                print(f"Creating new category for '{category['name']}'...")
                categories_data.append(category)
            else:
                print(f"Using existing category '{existing_category[choice-1]['name']}' for '{category['name']}'...")
                categories_data.append({"name": existing_category[choice-1]["name"]})
        while True:
            try:
                choice = input("Do you want to add a new category? (y/n): ")
                if choice not in ["y", "n"]:
                    raise ValueError
                if choice == "y":
                    new_category = input("Enter the new category: ")
                    categories_data.append({"name": new_category})
                if choice == "n":
                    break
            except ValueError:
                print("Invalid choice. Please try again.")
        book["categories"] = categories_data
        
        # Get the cover image
        if book["cover"]:
            print("Getting cover image...")
            cover = requests.get(book["cover"], timeout=10)
            if cover.status_code != 200:
                raise BooksAPIHelperError(f"Error {cover.status_code}: {cover.text}")
            cover_data = BytesIO(cover.content)
            book["cover"] = cover_data
        else:
            book["cover"] = None

        # Post the book information to the API
        files = {"cover": (f"{book['title']}.jpg", book.pop("cover"))} if book["cover"] else None
        headers = {"Content-Type": "application/json"}
        print(f"Posting {book['title']}...")
        response = requests.post(url + "/books/", headers=headers, data=json.dumps(book), timeout=10)
        if response.status_code != 201:
            raise BooksAPIHelperError(f"Error {response.status_code}: {response.text}")
        if response.status_code == 201:
            print(f"Posted {book['title']}")
            book_id = response.json()["id"]
            book_url = f"{url}/books/{book_id}/"
            print(f"Posting cover for {book['title']}...")
            response = requests.patch(book_url, files=files, timeout=10)
            if response.status_code != 200:
                raise BooksAPIHelperError(f"Error {response.status_code}: {response.text}")
            print(f"Posted cover for {book['title']}")
        print(f"Succesfully posted {book['title']} to {url}/books/{book_id}/")
        return book

    def post_books(self, books, url):
        """
        This function is used to post books information to the API.

        Args:
            books (list): The list of books information to be posted.
            url (str): The URL of the API to be used.

        Returns:
            list: The list of books information from the Google Books API.
        """
        results = []
        skipped = []
        for i, book in enumerate(books):
            print(f"Progress: {i+1}/{len(books)}")
            try:
                self.post_book(book, url)
                results.append(book)
            except BooksAPIHelperError as e:
                print(e)
                skipped.append(book)
        return books


class BooksAPIHelperError(Exception):
    """
    This class is used to represent an error from the Books API Helper.
    """
