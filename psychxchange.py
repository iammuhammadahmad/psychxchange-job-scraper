import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession
import re
import time
from google_sheet import GoogleSheet
import settings as config

# Google Sheet Object
gs_obj = GoogleSheet()

worksheet = gs_obj.worksheet(config.psychxchange["sheet_id"], config.psychxchange["sheet_title"])

def scrape():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # Add custom headers
    chrome_options.add_argument('--log-level=1')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver=webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(config.psychxchange["BASE_URL"])

    try:
        WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_ctl0_ContentPlaceHolder_ListAllButton'))).click()
    except Exception as e:
        print(e)
    counter = 1
    while True:
        links = driver.find_elements(By.CSS_SELECTOR, '.searchResult > .searchResultRow > a')
        for link in links:
            job={"Job URL" : link.get_attribute("href")}
            
            # If already exist in Google Sheet then ignore
            isExist=gs_obj.isExist(worksheet, job)
            if isExist:
                print("\nJOB ALREADY EXIST : ", job["Job URL"])
            else:
                scrapeJob(job["Job URL"])
                print("\nTOTAL COMPLETED JOB: ", str(counter))
                counter += 1
            time.sleep(2)
        try:
            WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_ctl0_ContentPlaceHolder_PageLinkNext'))).click()
        except Exception as e:
            break


# SCRAPTE JOB'S DETAILS AND UPLOAD TO GOOGLE SHEET
def scrapeJob(url):
    print("\nSCRAPPING START: ", url)
    job_number=''
    title=''
    jobType=''
    location=''
    listed_by=''
    listed=''
    email=''
    phone=''
    try:
        job_page = requests.get(url)
    except:
        # AGAIN REQUEST IF ANY ERROR
        print("\nRETRYING TO GET JOB'S RECORD!\n")
        job_page = requests.get(url)

    
    if job_page.status_code == 200:
        soup = BeautifulSoup(job_page.content, features="html5lib")
        
        try:
            job_number = soup.select_one('#panelContent > table > tbody > tr:nth-child(3) > td > div.contentSummary > div > table > tbody > tr:nth-child(1) > td').getText().strip()
        except Exception as error:
            print("JOB NUMBER NOT EXIST: ", error)

        try:
            title = soup.select_one('#_ctl0_ContentPlaceHolder_JobDetails__ctl0_JobDetailControl_JobDetailContent > div.detailHeader').getText().strip()
        except Exception as error:
            print("JOB TITLE NOT EXIST: ", error)
        

        try:
            jobType = soup.select_one('#panelContent > table > tbody > tr:nth-child(3) > td > div.contentSummary > div > table > tbody > tr:nth-child(2) > td').getText().split('/')[0]
        except Exception as error:
            print("JOB TYPE NOT EXIST: ", error)
        
        try:
            location = soup.select_one('#panelContent > table > tbody > tr:nth-child(3) > td > div.contentSummary > div > table > tbody > tr:nth-child(2) > td').getText().split('/')[-1]
        except Exception as error:
            print("JOB LOCATION NOT EXIST: ", error)
        
        try:
            listed_by_text = soup.select_one('#panelContent > table > tbody > tr:nth-child(3) > td > div.contentSummary > div > table > tbody > tr:nth-child(3) > td').getText().strip()
            # Regular expression pattern to match the date
            pattern = r"\d+\s+\w+\s+\d+"

            listed_by = re.sub(pattern, "", listed_by_text)
            
            listed_by = re.sub(r"\b(on)\b", "", listed_by)
            
        except Exception as error:
            print("JOB LISTED_BY NOT EXIST: ", error)

        try:
            listed = soup.select_one('#panelContent > table > tbody > tr:nth-child(3) > td > div.contentSummary > div > table > tbody > tr:nth-child(3) > td').getText().strip()
            
            # Regular expression pattern to match the date
            pattern = r"\d+\s+\w+\s+\d+"
            
            # Search for the date pattern in the text
            match = re.search(pattern, listed)

            if match:
                date = match.group()
                listed = date
            else:
                print("No date found.")


            # print("JOB LISTED: ", listed)
        except Exception as error:
            print("JOB LISTED NOT EXIST: ", error)
        
        try:
            session = HTMLSession()
            response = session.get(url)
            response.html.render(timeout=20)
            contact = response.html.find('.detailContactDetails')
            # phone_pattern = r"\(?\d{2}\)?\s?\d{4}\s?\d{4}|\d{4}\s?\d{3}\s?\d{3}"
            phone_pattern = r"\(?\d{2}\)?\s?\d{4}\s?\d{4}|\d{4}\s?\d{3}\s?\d{3}|\d{8}"



            for i in contact:
                # Remove parentheses and spaces from the phone number
                cleaned_number = re.sub(r'[()]', '', i.text)
                # match variable contains a Match object.
                phone = re.findall(phone_pattern, cleaned_number) 
                if phone:
                    phone = ', '.join(phone)
                else:
                    phone = ''
                email_pattern = r'[\w.-]+@[\w.-]+\.\w+\b'
                mail = re.findall(email_pattern, i.text)
                if mail:
                    email=', '.join(map(str,mail))
                else:
                    email = ''
        except Exception as error:
            print("Phone & Email not found: ", error)

        try:
            job={
                "Job URL": url,
                "Job Site": "Australian Psychxchange Association",
                "Title": title,
                "Type": jobType,
                "JOB NUMBER": job_number,
                "Location": location,
                "Email": email,
                "Phone": phone,
                "Listed By": listed_by,
                "Listed": listed,
                "Profession": "Psychxchange"
            }

            print(job)

            # Saving to Google Sheet
            gs_obj.add(worksheet, list(job.values()))
        except Exception as error:
            print("No Saved to Google Sheet !", error)