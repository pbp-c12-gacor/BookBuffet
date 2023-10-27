"""
This file is used to scrape books information from the Google Books API.
"""

import json
from books_api import BooksAPIHelper

if __name__ == "__main__":
    print("Scraping books information from the Google Books API...")
    print("This may take a while...")
    books_api = BooksAPIHelper()
    with open("query.txt", "r", encoding="utf-8") as file:
        list_of_query = file.read().splitlines()

    print("1. Scrape and post books information to the API")
    print("2. Scrape books information only")
    print("3. Post books information only")
    choice = input("Enter your choice: ")
    if choice == "1":
        results, skipped = books_api.scrape_and_post_books(
            list_of_query, "http://127.0.0.1:8000/api"
            )
    elif choice == "2":
        results, skipped = books_api.scrape_books(list_of_query)
    elif choice == "3":
        with open("results.json", "r", encoding="utf-8") as file:
            results = json.load(file)
        results, skipped = books_api.post_books(results, "http://127.0.0.1:8000/api")
    else:
        raise ValueError("Invalid choice.")

    if choice == "1" or choice == "2":
        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)
        print(f"Scraped {len(results)} books.")
        with open("skipped.txt", "w", encoding="utf-8") as file:
            for skipped_book in skipped:
                file.write(skipped_book + "\n")
        print(f"Skipped {len(skipped)} books.")
    if choice == "1" or choice == "3":
        print(f"Posted {len(results)} books.")
    if choice == "3":
        with open("skipped.json", "w", encoding="utf-8") as file:
            json.dump(skipped, file, indent=4)
        print(f"Skipped {len(skipped)} books.")
    print("Done.")
