# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:55:17 2021

@author: Nathaniel
"""
import csv 
import json 
import USnewsscraper
import requests
import os

# TODO: reformat for consistent styling
# TODO: add libraries to requirements.txt

# class TopSchool():
#     def __init__(self, name, unitID, rank):
#         self.name = name
#         self.unitID = unitID
#         self.rank = rank

class TopSchools:
    def __init__(self, major, college, unitID):
        self.major = major
        self.college = college
        self.unitID = unitID
        
# class TopSpecialtySchools():
#     def __init__(self, specialties, rank):
#         self.specialties = []
#         self.rank = []
def getCollegeRankings():
    college_information = []
    majorArray = []
    specialtiesArray = []
    TopSchoolArray = []
    CollegeArray = []
    
    
    csvFilePath = r'college_information.csv'
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 
    
        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            college_information.append(row)
        
        dcollege_information = json.dumps(college_information)
        text_file = open('college_information.json', 'w')
        text_file.write(dcollege_information)
        text_file.close()
        with open('college_information.json', 'r') as json_file:
            jsoncollege_information = json.load(json_file)
        
        
    majorArray = USnewsscraper.getMajors()
    specialtiesArray = USnewsscraper.getSpecialties(majorArray)
    
    
    for major in majorArray:
       RankArray = []
       CollegeArray = []
       for x in range(1, 4):
            majorURL = 'https://www.usnews.com/best-graduate-schools/api/search?program=' + major.majorValue + '&_page=' + str(x)
            #    print(majorURL)
            headers = {'User-Agent':'Mozilla/5.0'}
            
            majReq = requests.get(majorURL, headers = headers)
            
            jsonD = json.dumps(majReq.text)
            jsonMajData = json.loads(jsonD)
            # with open (jsonD) as json_file:
            #     jsonMajData = json.loads(json_file)
            #     for item in jsonMajData['data']['items']:
            #         print(item['name']) 
            # majorData = json.loads(jsonMajorData.decode('UTF-8','strict'))
            #print(jsonMajorData)
            text_file = open(major.major + ".json", "w")
            text_file.write(jsonMajData)
            text_file.close()
            
            with open( major.major +'.json') as json_file:
                data = json.load(json_file)
                for p in data['data']['items']:
                    tempID = "0"
                    for i in jsoncollege_information:
                        if i['institution name'] in p['name'].replace('--', '-'):
                             #print(i['unitid'])
                            tempID = i['unitid']
                    CollegeArray.append(p['name'])
                    RankArray.append(tempID)
            os.remove(major.major + '.json')
       TopSchoolArray.append(TopSchools(major.majorValue, CollegeArray, RankArray))
    
        
        
    for major in specialtiesArray:
        RankArray = []
        CollegeArray = []
        for x in range(1, 4):
            majorURL = 'https://www.usnews.com/best-graduate-schools/api/search?program=' + major.specmajorValue + '&specialty='+ major.specialtyValue + '&_page=' + str(x)
            # print(majorURL)
            headers = {'User-Agent':'Mozilla/5.0'}
            
            majReq = requests.get(majorURL, headers = headers)
            
            jsonD = json.dumps(majReq.text)
            jsonMajData = json.loads(jsonD)
            # with open (jsonD) as json_file:
            #     jsonMajData = json.loads(json_file)
            #     for item in jsonMajData['data']['items']:
            #         print(item['name']) 
            # majorData = json.loads(jsonMajorData.decode('UTF-8','strict'))
            #print(jsonMajorData)
            
            text_file = open(major.specialty + ".json", "w")
            text_file.write(jsonMajData)
            text_file.close()
            
            with open( major.specialty + '.json', 'r') as json_file:
                data = json.load(json_file)
                for p in data['data']['items']:
                    tempID = "0"
                    for i in jsoncollege_information:
                        if i['institution name'] in p['name'].replace('--', '-'):
                             #print(i['unitid'])
                            tempID = i['unitid']
                    CollegeArray.append(p['name'])
                    RankArray.append(tempID)
            os.remove(major.specialty + '.json')
            
        TopSchoolArray.append(TopSchools(major.specialtyValue, CollegeArray, RankArray)) 
    
    
    with open('college_ranking.json', 'w') as f:
        f.write(json.dumps([ob.__dict__ for ob in TopSchoolArray]))
                # for i in college_information['']
        # for s in range(len(jsonMajData["data"]["items"])):
        #     print((jsonMajData[s]['name']))
        #  for item in jsonMajData['data']['items']:
        #     print(item['name']) 