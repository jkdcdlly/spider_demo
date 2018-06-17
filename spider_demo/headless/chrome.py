from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://www.ting56.com/mp3/12837.html")
driver.implicitly_wait(10)
driver.get("http://www.ting56.com/video/12837-0-0.html")
driver.implicitly_wait(10)
driver.find_element_by_css_selector('audio[id=jp_audio_0]')
audio = driver.find_element_by_css_selector('audio[id=jp_audio_0]')
audio.get_attribute("src")
print
audio.get_attribute("src")
import urllib

urllib.urlretrieve(audio.get_attribute("src"))
