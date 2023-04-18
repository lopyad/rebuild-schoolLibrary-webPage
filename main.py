from exporter import save_to_file
from scrapper import extract_book_list

idx = "00"
idx = input("추출할 책의 분류를 입력하세요(00~99) : ")
print(f"{idx} 분류에 해당하는 책 내용 추출 시작")
book_list = extract_book_list(idx)
save_to_file(book_list, idx)
