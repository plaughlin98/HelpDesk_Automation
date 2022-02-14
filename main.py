import AppKit
import logging
import config
import pyautogui
import time
import webbrowser
from os import system
from datetime import datetime
from selenium import webdriver
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with


USER = config.USER
PASS = config.PASS
print(PASS)
pyautogui.FAILSAFE = True

def getWebDriver():
    driver = webdriver.Chrome()
    driver.maximize_window() # For maximizing window
    driver.implicitly_wait(20)
    driver.get(config.SITE_URL)
    return driver

def signIn(driver, username, password):
    inputUserElement = driver.find_element(By.ID, 'sso_username')
    inputPassElement = driver.find_element(By.ID, 'ssopassword')
    inputUserElement.send_keys(username)
    inputPassElement.send_keys(password)
    inputPassElement.send_keys(Keys.ENTER)
    agreeButton = driver.find_element(By.XPATH,'//button[text()="I AGREE"]')
    agreeButton.click()
    notificationsButton = driver.find_element(By.ID, 'rejectDesktopNotifications')
    time.sleep(1)
    notificationsButton.click()

# def createTextMessage(text, timeRemaining):
#     textToSend = "Time Remaining: " + timeRemaining + " | " + text
#     sms.sendMessage(textToSend)

def checkHelpdesk(driver, previousCount, timeRemaining):
    helpDeskSpan = driver.find_element(By.XPATH,'//span[text()="Helpdesk"]')
    helpDeskRecord = driver.find_element(locate_with(By.CLASS_NAME, "dijitImageAccordionRowCount").to_right_of(helpDeskSpan))
    time.sleep(.5)
    helpDeskRecordText = "Helpdesk " + helpDeskRecord.text[8:-1]
    helpDeskCount = helpDeskRecord.text[15:-1]
    try:
        helpDeskCount = int(helpDeskCount.replace(" ", ""))
    except:
        print("Page not loaded")
        time.sleep(1)
        driver.refresh()
        time.sleep(5)
        checkHelpdesk(driver, 0, timeRemaining)

    print("Previous Count: ", previousCount)
    print("Current Count: ", helpDeskCount)
    if previousCount != helpDeskCount:
        sayAlerts(helpDeskRecordText)
        sayAlerts(timeRemaining)
    checkForS1(driver)
    return helpDeskCount
    
def checkForS1(driver):
    try:
        severity1Element = driver.find_element(By.XPATH,'//td[text()="1-Critical"]')
    except:
        print("No Severity 1's")
        print("\n\n")
    else:
        sayAlerts("Severity 1 on HelpDesk")
        # createTextMessage("Severity 1 on Helpesk")

def sayAlerts(text):
    system("say -v 'Alex' " + "'" + text + "'")

def convertHour(hour):
    howLongInt = float(hour) * 3600
    return howLongInt

def formatTime(time):
    time = abs(time)
    hours = int(time)
    minutes = (time*60) % 60
    seconds = (time*3600) % 60

    if hours < 1:
        return "Time Remaining is: %02d minutes and %02d seconds" % (minutes, seconds)
    elif hours == 1:
        return "Time Remaining is: %d hour %02d minutes and %02d seconds" % (hours, minutes, seconds)
    else:
        return "Time Remaining is: %d hours %02d minutes and %02d seconds" % (hours, minutes, seconds)

### MAIN LOOP ###

def mainLoop():
    howLong = input("How many hours?")
    whatType = input("HD or Drop?").lower()
    timeout = convertHour(howLong)
    timeout_start = time.time()
    
    if whatType == "drop":
        while time.time() < timeout_start + timeout:
            pyautogui.FAILSAFE = True
            mouse_pos = pyautogui.position()
            
            pyautogui.moveRel(0, 100, duration=1)
            pyautogui.moveRel(0, -100, duration=1)
            timeString = (time.time() - (timeout_start + timeout)) / 3600
            sayAlerts(formatTime(timeString))
            time.sleep(60)

    elif whatType == "hd":
        try:
            driver = getWebDriver()
            signIn(driver, USER, PASS)
            time.sleep(5)
            previousCount = 0
            
            while time.time() < timeout_start + timeout:
                timeString = (time.time() - (timeout_start + timeout)) / 3600
                time.sleep(3)
                previousCount = checkHelpdesk(driver, previousCount, formatTime(timeString))
                pyautogui.moveRel(0, -1, duration=0.1)
                pyautogui.moveRel(0, 1, duration=0.1)
                time.sleep(21)
                driver.refresh()

        except Exception as Argument:
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            f = open("errors.txt", "a")
            f.write(date_time + "\n")
            f.write(str(Argument))
            f.write("\n")
            f.close()

    else:
        print("Not an option, please type either 'HD' or 'Drop")
        mainLoop()

    sayAlerts("Program is over.")

if __name__ == "__main__":
    mainLoop()      