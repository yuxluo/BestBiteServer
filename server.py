from html.parser import HTMLParser
import os
import copy 
import configparser
import time

InComingMenuItem = False 
ExistingMenu = set()
UpdatedMenu = set()
StringsLib = configparser.RawConfigParser()
CurrentVersion = -1

def parse_menu():
  global StringsLib
  class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
      global InComingMenuItem
      if tag == "div" and attrs[0] == ('class', 'item-name'):
        InComingMenuItem = True

    def handle_data(self, data):
      global InComingMenuItem
      global UpdatedMenu

      if InComingMenuItem == True:
        sanitized = data.strip()
        if sanitized not in UpdatedMenu:
          UpdatedMenu.add(sanitized)
      InComingMenuItem = False

  parser = MyHTMLParser()
  
  for key in StringsLib['URL']:
    process_dining_hall(key, parser)

def process_dining_hall(dining_hall_name, parser):
  global StringsLib
  print("@@@ Processing Today's Menu for " + dining_hall_name)
  os.system("wget " + StringsLib.get('URL', dining_hall_name) + ">/dev/null 2>&1")
  with open('index.html', 'r') as file:
    data = file.read().replace('\n', '')
  parser.feed(data)
  os.system("rm index.html")


def RecoverData():
  global ExistingMenu
  global CurrentVersion

  VersionFile = open("LatestVersion.txt", 'r')
  Lines = VersionFile.readlines() 
  CurrentVersion = int(Lines[0])
  VersionFile.close()
  print("Current Version is: " + str(CurrentVersion))

  MenuFile = open("Menu.txt", 'r')
  Lines = MenuFile.readlines() 

  for item in Lines:
    if item != "" and item != "\n":
      if item[-1] == "\n":
        ExistingMenu.add(item[:-1])
      else:
        ExistingMenu.add(item)

  MenuFile.close()
  print("Current Menu:")
  print(ExistingMenu)


def main():
  global StringsLib
  global ExistingMenu
  global UpdatedMenu
  global CurrentVersion

  StringsLib.read('strings.properties')
  RecoverData()
  UpdatedMenu = copy.deepcopy(ExistingMenu)

  while True:
    parse_menu()
    if len(UpdatedMenu.difference(ExistingMenu)) != 0:
      UpdateMenu()
    else:
      print("@@@ No New Update")
    time.sleep(3600)
  

  

def UpdateMenu():
  global ExistingMenu
  global UpdatedMenu
  global CurrentVersion
  CurrentVersion += 1

  print("@@@ " + str(len(UpdatedMenu.difference(ExistingMenu))) + " new updates to menu")
  print("@@@ Writing Updates to Version " + str(CurrentVersion) + " of the menu")

  VersionFile = open("LatestVersion.txt", 'w')
  VersionFile.writelines(str(CurrentVersion))
  VersionFile.close()

  MenuFile = open("Menu.txt", 'w')
  for dish in sorted(UpdatedMenu):
    MenuFile.writelines(dish + "\n")
  MenuFile.close()

  ExistingMenu = copy.deepcopy(UpdatedMenu)

if __name__== "__main__":
  main()
