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


file_dir = os.path.dirname(os.path.realpath(__file__))
driver_path = os.path.join(file_dir, 'geckodriver.exe')
driver = webdriver.Firefox(executable_path=driver_path)
driver.set_page_load_timeout(5)

driver.get('https://reddit.com/r/' + subreddit)

links_found = 0
links = deque()


def get_links(driver: webdriver):
    return driver.find_elements_by_css_selector('a.title')


links.extend(get_links(driver))
links_considered = 0

while links_considered < links_limit:
    if len(links) == 0:
        next_button = driver.find_element_by_css_selector('span.next-button a')
        next_button.click()
        links.extend(get_links(driver))

    link = links.pop()
    if keyword in link.text.lower():
        links_found += 1
    links_considered += 1

driver.close()

print('Found {} matches in {} links'.format(links_found, links_considered))
print('Hit rate: {:.1f}%'.format(100 * links_found / links_considered))

