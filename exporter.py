import json

def save_to_file(book_list=None, idx="00"):
  # JSON 파일로 저장할 경로와 파일명을 지정
  file_path = f"book/books{idx}.json"
  
  with open(file_path, "w", encoding="utf-8") as f:
      # JSON 파일에 쓸 데이터를 직렬화합니다.
      # ensure_ascii=False 옵션은 유니코드 문자열을 인코딩하지 않습니다.
      json.dump(book_list, f, ensure_ascii=False, indent="\t")


# import csv

# def save_to_file(books=None, idx="00"):
#   file = open(f"book/books{idx}.csv", mode="w")
#   writer = csv.writer(file)
#   writer.writerow(["title","author","publisher","call_number","img","rental"])

#   for book in books:
#     writer.writerow(list(book.values()))