from html.parser import HTMLParser
import os
import copy 

InComingMenuItem = False 
ExistingMenu = set()


def parse_menu():
  class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
      global InComingMenuItem
      if tag == "div" and attrs[0] == ('class', 'item-name'):
        InComingMenuItem = True

    def handle_data(self, data):
      global InComingMenuItem
      if InComingMenuItem == True:
        print("Menu Item: ", data)
        InComingMenuItem = False

  parser = MyHTMLParser()
  os.system("wget https://dining.umich.edu/menus-locations/dining-halls/bursley/")
  with open('index.html', 'r') as file:
    data = file.read().replace('\n', '')
  parser.feed(data)
  os.system("rm index.html")


def RecoverData(CurrentVersion, CurrentMenu):
  VersionFile = open("LatestVersion.txt", 'r')
  Lines = VersionFile.readlines() 
  CurrentVersion = Lines[0]
  VersionFile.close()
  print("Current Version is: " + CurrentVersion)

  MenuFile = open("Menu.txt", 'r')
  Lines = MenuFile.readlines() 

  for item in Lines:
    if item != "" and item != "\n":
      if item[-1] == "\n":
        CurrentMenu.add(item[:-1])
      else:
        CurrentMenu.add(item)


def main():
  CurrentVersion = -1
  CurrentMenu = set()

  RecoverData(CurrentVersion, CurrentMenu)
  print("Current Menu:")
  print(CurrentMenu)

  global ExistingMenu
  ExistingMenu = copy.deepcopy(CurrentMenu)
  parse_menu()

if __name__== "__main__":
  main()
