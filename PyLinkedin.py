from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import re

# vars
skip_list = ['Chapter Quiz']
course_list = []
home_url = 'https://www.linkedin.com/learning/'
spl_chrs = list(r"<>?/|\*:\"")
progress_link = "https://www.linkedin.com/learning/me/in-progress"
saved_link = "https://www.linkedin.com/learning/me/saved"
completed_link = "https://www.linkedin.com/learning/me/completed"



def download_video(url, savename):
    print("Downloading {}".format(savename))
    urllib.request.urlretrieve(url, savename)


def access_course(url):
    driver.get(url)
    import time
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "classroom-toc-section__toggle-title")))
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".classroom-toc-section.classroom-toc-section--collapsed")))
    sections = driver.find_elements_by_css_selector(".classroom-toc-section.classroom-toc-section--collapsed")
    # classroom-toc-section classroom-toc-section--collapsed
    for section in sections:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".classroom-toc-section.classroom-toc-section--collapsed")))
        try:
            section.click()
        except:
            breakpoint()
    elem = driver.find_element('xpath', "//*")
    source_code = elem.get_attribute("outerHTML")
    soup = BeautifulSoup(source_code, "lxml")
    total_sections = soup.find_all('section',class_='classroom-toc-section')
    course_name_obj = soup.find('div', class_="classroom-nav__details")
    course_name = course_name_obj.text.strip().split('\n')[0].strip()
    for section in total_sections:
        section_name = section.find_all('span',class_='classroom-toc-section__toggle-title')[0].text.strip()
        titles = section.find_all('div', class_='classroom-toc-item__title')
        title_links = section.find_all('a', href=True)
        sl_no = 1
        for title_obj,link_obj in zip(titles,title_links):
            video_name = title_obj.text.strip().split('\n')[0]
            if video_name in skip_list:
                continue
            partial_url = link_obj['href']
            complete_url = "https://www.linkedin.com{}".format(partial_url)
            driver.get(complete_url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "vjs-tech")))
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "vjs_video_3_html5_api")))
            elem = driver.find_element('xpath', "//*")
            source_code = elem.get_attribute("outerHTML")
            soup = BeautifulSoup(source_code, "lxml")
            try:
                for k in range(5):
                    if soup.find('video', src=True) != None:
                        download_link = soup.find('video', src=True)['src']
                        break
                    else:
                        import time
                        time.sleep(3)
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "vjs-tech")))
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "vjs_video_3_html5_api")))
                        elem = driver.find_element('xpath', "//*")
                        source_code = elem.get_attribute("outerHTML")
                        soup = BeautifulSoup(source_code, "lxml")
            except:
                import time
                time.sleep(5)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "vjs-tech")))
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "vjs_video_3_html5_api")))
                elem = driver.find_element('xpath', "//*")
                source_code = elem.get_attribute("outerHTML")
                soup = BeautifulSoup(source_code, "lxml")
                download_link = soup.find('video', src=True)['src']
            course_name = re.sub(r'[*<>?/|\\:"]', '_', course_name)
            section_name = re.sub(r'[*<>?/|\\:"]', '_', section_name)
            video_name = re.sub(r'[*<>?/|\\:"]', '_', video_name)
            video_name = "{}- {}".format(sl_no, video_name)
            sl_no += 1
            location = "{}\\{}\\".format(course_name.strip(), section_name.strip())
            file_name = location+video_name+".mp4"
            Path(location).mkdir(parents=True, exist_ok=True)
            print("Downloading - {}".format(video_name))
            download_video(download_link, file_name)


if __name__ == "__main__":
    # selenium driver
    driver = wb.Firefox()
    driver.get('https://www.linkedin.com/learning/')
    input("Please login and then press enter")
    link = input("Please enter the Course link to download.")
    access_course(link)
    print("Downloaded!!!")


