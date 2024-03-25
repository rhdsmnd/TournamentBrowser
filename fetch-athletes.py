import os.path

from bottle import route, run, view
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import time

athleteRegex = re.compile(r"(?P<belt>.*)/(?P<age>.*)/(?P<gender>.*)/\s+(?P<weightclass>Open Class|[a-zA-Z\-]+)\s+(\((?P<weightclasslimit>.*)\))?(?P<name>.*)")



maleBrackets = 'https://www.bjjcompsystem.com/tournaments/{}/categories?gender_id=1'
femaleBrackets = 'https://www.bjjcompsystem.com/tournaments/{}/categories?gender_id=2'
bracketXpath = '//a[./div/div[contains(., \'{}\')] and //*[contains(., \'{}\') and contains(., \'{}\')]]'


def fetchAthletes(browser, eventIds):
    ibjjfEventId = eventIds['ibjjfId']

    floPrefix = ''
    hasFloLink = eventIds.get('floId') is not None
    if hasFloLink:
        floPrefix = 'https://www.flograppling.com/events/{}/videos?search='.format(eventIds['floId'])

    registeredPplURL = 'https://www.ibjjfdb.com/ChampionshipResults/{}/PublicAcademyRegistration?lang=en-US'.format(
        ibjjfEventId)
    browser.get(registeredPplURL)
    time.sleep(10)
    athleteTable = browser.find_element(By.XPATH, "//*[contains(text(),'Unity Jiu-jitsu')]/following-sibling::table")
    athleteRows = athleteTable.find_elements(By.XPATH, ".//tr")
    athletes = []
    for athleteRow in athleteRows:
        m = athleteRegex.match(athleteRow.text)
        if m is None:
            print("Didn't match: " + athleteRow.text)
            continue
        athlete = {}
        for k, v in m.groupdict().items():
            if v is None:
                print("No value for key: " + k)
                continue
            athlete[k] = v.strip()
        if hasFloLink:
            athlete['flolink'] = floPrefix + athlete['name'].replace(" ", "%20")
        athletes.append(athlete)
    return athletes

def addBrackets(browser, athletes, eventIds):
    ibjjfEventId = eventIds['ibjjfId']

    browser.get(maleBrackets.format(ibjjfEventId))
    time.sleep(5)
    for athlete in athletes:
        if athlete['gender'] != 'Male':
            continue
        # print(athlete)
        try:
            bracketURL = browser.find_element(By.XPATH, bracketXpath.format(athlete['age'], athlete['belt'], athlete['weightclass'].replace("-", " ")))
            athlete['bracket'] = bracketURL.get_attribute('href')
        except NoSuchElementException:
            print("Could not find bracket url for athlete: {}".format(athlete['name']))

    browser.get(femaleBrackets.format(ibjjfEventId))
    time.sleep(5)
    for athlete in athletes:
        if athlete['gender'] != 'Female':
            continue
        try:
            bracketURL = browser.find_element(By.XPATH, bracketXpath.format(athlete['age'], athlete['belt'], athlete['weightclass'].replace("-", " ")))
            athlete['bracket'] = bracketURL.get_attribute('href')
        except NoSuchElementException:
            print("Could not find bracket url for athlete: {}".format(athlete['name']))

def readAthleteData(eventIds, force = False):
    ibjjfEventId = eventIds['ibjjfId']
    athletesFilename = "{}-athletes.json".format(ibjjfEventId)
    if force or not os.path.isfile(athletesFilename):
        print("Downloading athlete data for event {}".format(ibjjfEventId))
        browser = webdriver.Chrome()

        athletes = fetchAthletes(browser, eventIds)
        addBrackets(browser, athletes, eventIds)

        with open(athletesFilename, 'w') as outfile:
            print("writing athlete data to {}".format(athletesFilename))
            outfile.write(json.dumps(athletes, indent=4))
    with open(athletesFilename, 'r') as infile:
        return json.load(infile)


# TODO: Use Selenium to generate a list of upcoming events
events = [
    {
        'name': "Pan IBJJF Jiu-Jitsu Championship 2024",
        'date': 'March 20th - 24th, 2024',
        'ibjjfId': '2359',
        'floId': '11804592-2024-pan-jiu-jitsu-ibjjf-championship'
    },
    {
        'name': "New York Open 2024",
        'date': 'April 6th - 7th, 2024',
        'ibjjfId': '2394'
    },
    {
        'name': "New York Open No-Gi 2024",
        'date': 'April 6th - 7th, 2024',
        'ibjjfId': '2395'
    },
    {
        'name': "World IBJJF Jiu-Jitsu Championship 2024",
        'date': 'May 29th - June 2nd, 2024',
        'ibjjfId': '2465'
    }
]

eventsMap = {}
for event in events:
    eventsMap[event.get('ibjjfId')] = event

# for event in events:
#     readAthleteData(event)
# print(json.dumps(athletes, indent=4))

@route('/')
@view('index')
def home():
    return dict(events=events)

@route('/events/<ibjjfId>')
@view('event')
def event(ibjjfId):
    athletesFilename = "{}-athletes.json".format(ibjjfId)
    print(eventsMap[ibjjfId])
    with open(athletesFilename, 'r') as infile:
        athletes = json.load(infile)
        return dict(event=eventsMap[ibjjfId], athletes=athletes)


run(host='localhost', port=8080, debug=True)