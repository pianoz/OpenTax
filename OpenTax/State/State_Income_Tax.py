import re
import pandas
import os

# w4 tuple is [taxable pay, single, dependents, extra]


payfreq = {
    "Semiannually": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Semimonthly": 24,
    "Biweekly": 26,
    "Weekly": 52,
    "Daily": 260
}

# 2d array where 1 = Mar Jo, 2 = single/HoH, 3 = Mar sep, 4 = dependant allowance
gastddeduc = [230.75, 177.00, 115.50]

gapaykeyfreq = {
    "Weekly": 0,
    "Biweekly": 1,
    "Semimonthly": 2,
    "Monthly": 3,
    "Quarterly": 4,
    "Semiannually": 5,
    "Daily": 7
}

okwithholdingallowance = {
    "Weekly": 19.23,
    "Biweekly": 38.46,
    "Semimonthly": 41.67,
    "Monthly": 83.33,
    "Quarterly": 250,
    "Semiannually": 500,
    "Annual": 1000,
    "Daily": 3.85
}

okmarried = [
    [0, 488, 0, 0],
    [488, 565, 0, .005],
    [565, 681, .38, .01],
    [681, 777, 1.54, .02],
    [777, 865, 3.46, .03],
    [865, 958, 6.12, .04],
    [958, 9999999999, 9.81, .05]
]
oksingle = [
    [0, 244, 0, 0],
    [244, 283, 0, .005],
    [283, 340, .19, .01],
    [340, 388, .77, .02],
    [388, 433, 1.73, .03],
    [433, 521, 3.06, .04],
    [521, 999999999, 6.60, .05]
]


def statehandler(state, filingtuple):
    if state.upper() == "CO" or state.upper() =="COLORADO":
        return cowithholding(filingtuple)
    if state.upper() == "KY" or state.upper() =="KENTUCKY":
        return kywithholding(filingtuple)
    if state.upper() == "GA" or state.upper() =="GEORGIA":
        return gawithholding(filingtuple)
    if state.upper() == "OK" or state.upper() =="OKLAHOMA":
        return okwithholding(filingtuple)
    else:
        print("Input not recognized")
        return 0


def cowithholding(w4tuple):
    one_c = w4tuple[0] * payfreq["Biweekly"]
    two_a = 4000
    if not w4tuple[1]:
        two_a = 8000
    two_d = ((max((one_c - two_a), 0)) * 0.0463) / payfreq["Biweekly"]
    withholding = w4tuple[2] + two_d
    return round(withholding, 0)


def kywithholding(w4tuple):
    # 2020 standard deduction: 2650
    # 2020 KY rate is 5% of taxable income
    taxablewages = w4tuple[0] * payfreq["Biweekly"] - 2650
    grosstax = taxablewages * .05
    return round((grosstax / payfreq["Biweekly"]), 0)


def gawithholding(w4tuple):
    # if true, single
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    if w4tuple[1]:
        dir_path = os.path.join(dir_path + "\Resources","gasingle.csv")
        taxtable = pandas.read_csv(dir_path)
    if not w4tuple[1]:
        dir_path = os.path.join(dir_path + "\Resources", "gamarried.csv")
        taxtable = pandas.read_csv(dir_path)
    length = len(taxtable.index)
    for rindex, row in taxtable.iterrows():
        if row[0] <= w4tuple[0] < row[1]:
            gawh = row[w4tuple[2] + 2]
            return round(gawh, 2)
        if rindex == length - 1:
            if w4tuple[1]:
                gawh = row[w4tuple[2] + 2] + (w4tuple[0] - 1951) * 0.0575
            if not w4tuple[1]:
                gawh = row[w4tuple[2] + 2] + (w4tuple[0] - 1920) * 0.0575
    return round(gawh, 0)


def okwithholding(w4tuple):
    oktw = w4tuple[0] - okwithholdingallowance["Biweekly"] * w4tuple[2]
    if oktw < 0:
        oktw = 0
    if w4tuple[1]:
        for i in range(7):
            if oksingle[i][0] <= oktw < oksingle[i][1]:
                okwith = oksingle[i][2] + (oktw - oksingle[i][0]) * oksingle[i][3]
                return round(okwith, 0)

    if not w4tuple[1]:
        for i in range(7):
            if okmarried[i][0] <= oktw < okmarried[i][1]:
                okwith = okmarried[i][2] + (oktw - okmarried[i][0]) * okmarried[i][3]
                return round(okwith, 0)


def statetester():
    try:
        while True:
            print("\n"
                  "State Withholding tester"
                  "\n")
            while True:
                try:
                    state = str(input("What state? (currently supports: CO, KY, OK, GA)"))
                except ValueError:
                    print("Incorrect input, what state?")
                else:
                    break
            while True:
                try:
                    wage = float(input("\n" "Taxable Wage" "\n").replace(',', '').replace('$', ''))
                except ValueError:
                    print("Incorrect input, Taxable Wage?")
                else:
                    break
            taxstat = input("Single?").lower() in ['yes', 'y', 'yea', 'true', 'correct']
            while True:
                try:
                    depend = int(input("Number of dependants/allowances?"))
                except ValueError:
                    print("Incorrect input. Try again")
                else:
                    break
            taxtuple = [wage, taxstat, depend]
            print(statehandler(state, taxtuple))
    except KeyboardInterrupt:
        print("quitting")