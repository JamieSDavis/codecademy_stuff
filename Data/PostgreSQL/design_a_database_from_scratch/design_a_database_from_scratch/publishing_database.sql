-- Creating all of the tables

CREATE TABLE agency (
  name text PRIMARY KEY,
  address text
);

CREATE TABLE agent (
  name text PRIMARY KEY,
  agency_name text REFERENCES agency(name)
);

CREATE TABLE author (
  name text PRIMARY KEY,
  bio text,
  agent_name text REFERENCES agent(name)
);

CREATE TABLE publisher (
  name text PRIMARY KEY
);

CREATE TABLE book(
  isbn bigint PRIMARY KEY,
  title text,
  publisher_name text REFERENCES publisher(name),
  price money
);

CREATE TABLE authors_books(
  author_name text REFERENCES author(name),
  book_isbn bigint REFERENCES book(isbn),
  PRIMARY KEY (author_name, book_isbn)
);

CREATE TABLE imprint (
  name text PRIMARY KEY,
  genre text,
  age_range text,
  publisher_name text REFERENCES publisher(name)
);

CREATE TABLE editor (
  name text PRIMARY KEY,
  imprint_name text REFERENCES imprint(name)
);

-- Creating an agency, two agents, and a publisher

INSERT INTO agency VALUES ('Writers Home', '123 Fake St.');
INSERT INTO agent VALUES ('Frodo Baggins', 'Writers Home');
INSERT INTO agent  VALUES ('Bilbo Baggins', 'Writers Home');
INSERT INTO publisher VALUES ('Simon and Schuster');


-- Realizing that the data type of age_range should actually be two columns of ints
ALTER TABLE imprint DROP COLUMN age_range;
ALTER TABLE imprint ADD COLUMN age_min int;
ALTER TABLE imprint ADD COLUMN age_max int;


-- Adding two imprints and an editor that works at one of the imprints
INSERT INTO imprint VALUES ('Pocket Books', 'paperback', 'Simon and Schuster', 7, 80);
INSERT INTO imprint VALUES ('Stormy Castle', 'fantasy', 'Simon and Schuster', 16, 30);
INSERT INTO editor VALUES ('Jennifer Editor', 'Stormy Castle');

-- Realizing that a book is only connected to a publisher, but we can't find the editor based on that information alone
ALTER TABLE book ADD COLUMN	editor_name text REFERENCES editor(name);

-- Adding two books
INSERT INTO book VALUES (1234, 'The Great Adventure', 'Simon and Schuster', 12.99, 'Jennifer Editor');
INSERT INTO book VALUES (5249, 'The Return of the Queen', 'Simon and Schuster', 15.99, 'Jennifer Editor');

-- Adding an author
INSERT INTO author VALUES ('J.T.T Rolkin', 'This author is a prolific fantasy author', 'Frodo Baggins');

-- Making it so our author has written two books
INSERT INTO authors_books VALUES ('J.T.T Rolkin', 5249);
INSERT INTO authors_books VALUES ('J.T.T Rolkin', 1234);


-- Realizing that a book doesn't need to know the publisher, as long as we know the editor.
ALTER TABLE book DROP COLUMN publisher_name;

