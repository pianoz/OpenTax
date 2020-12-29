from Federal.Federal_Income_Tax import testfunction
from State.State_Income_Tax import statetester

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
            if int(crsr) in range(0,len(self.options)):
                self.functionlist[int(crsr)]()
            else:
                print("Input Not Recognized")



def __main__():
    functionlist = [testfunction, statetester]
    optionlist = ["Run Federal", "Run State"]
    mainmenu = MenuGenerator("Main Menu", optionlist, functionlist)
    mainmenu.display()

__main__()