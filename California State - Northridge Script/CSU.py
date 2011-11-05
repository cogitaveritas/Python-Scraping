from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import csv

def InsertTerm():
	#This will insert the correct term data.
	browser.switch_to_frame('TargetContent')
	schoolTermBox = browser.find_element_by_name('NR_SSS_SOC_NWRK_STRM')
	schoolTermBox.find_element_by_xpath("option[text()='{0}']".format(stringTerm)).click()

	#Now to uncheck the "Open Classes" box.
	schoolOpenClassChkBox = browser.find_element_by_name('NR_SSS_SOC_NWRK_CHECK_BOX')
	schoolOpenClassChkBox.click()
	return

def CreateDeptArray():
	deptBox = browser.find_element_by_name('NR_SSS_SOC_NWRK_SUBJECT')
	deptTempArray = deptBox.find_elements_by_xpath("option")
	
	for deptTempOption in deptTempArray:
		deptTempValue = deptTempOption.text
		deptArray.append(deptTempValue)
	return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         MAIN PROGRAM START
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

schoolUrl = "https://mynorthridge.csun.edu/psp/PANRPRD/EMPLOYEE/SA/c/NR_SSS_COMMON_MENU.NR_SSS_SOC_BASIC_C.GBL?PORTALPARAM_PTCNAV=NRPA_SSS_SCHED_CLASS"

stringSemesterName = "Spring" #raw_input("Which semester should I scrape for?")
stringSemesterYear = "2012" #raw_input("Which year should I scrape for?")
stringTerm = "2123 - " + stringSemesterName + " Semester " + stringSemesterYear
deptArray = []

browser = webdriver.Firefox()
browser.get(schoolUrl)

InsertTerm()
CreateDeptArray()

for deptValue in deptArray:
	if deptValue != " ":
		print deptValue
		deptBox = browser.find_element_by_name('NR_SSS_SOC_NWRK_SUBJECT')
		deptBox.find_element_by_xpath('option[text()="{0}"]'.format(deptValue)).click()
		time.sleep(1)
	
