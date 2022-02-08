import requests
from bs4 import BeautifulSoup

def what_you_want(idx, date):
    """ select which category you want to get
            1. 학사 공지
            2. 일반 공지
            3. 사업단 소식
            4. 충남대 공지사항
    """
    if idx == 1:
        return get_the_content("https://computer.cnu.ac.kr/computer/notice/bachelor.do", date)
    elif idx == 2:
        return get_the_content("https://computer.cnu.ac.kr/computer/notice/notice.do", date)
    elif idx == 3:
        return get_the_content("https://computer.cnu.ac.kr/computer/notice/project.do", date)
    else:
        return get_from_cnu("https://plus.cnu.ac.kr/_prog/_board/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702", date)

def get_the_content(url, date):
    """ 컴퓨터 공학과 홈페이지 내용들 가져오기. """
    ret = []

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    update = soup.select('div.total-wrap > span')
    ret.append("오늘 업데이트 된 게시글 : " + update[1].text)

    files = soup.select('tbody > tr')
    for item in files:
        temp = []

        if date != item.text.split()[-2]:
             continue
        print(item.text.split()[-2])
        temp.append(item.select_one('td.b-num-box').text.strip().replace("\n", "").replace("\t", ""))

        title = item.select_one('div.b-title-box > a')
        temp.append(title.text.strip().replace("\n", "").replace("\t", ""))

        info = item.select_one('div.b-m-con > span')
        for word in info:
            word = word.strip().replace("\n", "").replace("\t", "")
            if word == "첨부파일" or word == "공지":
                continue
            temp.append(word)

        temp.append(url + title["href"])

        ret.append(temp)

    return ret

def get_from_cnu(url, date):
    """ 백마 광장 새소식 가져오기 """
    ret = []

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    update = soup.select_one('#boardFind > div > p').text.split(":")[1]
    ret.append("오늘 업데이트 된 게시글 : " + update)

    files = soup.select('tbody > tr')
    for item in files:
        temp = []

        if date != item.text.split()[-2].replace("-", ".")[2:]:
            continue

        temp.append(item.select_one('td.num').text.strip().replace("\n", "").replace("\t", ""))

        title = item.select_one('td.title > a')
        temp.append(title.text.strip().replace("\n", "").replace("\t", ""))

        temp.append(item.select_one('td.center').text.strip().replace("\n", "").replace("\t", ""))
        temp.append(item.select_one('td.date').text.strip().replace("\n", "").replace("\t", ""))
        temp.append(item.select_one('td.hits').text.strip().replace("\n", "").replace("\t", ""))

        temp.append(url + title["href"])

        ret.append(temp)

    return ret