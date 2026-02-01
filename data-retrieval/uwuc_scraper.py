import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_from_ucal(ucal_url: str):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(ucal_url)
    links = []
    print("driver setup, finding subject listings!")

    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.style__groups___IUc1d")))
    subject_collapsibles = table.find_elements(By.CSS_SELECTOR, "div.style__collapsibleBox___DBqEP")
    print(f"{len(subject_collapsibles)} subject collapsibles found! gettings links...")

    for sc in subject_collapsibles:
        # print(sc.get_attribute("name"))
        # expand_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.style__collapseButton___D0Xl5")))
        expand_btn = sc.find_element(By.CSS_SELECTOR, "button.style__collapseButton___D0Xl5")
        driver.execute_script("arguments[0].click();", expand_btn)
        collapse_content = sc.find_element(By.CSS_SELECTOR, "div.ReactCollapse--collapse")

        link_elements = collapse_content.find_elements(By.CSS_SELECTOR, "a")
        for le in link_elements:
            links.append(le.get_attribute("href"))
    
    # print(links)
    return links

# tried with bs4, doesn't work :(
def get_from_ucal_bs4(ucal_url: str):
    page = requests.get(ucal_url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = []
    print(page.content)

    table = soup.find("div", id="__KUALI_TLP")
    subject_listings = table.find_all("div", class_="ReactCollapse--content")

    for subject in subject_listings:
        course_link_elems = subject.find_all("a")
        course_links = [elem["href"] for elem in course_link_elems]
        links.extend(course_links)

    print(links)

#get_from_ucal("https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/courses")