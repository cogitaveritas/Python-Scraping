from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from xml.dom.minidom import Document
import time
import csv
import re
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                     INITIALIZATIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
schoolUrl = "http://www.svcc.edu/schedule/coursesched/Spring/full-listing.html"

stringSemesterName = "Spring" #raw_input("Which semester should I scrape for?")
stringSemesterYear = "2012" #raw_input("Which year should I scrape for?")
stringTerm = stringSemesterName + stringSemesterYear
stringIsFirstCourse = True

targetFile = open('Sauk Valley Community College Spring 2012_data.xml', 'w')

hashDepts = {}
daysToSave = ""
timeToSave = ""
roomToSave = ""
profToSave = ""
deptAbbrevToSave = ""
courseNumToSave = ""
courseNameToSave = ""
uniqueNumToSave = ""
sectionNumToSave = ""
creditHoursToSave = ""
doc = Document()

# Create the <myEdu> base element
myEdu = doc.createElement("myedu")
myEdu.setAttribute("data-type", "schedule")
myEdu.setAttribute("version", "1")
doc.appendChild(myEdu)

# Create the <source> element
source = doc.createElement("source")
source.setAttribute("name", "DALLAS")
source.setAttribute("id", "fe80::5fb:90f5:1e9c:5995%11 2001:470:1f0f:c02:5fb:90f5:1e9c:5995 2001:470:1f0f:c02:ccd9:e1d7:fa6d:9940 10.10.0.135 ")
source.setAttribute("ami", "")
source.setAttribute("instance-id", "")
source.setAttribute("start-time", "11/4/2011 10:02:19 PM")
source.setAttribute("duration", "20969.1659696")
myEdu.appendChild(source)

# Create the <data> element
data = doc.createElement("data")
myEdu.appendChild(data)

# Create the <school> element
school = doc.createElement("school")
school.setAttribute("school-id", "2431")
school.setAttribute("name", "Sauk Valley Community College")
data.appendChild(school)

# Create the <section-list> element
sectionList = doc.createElement("section-list")
sectionList.setAttribute("semester-name", stringSemesterName)
sectionList.setAttribute("semester-year", stringSemesterYear)
data.appendChild(sectionList)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                     FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def GetDepts():
	browser.get("http://www.svcc.edu/schedule/coursesched/Spring/depts/index.html")
	mainDiv = browser.find_element_by_id('main')
	arrayDeptLinks = mainDiv.find_elements_by_tag_name('li')

	global hashDepts

	for stringTempDept in arrayDeptLinks:
		stringTempDeptValue = stringTempDept.text

		deptRegex = re.search('\(([^)]+)\)\s*(.+)', stringTempDeptValue)
		stringDeptAbbrev = deptRegex.group(1)
		stringDeptName = deptRegex.group(2)

		hashDepts[stringDeptAbbrev] = stringDeptName
	return

def CourseFunction():
	global deptAbbrevToSave
	global courseNumToSave
	global courseNameToSave

	deptAbbrevToSave = rowCourseRegex.group(1)
	courseNumToSave = rowCourseRegex.group(2)
	courseNameToSave = rowCourseRegex.group(3)

	#print deptAbbrevToSave + " " + courseNumToSave + " " + courseNameToSave
	return

def SectionFunction():
	global daysToSave
	global timeToSave
	global roomToSave
	global profToSave
	global uniqueNumToSave
	global sectionNumToSave
	global creditHoursToSave
	#print rowText
	rowSectionRegex = re.search('^(\d{5})\s+(\S+)\s+(\d+\.?\d*)?\s*([MTWThFS]+|Online|TBA|Open\sLab)\s+(\d+\:\d+-\d+\:\d+)?\s*(.+)', rowText)
	uniqueNumToSave = rowSectionRegex.group(1)
	sectionNumToSave = rowSectionRegex.group(2)
	creditHoursToSave = rowSectionRegex.group(3)
	daysToSave = rowSectionRegex.group(4)
	timeToSave = rowSectionRegex.group(5)
	roomAndProfessor = rowSectionRegex.group(6)

	roomAndProfessorRegex = re.search('^([A-Z0-9]+\s)?\s*([A-Z]+\.\s\S+)?', roomAndProfessor)
	roomRegex = roomAndProfessorRegex.group(1)
	profToSave = roomAndProfessorRegex.group(2)
	if roomRegex == None:
		roomRegex = " "
	roomRegexer = re.search('(\S+)?', roomRegex)
	roomToSave = roomRegexer.group(1)

	#if timeToSave != None:
	#	arrayTimes.append(timeToSave)

	#if roomToSave != None:
	#	arrayRooms.append(roomToSave)

	#if profToSave != None:
	#	arrayProfs.append(profToSave)

	
	return

def SaveData():

	global deptAbbrevToSave
	global courseNumToSave
	global courseNameToSave
	global hashDepts
	global daysToSave
	global timeToSave
	global roomToSave
	global profToSave
	global deptAbbrevToSave
	global courseNumToSave
	global courseNameToSave
	global uniqueNumToSave
	global sectionNumToSave
	global creditHoursToSave
	endTimeToSave = None
	startTimeToSave = None
	profFirstToSave = None
	profLastToSave = None
	meetingType = None

	#Let's first clean up and split up.
	if profToSave != None:
		profSplitRegex = re.search('([^.]+)\.\s+(.+)', profToSave)
		profFirstToSave = profSplitRegex.group(1)
		profLastToSave = profSplitRegex.group(2)

	if timeToSave != None:
		timeSplitRegex = re.search('([^:]+):([^-]+)-([^:]+):(.+)', timeToSave)
		startTimeToSave = timeSplitRegex.group(1) + timeSplitRegex.group(2)
		endTimeToSave = timeSplitRegex.group(3) + timeSplitRegex.group(4)
	else:
		startTimeToSave = "TBA"
		endTimeToSave = "TBA"

	daysToSave = re.sub('Th', 'R', daysToSave)

	if daysToSave == "Online":
		daysToSave = "TBA"
		meetingType = "online"
		if timeToSave ==  None:
			startTimeToSave = "TBA"
			endTimeToSave = "TBA"
		if roomToSave == None:
			roomToSave = "WWW"
	elif daysToSave == "Open Lab":
		daysToSave = "TBA"
	elif daysToSave != "TBA" and daysToSave != "Open Lab":
		meetingType = "in-class"

	# Create the <section> element
	section = doc.createElement("section")
	section.setAttribute("course-name", courseNameToSave)
	section.setAttribute("course-number", courseNumToSave)
	if creditHoursToSave != None:
		section.setAttribute("credit-hours", creditHoursToSave)
	section.setAttribute("dept-abbrev", deptAbbrevToSave)
	deptNameToSave = hashDepts[deptAbbrevToSave]
	section.setAttribute("dept-name", deptNameToSave)
	section.setAttribute("section-number", sectionNumToSave)
	section.setAttribute("unique-number", uniqueNumToSave)
	sectionList.appendChild(section)

	# Create the <professor-list> element
	if profFirstToSave != None or profLastToSave != None:
		profList = doc.createElement("professor-list")
		section.appendChild(profList)

	# Create the <professor> element
	if profFirstToSave != None or profLastToSave != None:
		professor = doc.createElement("professor")
		if profFirstToSave != None:
			professor.setAttribute("first-name", profFirstToSave)
		if profLastToSave != None:
			professor.setAttribute("last-name", profLastToSave)
		profList.appendChild(professor)

	#Create the <dtr-list> element
	dtrList = doc.createElement("dtr-list")
	section.appendChild(dtrList)

	# Create the <dtr> element
	dtr = doc.createElement("dtr")
	dtr.setAttribute("days", daysToSave)
	if endTimeToSave != None:
		dtr.setAttribute("end-time", endTimeToSave)
	if startTimeToSave != None:
		dtr.setAttribute("start-time", startTimeToSave)
	if roomToSave != None:
		dtr.setAttribute("room", roomToSave)
		if meetingType != None:
			dtr.setAttribute("meeting-type", meetingType)
	else:
		dtr.setAttribute("room", "TBA")
	dtrList.appendChild(dtr)



	# Print our newly created XML
	#print doc.toprettyxml(indent="  ")
	#inputTester = raw_input("Waiting...")
	return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                         MAIN PROGRAM
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

browser = webdriver.Firefox()
GetDepts()
browser.get(schoolUrl)

coursePageDiv = browser.find_element_by_id('main')
courseTable = coursePageDiv.find_element_by_tag_name('table')
arrayCourseRows = courseTable.find_elements_by_tag_name('tr')

for rowData in arrayCourseRows:
	rowText = rowData.text

	rowCourseRegex = re.search('^([A-Z]{3})\s+(\d{3})\s+(.+)', rowText)
	if rowCourseRegex != None:
		CourseFunction()
	else:
		rowSectionRegex = re.search('^(\d{5})', rowText)
		if rowSectionRegex != None:
			SectionFunction()
			SaveData()

targetFile.write(doc.toprettyxml(indent="  "))
targetFile.close()