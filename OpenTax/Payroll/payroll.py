import pandas as pd


def payrolltester():

    return


def addemployee():
    fullframe = pd.read_csv("Data/Records/Employees.csv")
    headers = fullframe.head()
    colcount = len(headers)
    newemployeedata = [None]*colcount
    index = 0
    back = "EIN"
    for i in headers:
        print("Input data for,", i, "\n")
        inputdata = input(": ")

        if inputdata.upper() == "BACK":
            print("Input data for,", back, "\n")
            inputdata = input(": ")
            newemployeedata[index-1] = inputdata

            print("Input data for,", i, "\n")
            inputdata = input(": ")

        newemployeedata[index] = inputdata
        index += 1
        back = i
    fullframe.loc[len(fullframe.index())] = newemployeedata
    fullframe.to_csv("Data/Records/Employees.csv")
    print("added employee")

    return


def changeemployeedata():

    return


def removeemployee():

    return


def employeehandler():
    functionlist = [addemployee, changeemployeedata]
    menuoptions = ["Add New Employee", "Change Employee Data"]
    emenu = MenuGenerator("Employee Handler", menuoptions, functionlist)
    emenu.display()

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
            if crsr.upper() == 'Q' or crsr.upper() == "QUIT":
                quit()
            if int(crsr) in range(0, len(self.options)):
                self.functionlist[int(crsr)]()
            else:
                print("Input Not Recognized")

