from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class Driver:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("enable-automation")
        chrome_options.add_argument("--disable-browser-side-navigation");
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)

    def what_you_want(self, idx, date):
        """ select which category you want to get
                1. 학사 공지
                2. 일반 공지
                3. 사업단 소식
                4. 충남대 공지사항
        """
        if idx == 1:
            return self.get_the_content("https://computer.cnu.ac.kr/computer/notice/bachelor.do", date)
        elif idx == 2:
            return self.get_the_content("https://computer.cnu.ac.kr/computer/notice/notice.do", date)
        elif idx == 3:
            return self.get_the_content("https://computer.cnu.ac.kr/computer/notice/project.do", date)
        elif idx == 0:
            return self.get_from_cnu(
                "https://plus.cnu.ac.kr/_prog/_board/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702", date)
        elif idx == 4:
            return self.get_the_content("https://computer.cnu.ac.kr/computer/notice/job.do", date)

    def get_the_content(self, url, date):
        """ 컴퓨터 공학과 홈페이지 내용들 가져오기. """
        self.content = []
        self.driver.get(url)

        update = self.driver.find_elements(By.CSS_SELECTOR, 'div.total-wrap > span')
        self.content.append("오늘 업데이트 된 게시글 : " + update[1].text)

        files = self.driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')
        for item in files:
            temp = []

            if date != item.text.split()[-2]:
                continue

            temp.append(item.find_element(By.CSS_SELECTOR, 'td.b-num-box').text)

            title = item.find_element(By.CSS_SELECTOR, 'div.b-title-box > a')
            temp.append(title.text)

            info = item.find_elements(By.CSS_SELECTOR, 'div.b-m-con > span')
            for word in info:
                if word.text == "첨부파일" or word.text == "공지":
                    continue
                temp.append(word.text)

            temp.append(title.get_attribute("href"))

            self.content.append(temp)

        return self.content

    def get_from_cnu(self, url, date):
        """ 백마 광장 새소식 가져오기 """
        self.content = []
        self.driver.get(url)

        update = list(self.driver.find_element(By.CSS_SELECTOR, '#boardFind div > p').text.split())[-1]
        self.content.append("오늘 업데이트 된 게시글 : " + update[:-1])

        files = self.driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')
        for item in files:
            temp = []

            if date != item.text.split()[-2].replace("-", ".")[2:]:
                continue

            temp.append(item.find_element(By.CSS_SELECTOR, 'td.num').text)

            title = item.find_element(By.CSS_SELECTOR, 'td.title > a')
            temp.append(title.text)

            temp.append(item.find_element(By.CSS_SELECTOR, 'td.center').text)
            temp.append(item.find_element(By.CSS_SELECTOR, 'td.date').text)
            temp.append(item.find_element(By.CSS_SELECTOR, 'td.hits').text)

            temp.append(title.get_attribute("href"))

            self.content.append(temp)

        return self.content
