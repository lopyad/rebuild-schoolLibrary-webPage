from exporter import save_to_file
from scrapper import extract_book_list

book_list = extract_book_list("10")
save_to_file(book_list, "10")
