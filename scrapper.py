from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
import time

def extract_book_list(idx="00"):
  #setting
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  #운호고등학교 도서관 url
  url = "https://reading.cbe.go.kr/r/newReading/search/schoolSearchOnlyForm.jsp?schoolCode=10258&kind=1"

  #url로 접근
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  driver.implicitly_wait(5)

  #idx에 해당하는 분류로 JS코드를 실행해서 이동
  js_code = f"goSearchKdcOnly('{idx}', '', '');"
  driver.execute_script(js_code)
  driver.implicitly_wait(5)
  
  #해당 페이지, 해당 분류 전부 스크랩핑 시작
  book_data = []
  
  # 책에 대한 정보가 담겨있는 <ul>태그 전부 가져오기
  book_list  = driver.find_element(By.CLASS_NAME, "school_lib")
  driver.implicitly_wait(3)
  ul_tags = book_list.find_elements(By.TAG_NAME, "ul")
  
  #각각의 <ul>태그 자식인 <li>태그에서 정보 추출하기
  for ul_tag in ul_tags:
    #책 제목, 저자, 출판정보, 청구기호, 소장처, 책 이미지 링크, 대출 가능 여부
    #title, author, publisher, call_number, location, image, rental
    book = {
      "title" : "None",
      "author" : "None",
      "publisher" : "None",
      "call_number" : "None",
      "location" : "None",
      "image" : "None",
      "rental" : "None"
    }
    book["title"] = ul_tag.find_element(By.CLASS_NAME, "bd_list_title").text
    book["image"] = ul_tag.find_element(By.TAG_NAME, "img").get_attribute("src")
    
    # # "book_image" 클래스에서 이미지 링크 가져오기
    # book_img = ul_tag.find_element(By.TAG_NAME, "img").get_attribute("src")
  
    # # "bd_list_title" 클래스에서 클래스가 "bold"인 span의 텍스트 가져오기
    # book_title = ul_tag.find_element(By.CLASS_NAME, "bd_list_title").text

    # book_writer = ul_tag.find_element(By.CLASS_NAME, "bd_list_writer").find_element(By.CLASS_NAME, "dd").text
    # print(book_writer)
    
    # # 가져온 내용을 dictionary에 저장
    # book = {"title": book_title, "image": book_img}
    book_data.append(book)
  
  # 결과 출력
  print(book_data)
  
  # 웹드라이버 종료
  time.sleep(3)
  driver.quit()

  #return값 전달
  return book_data

