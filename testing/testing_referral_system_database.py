import json
import requests

BASE_URL = 'http://127.0.0.1:8000/referral_system_database/'

# Create a book
book_data = {
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt",
    "published_date": "1999-10-30",
    "isbn": "9780201616224"
}

response = requests.post(BASE_URL, data=json.dumps(book_data), headers={'Content-Type': 'application/json'})
print('Create:', response.status_code, response.json())

# List books
response = requests.get(BASE_URL)
print('\nList:', response.status_code, response.json())

# Get book ID
book_id = response.json()[0]['id']

# Retrieve a single book
response = requests.get(f'{BASE_URL}{book_id}/')
print('\nRetrieve:', response.status_code, response.json())

# Update the book
updated_data = {
    "title": "The Pragmatic Programmer - Updated",
    "author": "Andrew Hunt",
    "published_date": "1999-10-30",
    "isbn": "9780201616224"
}
response = requests.put(f'{BASE_URL}{book_id}/', data=json.dumps(updated_data), headers={'Content-Type': 'application/json'})
print('\nUpdate:', response.status_code, response.json())

# Delete the book
# response = requests.delete(f'{BASE_URL}{book_id}/')
# print('\nDelete:', response.status_code)
