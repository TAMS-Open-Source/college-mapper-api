import pandas as pd
import json

data_link = '../data/college_information.csv'

data = pd.read_csv(data_link)

def getIDasObj(college_id):
  college_id = int(college_id)
  
  for key, unit_id in data['unitid'].items():
    
    if college_id == unit_id:
      series = data[key:key+1].squeeze()
      seriesDict = series.to_dict()
      shortDict = {
        'unitid': int(seriesDict['unitid']),
        'lon': float(seriesDict['HD2019.Longitude location of institution']),
        'lat': float(seriesDict['HD2019.Latitude location of institution'])
      }
      return shortDict

def convertInputToJSON():

  ids = input("IDs:")
  ids = ids.split(', ')

  dicts = []
  for unitid in ids:
    obj = getIDasObj(unitid)
    dicts.append(obj)
  
  with open("../data/lat_lon.json", "w") as outfile:
    json.dump(dicts, outfile)

if __name__ == '__main__':
  convertInputToJSON()