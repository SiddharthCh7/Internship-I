-- Create authors table
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birthdate DATE
);

-- Create books table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INT,
    published_year YEAR,
    price DECIMAL(10, 2),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Inserting values into authors table
INSERT INTO authors (name, birthdate) VALUES
('George Orwell', '1903-06-25'),
('J.K. Rowling', '1965-07-31'),
('J.R.R. Tolkien', '1892-01-03');

-- Inserting values into books table
INSERT INTO books (title, author_id, published_year, price) VALUES
('1984', 1, 1949, 15.99),
('Animal Farm', 1, 1945, 9.99),
('Harry Potter and the Sorcerer''s Stone', 2, 1997, 29.99),
('Harry Potter and the Chamber of Secrets', 2, 1998, 24.99),
('The Hobbit', 3, 1937, 19.99),
('The Lord of the Rings', 3, 1954, 39.99);

-- Adding a new column to authors table
ALTER TABLE authors ADD COLUMN nationality VARCHAR(50);

-- Updating existing records with the new column
UPDATE authors SET nationality = 'British' WHERE author_id = 1 OR author_id = 2;
UPDATE authors SET nationality = 'South African' WHERE author_id = 3;

-- Adding a new column to books table
ALTER TABLE books ADD COLUMN genre VARCHAR(50);

-- Updating existing records with the new column
UPDATE books SET genre = 'Dystopian' WHERE book_id = 1 OR book_id = 2;
UPDATE books SET genre = 'Fantasy' WHERE book_id = 3 OR book_id = 4 OR book_id = 5 OR book_id = 6;

-- Select all books with their author's name
SELECT b.title, a.name AS author, b.published_year, b.price
FROM books b
JOIN authors a ON b.author_id = a.author_id;

-- Select books with a price greater than $20
SELECT title, price
FROM books
WHERE price > 20;

-- Select authors and count of books they have written
SELECT a.name, COUNT(b.book_id) AS book_count
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
GROUP BY a.name;

-- Select authors born before 1950
SELECT name, birthdate
FROM authors
WHERE birthdate < '1950-01-01';

-- Select books along with their genres
SELECT title, genre
FROM books;

