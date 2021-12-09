from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import chromedriver_binary
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import json

def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_token = 'token'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)


def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addrs, msg, my_password):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, my_password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()

def job(new_name):

    with open('/Users') as f:
        info = json.load(f)

    FROM_ADDRESS = info['email']
    MY_PASSWORD = info['password']

    TO_ADDRESS = 'yourname@gmail.com'
    BCC = ''
    SUBJECT = ''
    BODY = new_name
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)

def detect_update():
    submit_num = "submit"
    password = "password"

    option = Options()
    option.add_argument('--headless')

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)

    browser.implicitly_wait(10)

    browser.get("https://mash-i.com/login.html?nb=1")
    email_elem = browser.find_element_by_id("login_id")
    email_elem.send_keys(submit_num)

    password_elem = browser.find_element_by_id("login_pw")
    password_elem.send_keys(password)

    submit = browser.find_element_by_xpath("//*[@id='content']/a[1]")
    submit.click()
    time.sleep(5)

    search = browser.find_element_by_id("SubButton6")
    search.click()
    time.sleep(3)

    select_kanagawa = browser.find_element_by_xpath("//*[@id='jobsearch1']/div[2]/div[2]/fieldset[2]/div[2]/div[3]/label")
    select_kanagawa.click()

    select = browser.find_element_by_xpath("//*[@id='jobsearch1']/div[3]/a")
    select.click()
    time.sleep(3)


    job_name = browser.find_elements_by_class_name("job2work_name")
    new_name = [x.text for x in job_name]

    day_name = browser.find_elements_by_class_name("job2date")
    day = [x.text for x in day_name]

    n = len(new_name)
    job_list = []
    for i in range(n):
        job_arrign = new_name[i] + day[i]
        job_list.append(job_arrign)

    job_list =str(job_list)

    try:
        with open('/Users/old_name.txt') as f:
            old_name = f.read()
    except:
        old_name = ''

    if job_list == old_name:
        print("No change")
        return False
    else:
        with open("/Users/old_name.txt","w") as f:
            f.write(job_list)
        print("A new job has arrived")
        return True

if __name__ == '__main__':
    count = 0
    if detect_update() == True:
        count += 1
        if count % 2 == 1:
            with open('/Users/old_name.txt') as f:
                jobline = f.readline()
            send_line_notify(jobline)
        else:
            send_line_notify(jobline)
    else:
        print("No new job")
