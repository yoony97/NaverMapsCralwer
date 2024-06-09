import json
import logging
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 로깅 기본 설정: 기본 로거를 설정하고 로그 레벨을 DEBUG로 설정합니다.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# 로거 객체 생성
logger = logging.getLogger(__name__)


class NaverMapsCralwer:
    def __init__(self, keyword, driver_path, config_path='./config.json', headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)  # Add your driver path if necessary
        self.base_url = 'https://map.naver.com/v5/search'
        self.driver.get(self.base_url)
        self.keyword = keyword
        self.shop_dict = {keyword: []}
        self.__load_config__(config_path)

    def __load_config__(self, config_path):
        with open(config_path, 'r') as file:
            self.config = json.load(file)
            
    def close(self):
        self.driver.quit()
    
    def __wait_for_element__(self, css_selector, timeout=10):
        try:
            wait = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
            return wait
        except:
            print(f"{css_selector} 태그를 찾지 못하였습니다.")
            self.close()

    def __switch_frame__(self, frame_name):
        sleep(2)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(frame_name)
        sleep(2)
    
    def __page_up__(self, num):
        logger.info('페이지 업 진행')
        body = self.driver.find_element(By.CSS_SELECTOR, 'body')
        body.click()
        for i in range(num):
            body.send_keys(Keys.PAGE_UP)
        sleep(3)

    def __page_down__(self, num):
        logger.info('페이지 다운 진행')
        body = self.driver.find_element(By.CSS_SELECTOR, self.config['body'])
        body.click()
        for _ in range(num):
            body.send_keys(Keys.PAGE_DOWN)
        sleep(3)
    
    def save_results(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.shop_dict, file, indent=4, ensure_ascii=False)

    # 축소하기
    def __zoom_out__(self):
        logger.debug(f"전국의 관련 업체들을 검색하기 위해 네이버 지도를 축소합니다.")
        zoom_out_btn = self.driver.find_element(By.CSS_SELECTOR, self.config['zoom_out'])
        while True:
            value = self.driver.find_element(By.CSS_SELECTOR, self.config['zoom_state'])
            resolution = value.get_attribute('value')
            if int(resolution) != 1:
                zoom_out_btn.click()
                sleep(1)
            else:
                new_search = self.driver.find_element(By.CSS_SELECTOR, self.config['search_in_map'])
                new_search.click()
                break
        logger.debug(f"축소를 완료했습니다.")
        sleep(5)
    
    # 키워드 검색
    def __search__(self):
        logger.debug(f"네이버 지도에서 주어진 키워드: {self.keyword}를 검색합니다.")
        self.__wait_for_element__(self.config['search_input'], 10)
        search_form = self.driver.find_element(By.CSS_SELECTOR, self.config['search_input'])
        search_form.send_keys(self.keyword)
        search_form.send_keys(Keys.ENTER)
        logger.debug(f"검색을 완료했습니다.")
        sleep(1)
    
    def __get_pages__(self):
        next_btn = self.driver.find_elements(By.CSS_SELECTOR, self.config['page_list'])         # 페이지 리스트
        return next_btn
    
    def __get_address__(self, address_buttons, idx):
        jibun_address = ''
        road_address = ''
        
        if not address_buttons:
            logger.error('검색 결과가 없습니다. config를 재설정해주세요.')
            raise
        
        #주소 버튼 누르기
        address_buttons.__getitem__(idx).click()
        sleep(1)

        # (6) 주소 눌렀을 때 도로명, 지번 나오는 div
        addr = self.driver.find_elements(By.CSS_SELECTOR, self.config['address_info'])
        if not addr:
            logger.error("주소 확장 버튼이 없습니다. config를 재설정해주세요.")

        # 지번주소만 있는 경우
        if len(addr) == 1 and addr.__getitem__(0).text[0:2] == '지번':
            jibun = addr.__getitem__(0).text
            last_index = jibun.find('복사우\n')    # 복사버튼, 우편번호 제외하기 위함
            jibun_address = jibun[2:last_index-1]
            logger.debug(f"지번 주소만 있습니다. 지번 주소:{jibun_address}")

        # 도로명만 있는 경우
        elif len(addr) == 1 and addr.__getitem__(0).text[0:2] == '도로':
            road = addr.__getitem__(0).text
            last_index = road.find('복사우\n')     # 복사버튼, 우편번호 제외하기 위함
            road_address = road[3:last_index]
            logger.debug(f"도로명 주소만 있습니다. 도로명 주소: {road_address}")

        # 도로명, 지번 둘 다 있는 경우
        else:
            road = addr.__getitem__(0).text
            road_address = road[3:(len(road) - 2)]

            jibun = addr.__getitem__(1).text
            last_index = jibun.find('복사우\n')    # 복사버튼, 우편번호 제외하기 위함
            jibun_address = jibun[2:last_index-1]

            logger.debug(f"도로명과 지번주소가 존재합니다.\n도로명주소:{road_address}\n지번 주소:{jibun_address}")

        return jibun_address, road_address


    def __get_rating__(self, idx, shop_list):
        star = 0
        visite = 0
        blog = 0

        shop_list[idx].find_element(By.CSS_SELECTOR, self.config['shop_extend']).click()
        sleep(2)
        self.__switch_frame__(self.config['shop_frame'])
        
        rating_element = self.driver.find_elements(By.CSS_SELECTOR, self.config['rating']) 
        rating = rating_element.__getitem__(0).text
        rating = rating.replace('\n', ' ')
        rating = rating.replace(',', '')

        star_idx = rating.find('별점')
        visited_idx = rating.find('방문자리뷰')
        blog_idx = rating.find('블로그리뷰')

        if star_idx != -1:
            star = float(rating[:visited_idx].split(" ")[1])
        else:
            logger.info("해당 업체는 별점이 존재하지 않습니다.")
        
        if visited_idx != -1:
            visite = int(rating[visited_idx:blog_idx].split(" ")[1]) 
        else:
            logger.info("해당 업체는 방문자 리뷰가 존재하지 않습니다.")

        if blog_idx != -1:
            blog = int(rating[blog_idx:].split(" ")[1])
        else:
            logger.info("해당 업체는 블로그 리뷰가 존재하지 않습니다.")

        self.__switch_frame__(self.config['search_frame'])
        
        return star, visite, blog

    def __get_reviews__(self, idx, shop_list):
        shop_list[idx].find_element(By.CSS_SELECTOR, self.config['shop_extend']).click()
        self.__switch_frame__(self.config['shop_frame'])


        logger.debug('리뷰탭을 검색합니다.')
        review_tap = self.driver.find_elements(By.CLASS_NAME, self.config['review_tap'])
        for i in range(len(review_tap)):
            if review_tap.__getitem__(i).text == '리뷰':
                review_tap.__getitem__(i).click()
                break
        sleep(2)

        logger.debug('리뷰 표본 개수를 확인합니다.')
        reviews_check = self.driver.find_elements(By.CSS_SELECTOR, self.config['review_check'])

        #표본이 적을 때 발생하는 "리뷰 쓰기" 버튼을 검색하여 있을 경우, 종료
        if reviews_check:
            logger.info("표본 개수가 10개 미만입니다. 리뷰 수집을 정지합니다.")
            self.__switch_frame__(self.config['search_frame'])
            return []
        else:
            logger.info("표본 개수가 10개 이상입니다.")

        logger.debug('리뷰창을 확장합니다.')
        while True:
            sleep(1)
            next_tap = self.driver.find_elements(By.CLASS_NAME, self.config['review_extend'])
            if len(next_tap) == 0:
                break
            next_tap.__getitem__(0).click()

        logger.debug('리뷰를 저장합니다.')
        reviews_elements = self.driver.find_elements(By.CLASS_NAME, self.config['review'])
        reviews = []
        for i in reviews_elements:
            review = i.text
            element = review.split("\n")
            text, count = element[0], element[2]
            reviews.append((text.replace("\"", ''), count))
        
        self.__switch_frame__(self.config['search_frame'])

        return reviews

    def crawling(self):
        self.__search__()                       # 키워드 검색 
        self.__zoom_out__()                     # 지도 축소 idx        
        self.__switch_frame__(self.config['search_frame'])
        self.__page_down__(40)                  # 페이지 다운
        self.__page_up__(40)
        start = time.time()
        logger.info(f"[크롤링 시작] {self.keyword}")

        pages = self.__get_pages__()

        for page in range(1, len(pages)):
            logger.info(f"업체 정보들과 이름, 타입 등을 검색합니다.")
            shop_list = self.driver.find_elements(By.CSS_SELECTOR, self.config['shop_list'])
            names = self.driver.find_elements(By.CSS_SELECTOR, self.config['shop_names'])  # (3) 장소명
            types = self.driver.find_elements(By.CSS_SELECTOR, self.config['shop_types'])  # (4) 장소 유형
            address_buttons = self.driver.find_elements(By.CSS_SELECTOR, self.config['address_button'])
            logger.info(f"업체 정보, 이름, 타입 검색 완료")


            logger.info(f"해당 탭을 크롤링 시작합니다.")
            for shop_idx in range(len(shop_list)):
                self.__switch_frame__(self.config['search_frame'])

                shop_name = names[shop_idx].text
                shop_type = types[shop_idx].text

                jibun_address, road_address = self.__get_address__(address_buttons=address_buttons, idx=shop_idx)    
                star, visite, blog = self.__get_rating__(shop_idx, shop_list)
                reviews = self.__get_reviews__(idx=shop_idx, shop_list=shop_list)

                dict_temp = {
                    'name': shop_name,
                    'shop_type': shop_type,
                    'road_address': road_address,
                    'jibun_address': jibun_address,
                    'reivew' : reviews,
                    'nstar' : star,
                    'nblog' : blog,
                    'nvisite' : visite
                }

                self.shop_dict[self.keyword].append(dict_temp)
                logger.debug(f"{shop_name} ...완료")

            self.__switch_frame__(self.config['search_frame'])
            if not pages or not pages[-1].is_enabled():
                print('더 이상 페이지를 넘길 수 없습니다.')
                break

            if names and names[-1]:  # names 리스트가 비어있지 않음을 확인하고 마지막 요소 검사
                pages[-1].click()
                sleep(2)
            else:
                logger.debug('마지막 업체가 인식되지 않았거나 리스트가 비어 있습니다.')
                break            
    
        logger.info('[데이터 수집 완료]\n소요 시간 :', time.time() - start)

if __name__ == '__main__':
    crawler = NaverMapsCralwer('인테리어', './chromedriver.exe', config_path='./config.json', headless=False)
    crawler.crawling()
    crawler.save_results(filename='인테리어.json')
    crawler.close()


#app-root > div > div > div > div:nth-child(6) > div:nth-child(3) > div.place_section.no_margin.ySHNE > h2 > a.place_bluelink.z9BKO

#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.no_margin.ySHNE > div > div > div > div > div.IUbn3 > a