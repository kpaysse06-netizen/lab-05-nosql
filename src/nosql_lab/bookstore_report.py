#!/usr/bin/env python3
"""Print a report of each author's books from the bookstore database."""

import logging
import os

import pymongo

# Read the login details from environment variables (never type them in the code)
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Status messages will look like "INFO: ..." or "ERROR: ..."
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Authors to report on: two from the loaded files and one I added in step 7
AUTHOR_IDS = ["author_002", "author_003", "author_004"]


def main():
    """Connect to Atlas and print each listed author with their books."""
    client = None
    try:
        # Open the connection using the environment variables
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        client.admin.command("ping")  # fails right away if the login is wrong
        logging.info("Connected to MongoDB Atlas")

        # Pick the database and the two collections
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count how many authors from my list exist in the database
        count = authors.count_documents({"_id": {"$in": AUTHOR_IDS}})
        print(f"Authors: {count}\n")

        # Go through the list in order, one author at a time
        for author_id in AUTHOR_IDS:
            author = authors.find_one({"_id": author_id})
            if author is None:
                logging.warning("No author found with id %s", author_id)
                continue

            print(author["name"])

            # The join: find every book whose author_ids list contains this author's _id
            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")
            print()
    except pymongo.errors.PyMongoError as err:
        logging.error("MongoDB problem: %s", err)
    finally:
        # Always close the connection when finished
        if client is not None:
            client.close()
            logging.info("Connection closed")


if __name__ == "__main__":
    main()
