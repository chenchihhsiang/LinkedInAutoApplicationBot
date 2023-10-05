from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import json
import time

class EasyApplyLinkedin:
    def __init__(self, data):
        """Parameter initialization"""
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach',True)
        s = Service(data['driver_path'])
        self.driver = webdriver.Chrome(service=s, options=options)
        
    def discard(self):
        if len(self.driver.find_elements(By.XPATH, "//button[@aria-label='Dismiss']")) > 0:
            time.sleep(2)
            #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss']"))).click()
            dismiss  = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
            time.sleep(2)
            dismiss.send_keys(Keys.RETURN)
            time.sleep(3)
            if len(self.driver.find_elements(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")) > 0:
                time.sleep(2)
                confitm_dismiss  = self.driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")
                confitm_dismiss.send_keys(Keys.RETURN)
                time.sleep(3)

    def login_linkedin(self):
        """The function for logging into Linkedin Profile"""
        url = "http://www.linkedin.com/login"
        self.driver.get(url)

        self.driver.maximize_window()

        self.driver.refresh()
        time.sleep(2)

        # introduce our email/password and hit sign-in
        login_email = self.driver.find_element(By.ID, 'username')
        login_email.clear()
        login_email.send_keys(self.email)
        login_password = self.driver.find_element(By.ID, 'password')
        login_password.clear()
        login_password.send_keys(self.password)
        time.sleep(1)
        login_password.send_keys(Keys.RETURN)
        print("...Login successfully...")

    def jobs_search(self):
        """This function goes to the 'Jobs' section a looks for all the jobs that matches the keywords and location"""
        
        # go to Jobs
        self.driver.implicitly_wait(10)
        jobs_link = self.driver.find_element(By.LINK_TEXT, 'Jobs')
        jobs_link.click()

        # introduce our keyword/location and hit ENTER
        time.sleep(1)
        search_keywords = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label*="Search by title, skill, or company"]')
        search_keywords.clear()
        search_keywords.send_keys(self.keywords)
        search_location = self.driver.find_element(By.CSS_SELECTOR, 'input[aria-label*="zip"]')
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(1)
        search_location.send_keys(Keys.RETURN)
        

    def filter(self):
        """This function filters all the job results by 'Easy Apply' """

        # locate "Easy Apply" btn and click it
        time.sleep(1)
        easy_apply_switch = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Easy Apply filter"]')
        easy_apply_switch.click()
        print("...Checked Easy Apply...")

        # locate "Date posted" and "Past month" checkbox and check it
        time.sleep(2)
        date_posted_btn = self.driver.find_element(By.ID, 'searchFilter_timePostedRange')
        date_posted_btn.click()
        print("...Clicked Date Posted...")
        time.sleep(5)
        #WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Past week')]"))).click()
        #print("...Checked Past week...")
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Past month')]"))).click()
        print("...Checked Past month...")

        # locate "Show results" btn anc click it
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(., 'Show')]"))).click()
        print("...Show Results...")
        
    def find_offers(self):
        """This function finds all the offers through all the pages result of the search and filter"""

        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        time.sleep(1)
        total_results = self.driver.find_element(By.CLASS_NAME, "display-flex.t-normal.t-12.t-black--light.jobs-search-results-list__text")
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print(total_results_int)
        time.sleep(1)

        # get results for the first page
        current_page = self.driver.current_url
        results = self.driver.find_elements(By.CLASS_NAME, "ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item")

        # for each job add, submits application if no questions asked
        # applying jobs for the 1st page
        """
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = result.find_elements(By.CLASS_NAME, "disabled.ember-view.job-card-container__link.job-card-list__title")
            for title in titles:
                time.sleep(1)
                self.submit_apply(title)
        """
        # applying jobsfor the rests of pages
        if total_results_int > 24:
            starting_page = 1
            total_pages = 15
            for page_number in range(25 * (starting_page-1), 25 * total_pages, 25):
                print("============ Change to the page " + str((page_number/25)+1) + " ============")
                self.driver.get(current_page + '&start=' + str(page_number))
                time.sleep(3)
                results_ext = self.driver.find_elements(By.CLASS_NAME, "ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item")
                time.sleep(2)
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements(By.CLASS_NAME, "disabled.ember-view.job-card-container__link.job-card-list__title")
                    time.sleep(1)
                    for title_ext in titles_ext:
                        self.submit_apply(title_ext)
            else:
                self.close_session()

    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""
        
        print('You are applying to the position of: ', job_add.text)
        job_add.click()
        time.sleep(3)

        # click on the easy apply button, skip if already applied to the position
        try:
            time.sleep(3)
            try:
                self.driver.find_element(By.XPATH, "//span[contains(., 'Easy Apply')]").click()
                time.sleep(1)
            except StaleElementReferenceException:
                print("...Something went wrong but recovered...")
                return
            print("...Clicked Easy Apply ...")
        except NoSuchElementException:
            print('You already applied to this job, go to next...')
            return

        # try to submit if submit application is available...
        # next button
        next_count = 0
        while len(self.driver.find_elements(By.XPATH, "//button[@aria-label='Continue to next step']")) > 0:
            if next_count < 15:
                next_count += 1
                time.sleep(1)
                try:
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Continue to next step']"))).click()
                except TimeoutException:
                    print("...Something went wrong but recovered...")
                    discard()
                #next  = self.driver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']")
                #next.send_keys(Keys.RETURN)
                time.sleep(1)
            else:
                time.sleep(1)
                discard = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
                print("Cannot autofill the required infomation, exit and go to the next position")
                return

        # review button
        review_count = 0
        while len(self.driver.find_elements(By.XPATH, "//button[@aria-label='Review your application']")) > 0:
            if review_count < 10:
                review_count += 1
                time.sleep(1)
                try:
                    WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Review your application']"))).click()
                except TimeoutException:
                    print("...Something went wrong but recovered...")
                    discard()
                #review = self.driver.find_element(By.XPATH, "//button[@aria-label='Review your application']")
                #review.send_keys(Keys.RETURN)
                time.sleep(1)
            else:
                time.sleep(1)
                discard = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(3)
                print("Cannot autofill the required infomation, exit and go to the next position")
                return

        # submit button
        while len(self.driver.find_elements(By.XPATH, "//button[@aria-label='Submit application']")) > 0:
            time.sleep(1)
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit application']"))).click()
            except (TimeoutException, ElementClickInterceptedException) as e:
                print("...Something went wrong but recovered...")
                if len(self.driver.find_elements(By.XPATH, "//button[@aria-label='Dismiss']")) > 0:
                    time.sleep(1)
                    try:
                        time.sleep(1)
                        dismiss  = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                        time.sleep(1)
                        dismiss.send_keys(Keys.RETURN)
                    except TimeoutException:
                        discard()
                    #dismiss  = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                    #time.sleep(2)
                    #dismiss.send_keys(Keys.RETURN)
                    time.sleep(3)
                    if len(self.driver.find_elements(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")) > 0:
                        time.sleep(2)
                        confitm_dismiss  = self.driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")
                        confitm_dismiss.send_keys(Keys.RETURN)
                        time.sleep(3)
                return
            #submit = self.driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
            #submit.send_keys(Keys.RETURN)
            print("Successfully submit the application")
            time.sleep(2)
        
        """
        try:
            time.sleep(1)
            submit = self.driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
            submit.send_keys(Keys.RETURN)
            print("Successfully submit the application")
            time.sleep(2)
        # ... if not available, discard application and go to next
        except NoSuchElementException:
            print('Not direct application, going to next...')
            try:
                time.sleep(1)
                discard = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                time.sleep(1)
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = self.driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")
                time.sleep(2)
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(3)
            except NoSuchElementException:
                return
        """
        
        if len(self.driver.find_elements(By.XPATH, "//button[@aria-label='Dismiss']")) > 0:
            time.sleep(2)
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss']"))).click()
            except TimeoutException:
                discard()
            #dismiss  = self.driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
            #time.sleep(2)
            #dismiss.send_keys(Keys.RETURN)
            time.sleep(1)
            if len(self.driver.find_elements(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")) > 0:
                time.sleep(2)
                confitm_dismiss  = self.driver.find_element(By.XPATH, "//button[@data-control-name='discard_application_confirm_btn']")
                confitm_dismiss.send_keys(Keys.RETURN)
                time.sleep(3)

    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        bot.login_linkedin()
        time.sleep(20)
        bot.jobs_search()
        time.sleep(3)
        bot.filter()
        time.sleep(3)
        bot.find_offers()
        time.sleep(2)
        bot.close_session()

if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()

