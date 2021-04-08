# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 01:30:28 2021

@author: Nathaniel
"""
#https://www.usnews.com/best-graduate-schools/api/search?program=top-engineering-schools&specialty=eng&_page=2
#https://www.usnews.com/best-graduate-schools/api/search?program=top-business-schools&specialty=international-business
import requests
from bs4 import BeautifulSoup as soup

# TODO: refactor for code consistency
# TODO: add libraries

class Major:
    def __init__(self, major, majorValue):
        self.major = major
        self.majorValue = majorValue

class Specialties:
    def __init__(self, specialty, specmajorValue , specialtyValue):
        self.specialty = specialty
        self.specmajorValue = specmajorValue
        self.specialtyValue = specialtyValue




def getMajors():
    
    majorArray = []
    programsURL = 'https://www.usnews.com/best-graduate-schools/search'
    headers = {'User-Agent':'Mozilla/5.0'}

    majReq = requests.get(programsURL, headers = headers)
    majData = soup(majReq.text, "html5lib")
    
    rawMajors = majData.find("div", id = "ProgramRankings")
    for majorName in rawMajors.findAll("option"):
        if (majorName['value'] != ""):
                if (majorName['value'] == 'top-audiology-schools'):
                    majorArray.append(Major(majorName.string, 'top-health-schools'))
                elif(majorName['value'] == 'top-biological-sciences-schools'):
                    majorArray.append(Major(majorName.string, 'top-science-schools'))
                elif(majorName['value'] == 'top-criminology-schools'):
                    majorArray.append(Major(majorName.string, 'top-humanities-schools'))
                else:
                    majorArray.append(Major(majorName.string, majorName['value']))
                    #print(majorName['value'])
                    # print(majorName.string)
    return majorArray

def getSpecialties(majorArray):    
    headers = {'User-Agent':'Mozilla/5.0'}
    majorSpecialties = []
    broadSciSpec = []
    for value in majorArray:
         if(value.majorValue == 'top-science-schools'):
             specialtyURL = 'https://www.usnews.com/best-graduate-schools/' + value.majorValue
             specReq = requests.get(specialtyURL, headers = headers)
             specData = soup(specReq.text, "html5lib")
            
             rawSpec = specData.find("select", id = "specialty")
             for specName in rawSpec.findAll("option"):
                if(specName['value'] != "default"):                        
                    majorSpecialties.append(Specialties(specName.string.replace('/', '-').replace(':', '-'), value.majorValue, specName['value']))
                    if(specName['value'] != 'statistics'):
                       broadSciSpec.append(specName['value'])
                    #print(specName.string)
                    #print(specName['value'])                
             for specSciVal in broadSciSpec:
                 specialtyURL = 'https://www.usnews.com/best-graduate-schools/top-science-schools/' + specSciVal + '-rankings'
                 specReq = requests.get(specialtyURL, headers = headers)
                 specData = soup(specReq.text, "html5lib")
                 rawSpec = specData.find("div", id = "ProgramRankings")
                 firstBox = rawSpec.find("div", spacing = "3")
                 secondBox = firstBox.find_next("div", spacing = "3")
                 thirdBox = secondBox.find_next("div", spacing = "3")
                 default = thirdBox.find_next("option")
                 for specName in default.find_all_next("option"):
                         majorSpecialties.append(Specialties(specName.string.replace('/', '-').replace(':', '-'), value.majorValue, specName['value']))
                         #print(specName.string)
                         #print(specName['value'])
         else: 
             specialtyURL = 'https://www.usnews.com/best-graduate-schools/' + value.majorValue
             #print(specialtyURL)
             # print(value.majorValue)
             specReq = requests.get(specialtyURL, headers = headers)
             specData = soup(specReq.text, "html5lib")
            
             rawSpec = specData.find("select", id = "specialty")
             for specName in rawSpec.findAll("option"):
                    if(specName['value'] != "default"):                        
                        majorSpecialties.append(Specialties(specName.string.replace('/', '-').replace(":", "-"), value.majorValue, specName['value']))
                        #print(specName.string)
                        #print(specName['value'])
    return majorSpecialties