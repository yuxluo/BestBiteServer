

def main():
  CurrentVersion = -1
  CurrentMenu = set()

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

  
  print("Current Menu:")
  print(CurrentMenu)

        
if __name__== "__main__":
  main()
