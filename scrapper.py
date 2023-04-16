from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
import time
import re

def extract_max_page_number(text):
  # 전체 건수 추출
  #total_count = re.search(r'전체 (\d+)건', text).group(1)
  
  # 최대 페이지 수 추출
  max_page = re.search(r'(\d+)/(\d+) 페이지', text).group(2)
  
  #print("전체 건수:", total_count)
  print("최대 페이지 수:", max_page)
  return int(max_page)

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

  book_data = []
  
  #해당 분류의 페이지 수를 추출
  max_page = extract_max_page_number(driver.find_element(By.CLASS_NAME, "bd_list_guide").text)

  #페이지 수만 큼 스크래핑 
  for page in range(1, max_page+1):
    #현재 페이지, 해당 분류 전부 스크래핑 시작
    # 책에 대한 정보가 담겨있는 <ul>태그 전부 가져오기
    print(f"{page}페이지 추출 시작")
    # if page>=2:
    #   print("refreshed")
    #   driver.refresh
    #   driver.implicitly_wait(3)

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
  
      #추출해서 book에 넣기
      book["title"] = ul_tag.find_element(By.CLASS_NAME, "bd_list_title").text
      book["author"] = ul_tag.find_element(By.CLASS_NAME, "bd_list_writer").find_element(By.CLASS_NAME, "dd").text
      book["publisher"] = ul_tag.find_element(By.CLASS_NAME, "bd_list_company").find_element(By.CLASS_NAME, "dd").text
      book["call_number"] = ul_tag.find_element(By.CLASS_NAME, "bd_list_year").find_element(By.CLASS_NAME, "dd").text
      book["location"] = ul_tag.find_element(By.CLASS_NAME, "bd_list_location").find_element(By.CLASS_NAME, "dd").text
      book["rental"] = ul_tag.find_element(By.CLASS_NAME, "rental_box").text
      book["image"] = ul_tag.find_element(By.TAG_NAME, "img").get_attribute("src")
      
      book_data.append(book)

    #다음 페이지로 이동하기
    print(f"{page}페이지 추출 완료")
    js_code = f"goPagesOnly({page+1})"
    driver.execute_script(js_code)
    driver.implicitly_wait(5)
    
  # 결과 출력
  #print(book_data.count)
  
  # 웹드라이버 종료
  time.sleep(3)
  driver.quit()

  #return값 전달
  return book_data

