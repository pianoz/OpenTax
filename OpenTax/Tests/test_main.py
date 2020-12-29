def state():
    print("ran state")
    return

def federal():
    print("ran federal")
    return

def away():
    print("Unsucessfully ran away")
    return

class MenuGenerator:
    def __init__(self, menu, options, functionlist):
        self.menu = menu
        self.options = options
        self.offset = (68-len(menu)/2)
        self.functionlist  = functionlist

    def display(self):
        print(f"--------------------------------------------------------------------\n                         ",
              self.menu, "                          \n"
                         "--------------------------------------------------------------------\n")
        while 1:
            y = 0
            for x in self.options:
                print(y, " = ", x, "\n")
                y += 1
            crsr = input("\n: ")
            if crsr == 'q':
                return
            if int(crsr) in range(0,len(self.options)-1):
                self.functionlist[int(crsr)]()
            else:
                print("Input Not Recognized")


def __main__():
    functionlist = [state, federal,]
    optionlist = ["Run State", "Run Federal"]
    mainmenu = MenuGenerator("Main Menu", optionlist, functionlist)
    mainmenu.display()

__main__()