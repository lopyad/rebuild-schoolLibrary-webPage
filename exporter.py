import csv

def save_to_file(books=None, idx="00"):
  file = open(f"book/books{idx}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["title","author","publisher","call_number","img","rental"])

  for book in books:
    writer.writerow(list(book.values()))