from ordered_set import OrderedSet

def main():
    CurrentVersion = -1
    CurrentMenu = OrderedSet() 

    MenuFile = open('/Users/root1/Desktop/list.txt', 'r')
    Lines = MenuFile.readlines() 
    CurrentVersion = Lines[0]
    for i in range(1,len(Lines)):
        print(Lines[i][:-1])

        


if __name__== "__main__":
  main()
