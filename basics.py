import os
from collections import deque

from selenium import webdriver

print('See how often a word is mentioned in Reddit posts')
subreddit = input('Which subreddit? /r/')
keyword = input('Which keyword? ').lower()


links_limit = 0
while links_limit < 1:
    text = input('How many entries to check? [100]  ').strip()
    if text == '':
        links_limit = 100
    else:
        try:
            links_limit = int(text)
        except ValueError:
            print("Couldn't parse that, try again")


class RedditPage:
    def __init__(self, driver):
        self.driver = driver

    def get_links(self):
        divs = self.driver.find_elements_by_css_selector('div.thing')  # find divs with class 'thing'
        items = []
        for div in divs:
            found_links = div.find_elements_by_css_selector('a.title')
            items.extend(found_links)
        return items

    def navigate_to_next_page(self):
        next_button = self.driver.find_element_by_css_selector('span.next-button a')
        next_button.click()


file_dir = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(file_dir, 'chromedriver.exe')
web_driver = webdriver.Chrome(executable_path=driver_path)
web_driver.set_page_load_timeout(10)

web_driver.get('https://reddit.com/r/' + subreddit)

page = RedditPage(web_driver)

links_found = 0
links = deque()

links.extend(page.get_links())
links_considered = 0

while links_considered < links_limit:
    if links:
        link = links.pop()

        if keyword in link.text.lower():
            links_found += 1
        links_considered += 1

    else:
        # Empty deque
        page.navigate_to_next_page()
        new_links = page.get_links()
        links.extend(new_links)

web_driver.close()

print('Found {} matches in {} links'.format(links_found, links_considered))
print('Hit rate: {:.1f}%'.format(100 * links_found / links_considered))
