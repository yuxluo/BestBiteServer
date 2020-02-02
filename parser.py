from html.parser import HTMLParser
import os
import copy 
import configparser
import time
import unicodedata
import xml.etree.ElementTree as ET

class DiningHallClass:
  def __init__(self):
    self.DiningHallName = ""
    self.MealHours = []
    self.MealMenus = []

class MenuClass:
  def __init__(self):
    self.dining_halls = []


Menu_of_Today = None
StringsLib = configparser.RawConfigParser()
InComingMenuItem = False
InComingHour = False

def parse_menu():
  global StringsLib
  global Menu_of_Today
  class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
      global InComingMenuItem
      global InComingHour

      if tag == "div" and attrs[0] == ('class', 'item-name'):
        InComingMenuItem = True
      elif tag == "span" and len(attrs) and attrs[0] == ('class', 'calhours-times'):
        InComingHour = True
      elif tag == "i" and len(attrs) and attrs[0] == ('class', 'fa fa-minus'):
        process_ass()

    def handle_data(self, data):
      global MenuClass
      global InComingMenuItem
      global InComingHour

      if InComingMenuItem:
        sanitized = data.strip()
        process_item(sanitized)
        InComingMenuItem = False

      elif InComingHour:
        process_hour(data)
        InComingHour = False 


  parser = MyHTMLParser()
  
  for key in StringsLib['URL']:
    process_dining_hall(key, parser)

def process_ass():
  global Menu_of_Today
  Menu_of_Today.dining_halls[-1].MealMenus.append([])
  return

def process_hour(hour_data):
  global Menu_of_Today
  Menu_of_Today.dining_halls[-1].MealHours.append(unicodedata.normalize('NFKC', hour_data))
  return

def process_item(item_name):
  Menu_of_Today.dining_halls[-1].MealMenus[-1].append(item_name)
  return

def process_dining_hall(dining_hall_name, parser):
  global StringsLib
  global Menu_of_Today

  print("@@@ Processing Today's Menu for " + dining_hall_name)
  os.system("wget " + StringsLib.get('URL', dining_hall_name) + ">/dev/null 2>&1")
  with open('index.html', 'r') as file:
    data = file.read().replace('\n', '')

  Menu_of_Today.dining_halls.append(DiningHallClass())
  Menu_of_Today.dining_halls[-1].DiningHallName = dining_hall_name
  parser.feed(data)
  os.system("rm index.html")


def write_to_file():
  global Menu_of_Today

  root = ET.Element("menu")
  
  for dining_hall_item in Menu_of_Today.dining_halls:
    dining_hall_element = ET.SubElement(root, "dininghall")
    ET.SubElement(dining_hall_element, "name").text = dining_hall_item.DiningHallName
    afternoon = False

    for i in range(len(dining_hall_item.MealHours)):
      dining_hall_item.MealHours[i] = dining_hall_item.MealHours[i].replace(':', '')
      dining_hall_item.MealHours[i] = dining_hall_item.MealHours[i].replace(' ', '')
      dining_hall_item.MealHours[i] = dining_hall_item.MealHours[i].replace('am', '')
      dining_hall_item.MealHours[i] = dining_hall_item.MealHours[i].replace('pm', '')
      period = dining_hall_item.MealHours[i].split('‐')

      period[0] = int(period[0])
      period[1] = int(period[1])

      if afternoon:
        period[0] += 1200
        period[1] += 1200
      if period[1] < period[0]:
        afternoon = True
        period[1] += 1200

      meal_element = ET.SubElement(dining_hall_element, "meal")
      meal_start_element = ET.SubElement(meal_element, "start")
      meal_end_element = ET.SubElement(meal_element, "end")
      meal_start_element.text = str(period[0])
      meal_end_element.text = str(period[1])

      for dish in dining_hall_item.MealMenus[i]:
        dish_element = ET.SubElement(meal_element, "dish")
        dish_element.text = dish

  tree = ET.ElementTree(root)
  tree.write("Menu.xml")



def main():
  global StringsLib
  global Menu_of_Today

  StringsLib.read('strings.properties')
  Menu_of_Today = MenuClass()

  while True:
    parse_menu()
    write_to_file()
    time.sleep(3600)
  

  

# def UpdateMenu():
#   global ExistingMenu
#   global UpdatedMenu
#   global CurrentVersion
#   CurrentVersion += 1

#   print("@@@ " + str(len(UpdatedMenu.difference(ExistingMenu))) + " new updates to menu")
#   print("@@@ Writing Updates to Version " + str(CurrentVersion) + " of the menu")

#   VersionFile = open("LatestVersion.txt", 'w')
#   VersionFile.writelines(str(CurrentVersion))
#   VersionFile.close()

#   MenuFile = open("Menu.txt", 'w')
#   for dish in sorted(UpdatedMenu):
#     MenuFile.writelines(dish + "\n")
#   MenuFile.close()

#   ExistingMenu = copy.deepcopy(UpdatedMenu)

if __name__== "__main__":
  main()
