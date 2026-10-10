
 // Step 2: Select the bookstore database
db = db.getSiblingDB("bookstore");

// Step 3: Load authors.json
db.authors.drop();
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(doc);

// Step 4: Load books.json
db.books.drop();
doc = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(doc);

// Step 5: List all authors and books
db.authors.find();
db.books.find();

// Step 6: Insert two new books
db.books.insertMany([
  {
    title: "The Hobbit",
    published_year: 1937,
    author_ids: ["author_004"]
  },
  {
    title: "The Hunger Games",
    published_year: 2008,
    author_ids: ["author_005"]
  }
]);

// Step 7: Add missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "J.R.R. Tolkien",
    nationality: "British",
    bio: {
      short: "Fantasy author",
      long: "Known for The Hobbit and The Lord of the Rings."
    }
  },
  {
    _id: "author_005",
    name: "Suzanne Collins",
    nationality: "American",
    bio: {
      short: "Novelist and screenwriter",
      long: "Known for The Hunger Games series."
    }
  }
]);

// Step 8: Filter books by a list of authors
db.books.find({
  author_ids: {
    $in: ["author_001", "author_004"]
  }
});

