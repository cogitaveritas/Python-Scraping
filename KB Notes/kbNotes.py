from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

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
    except missingNavElementException:
        assert 0, "One of more elements failed to load while navigating."
        return False
        
    return True

#This function will handle actually inserting the data in the note page. It accepts an array with the appropriate information, then breaks it down into
#the correct variables.
def insertData( valueList ):
    stringTitle = valueList[0]
    stringDataType = valueList[1]
    stringNoteType = valueList[2]
    stringNoteStatus = valueList[3]
    stringTerm = valueList[4]
    stringYear = valueList[5]
    stringNote = valueList[6]
    
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
    except missingElementException:
        assert 0, "One or more elements failed to load on this page."
        return False

    return True

#Hard-Coded Data Declarations
impURL = "http://imp.myedu.com"
insertSuccessVar = False
navToSchoolVar = False
schoolArray = ("206", "2719")

arrayToInsert = ["Title", "Directory Information", "Skip Request", "Not Considered Directory Information", "Fall", "2011", "This was created by an automated script."]
#End Declarations

#Main Program
browser = webdriver.Firefox()

loginProcedure("scraper@myedu.com", "password1")

for i in schoolArray:
    insertSuccessVar = False
    navToSchoolVar = False
    while not navToSchoolVar:
        navToSchoolVar = navigateToSchool(i)

    while not insertSuccessVar:
        insertSuccessVar = insertData( arrayToInsert )
        
    browser.get(impURL)
