# Allo parser

Web scrapper of prompt autocomplete

- Database in src/database.db
- - 2339 unique promts with 10517 products autocomplete
- - 6666 unique promts with NO products autocomplete
- Main script src/main.py

### Task:
Using Python 3 collect hints from the search string of the allo.ua online store (http://allo.ua/).

### Requirements:
  - Use Python 3.6
  - As starting words, use all possible combinations of 1, 2 and 3 letters;
  - It is necessary to use multithreading (or asynchrony);
  - Save the results to a local sqlite database;
  - When restarting, the script should be able to continue execution from the place where it finished the last time;
  - Cannot use the Scrapy library.


## SOLUTION
Install requests:
```sh
$ pip3 install requests
```
- To get autocomplete for promt was copyed inner website AJAX request
- Used all possible permutations with 1-3 letters of english and russian alphabet separetly
- Used threading to spead up requests but limited to the amount that the server can handle, because otherwise it shoots 429 ERROR
- Used SQLite3 database with 2 tables(Products(promt, product), No_products(promt))
- Before start it subtract permutations that already exist in a database




