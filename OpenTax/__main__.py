from Federal.Federal_Income_Tax import testfunction
from State.State_Income_Tax import statetester
from Payroll.payroll import payrolltester, employeehandler
from Payroll.payroll import MenuGenerator


def __main__():
    functionlist = [testfunction, statetester, payrolltester, employeehandler]
    optionlist = ["Run Federal", "Run State", "Run Payroll", "Run Employee Handler"]
    mainmenu = MenuGenerator("Main Menu", optionlist, functionlist)
    mainmenu.display()

__main__()