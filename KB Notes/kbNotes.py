from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import csv

#This function is used to login to the IMP System when the program starts.
def loginProcedure( username, password ):
    browser.get(impURL)
    assert "Login" in browser.title
    usernameElem = browser.find_element_by_name("username")
    usernameElem.click()
    usernameElem.send_keys(username)
    passwordElem = browser.find_element_by_name("password")
    passwordElem.click()
    passwordElem.send_keys(password + Keys.RETURN)
    return

#This function will handle navigating to the "new note" page for the school with the given school ID number.
def navigateToSchool( schoolID ):
    try:
        browser.get(impURL)
        browser.find_element_by_xpath("//a[contains(@href,'/da/school-search/index?')]").click()
        school_idSearch = browser.find_element_by_id("school_id")
        school_idSearch.click()
        school_idSearch.send_keys(schoolID + Keys.RETURN)
        time.sleep(5)
        browser.find_element_by_xpath("//a[contains(@href,'/kb/note?school={0}')]".format(schoolID)).click()
        time.sleep(5)
        browser.find_element_by_xpath("//a[contains(@href,'/kb/note/add?school={0}')]".format(schoolID)).click()
        time.sleep(5)
    except NoSuchElementException: 
        print "One of more elements failed to load while navigating."
        print schoolID
        return False
        
    return True

#This function will read in a CSV file and store it as a two-dimensional array.
def valueReader():
    with open('Unsent Emails Note List C.csv', 'rb') as f:
        rowReader = csv.reader(f)
        for row in rowReader:
            arrayToInsert.append(row)
            schoolArray.append(row[1])
    return

#This function will handle actually inserting the data in the note page. It accepts an array with the appropriate information, then breaks it down into
#the correct variables.
def insertData( valueList ):
    stringTitle = 'Fall 2011 Directory Information Request'
    stringDataType = 'Directory Information'
    stringNoteType = valueList[3]
    stringNoteStatus = valueList[4]
    stringTerm = valueList[6]
    stringYear = '2011'
    stringNote = valueList[5]
    
    try:
        noteTitleElem = browser.find_element_by_id("note_title")
        noteTitleElem.click()
        noteTitleElem.send_keys(stringTitle)

        dataTypeElem = browser.find_element_by_id("data_type")
        dataTypeElem.find_element_by_xpath("option[text()='{0}']".format(stringDataType)).click()
        time.sleep(2)

        noteTypeElem = browser.find_element_by_id("note_type")
        noteTypeElem.find_element_by_xpath("option[text()='{0}']".format(stringNoteType)).click()
        time.sleep(2)

        noteStatusElem = browser.find_element_by_id("note_status")
        noteStatusElem.find_element_by_xpath("option[text()='{0}']".format(stringNoteStatus)).click()
        time.sleep(2)

        termElem = browser.find_element_by_id("term")
        termElem.find_element_by_xpath("option[text()='{0}']".format(stringTerm)).click()
        time.sleep(2)

        termYearElem = browser.find_element_by_id("term_year")
        termYearElem.click()
        termYearElem.send_keys(stringYear)
        time.sleep(2)

        noteElem = browser.find_element_by_id("note")
        noteElem.click()
        noteElem.send_keys(stringNote)
        time.sleep(2)

        #This section is what actually inserts the data. LEAVE THIS COMMENTED OUT until you are sure that you wish to insert the data. At that point, uncomment the lines relating to clickyClick.
        #clickyElem = browser.find_element_by_name("Create")
        #clickyElem.click()
        #time.sleep(2)
    except NoSuchElementException:
        print "One or more elements failed to load on this page."
        return False

    return True

#Hard-Coded Data Declarations
impURL = "http://imp.myedu.com"
insertSuccessVar = False
navToSchoolVar = False
count = 0
schoolArray = []
arrayToInsert = []

#End Declarations

#Main Program
browser = webdriver.Firefox()

valueReader()

loginProcedure("scraper@myedu.com", "password1")

for i in schoolArray:
    while not navToSchoolVar:
        navToSchoolVar = navigateToSchool(i)

    while not insertSuccessVar:
        insertSuccessVar = insertData( arrayToInsert[count] )

    count = count + 1
    insertSuccessVar = False
    navToSchoolVar = False
    browser.get(impURL)
