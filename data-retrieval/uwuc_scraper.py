import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_courses_from_ucal(ucal_url: str):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(ucal_url)
    courses = []
    print("driver setup, finding subject listings!")

    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.style__groups___IUc1d")))
    subject_collapsibles = table.find_elements(By.CSS_SELECTOR, "div.style__collapsibleBox___DBqEP")
    print(f"{len(subject_collapsibles)} subject collapsibles found! getting courses...")

    for sc in subject_collapsibles:
        # print(sc.get_attribute("name"))
        # expand_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.style__collapseButton___D0Xl5")))
        expand_btn = sc.find_element(By.CSS_SELECTOR, "button.style__collapseButton___D0Xl5")
        driver.execute_script("arguments[0].click();", expand_btn)
        collapse_content = sc.find_element(By.CSS_SELECTOR, "div.ReactCollapse--collapse")

        link_elements = collapse_content.find_elements(By.CSS_SELECTOR, "a")
        for le in link_elements:
            courses.append(le.text.split(" - ")[0])
    
    # print(courses)
    return courses

def get_subjects_from_ucal(ucal_url: str):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(ucal_url)
    subjects = []
    print("driver setup, finding subject listings!")

    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.style__groups___IUc1d")))
    subject_collapsibles = table.find_elements(By.CSS_SELECTOR, "div.style__collapsibleBox___DBqEP")
    print(f"{len(subject_collapsibles)} subject collapsibles found! getting subjects...")

    for sc in subject_collapsibles:
        subject_str = sc.get_attribute("name")
        split_subject_str = subject_str.split("(")
        subject_entry = {}
        subject_entry["subjectCode"] = split_subject_str[-1].strip(" )")
        subject_entry["subjectName"] = "(".join(split_subject_str[:-1]).strip()
        subjects.append(subject_entry)

    return subjects

subs = get_subjects_from_ucal("https://uwaterloo.ca/academic-calendar/undergraduate-studies/catalog#/courses")
with open("ucal-subjects.json", "w") as fo:
    json.dump(subs, fo, indent=2)