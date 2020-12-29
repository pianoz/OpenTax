import re

# w2params are as follows for a NEW W2, [Taxable Pay(0), tax status 0-2(1), line 4a(2), checked box T/F(3),
# line4b(4), step 3(5), additional w/h (6)]
# OLD w2 is as follows: [Taxable Pay (0), tax status 0-2(1), # of allowances (2),-,-,-, additional w/h (6)]
# Tax status can be as follows: Single/married filing separate (0), married jointly (1), HoH (2).

payfreq = {
    "Semiannually": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Semimonthly": 24,
    "Biweekly": 26,
    "Weekly": 52,
    "Daily": 260
}

marriedjointNOCheck = [
    [0, 11900, 0, 0, 0],
    [11900, 31650, 0, 10, 11900],
    [31650, 92150, 1975, 12, 31650],
    [92150, 182950, 9235, 22, 92150],
    [182950, 338500, 29211, 24, 182950],
    [338500, 426600, 66543, 32, 338500],
    [426600, 633950, 94735, 35, 426600],
    [633950, 9999999999, 167307.50, 37, 633950]
]
singlesepNOcheck = [
    [0, 3800, 0.00, 0, 0],
    [3800, 13675, 0.00, 10, 3800],
    [13675, 43925, 987.50, 12, 13675],
    [43925, 89325, 4617.50, 22, 43925],
    [89325, 167100, 14605.50, 24, 89325],
    [167100, 211150, 33271.50, 32, 167100],
    [211150, 522200, 47367.50, 35, 211150],
    [522200, 9999999999, 156235.00, 37, 522200]
]
HeadofhouseholdNOcheck = [
    [0, 10050, 0.00, 0, 0],
    [10050, 24150, 0.00, 10, 10050],
    [24150, 63750, 1410.00, 12, 24150],
    [63750, 95550, 6162.00, 22, 63750],
    [95550, 173350, 13158.00, 24, 95550],
    [173350, 217400, 31830.00, 32, 173350],
    [217400, 528450, 45926.00, 35, 217400],
    [528450, 9999999999, 154793.50, 37, 528450]
]
marriedjointcheck = [
    [0, 12400, 0.00, 0, 0],
    [12400, 22275, 0.00, 10, 12400],
    [22275, 52525, 987.50, 12, 22275],
    [52525, 97925, 4617.50, 22, 52525],
    [97925, 175700, 14605.50, 24, 97925],
    [175700, 219750, 33271.50, 32, 175700],
    [219750, 323425, 47367.50, 35, 219750],
    [323425, 9999999999, 83653.75, 37, 323425]
]
singlesepcheck = [
    [0, 6200, 0.00, 0, 0],
    [6200, 11138, 0.00, 10, 6200],
    [11138, 26263, 493.75, 12, 11138],
    [26263, 48963, 2308.75, 22, 26263],
    [48963, 87850, 7302.75, 24, 48963],
    [87850, 109875, 16635.75, 32, 87850],
    [109875, 265400, 23683.75, 35, 109875],
    [265400, 9999999999, 78117.50, 37, 265400]
]
Headofhouseholdcheck = [
    [0, 9325, 0.00, 0, 0],
    [9325, 16375, 0.00, 10, 9325],
    [16375, 36175, 705.00, 12, 16375],
    [36175, 52075, 3081.00, 22, 36175],
    [52075, 90975, 6579.00, 24, 52075],
    [90975, 113000, 15915.00, 32, 90975],
    [113000, 268525, 22963.00, 35, 113000],
    [268525, 9999999999, 77396.75, 37, 268525]
]


# All pay is biweekly at MFG


def federaloutsidehandler(newtrigger, w2params):
    tupleout = [0.0, 0.0, 0.0]
    tupleout[0] = float(federalwithholding(newtrigger, w2params))
    tupleout[1] = float(FICA_SS(w2params[0]))
    tupleout[2] = float(FICA_MC(w2params[0]))
    return tupleout


def adjustedannualwageamountnew(w2params):
    one_c = w2params[0] * payfreq["Biweekly"]
    one_d = one_c + w2params[2]
    # See if box is checked, if so, check their fed tax status
    # Step 1 on tax form, if they don't check the box and are married, 12900, if not married, 8600, if not checked, zero
    one_g = 0
    if not w2params[3]:
        if w2params[1] == 1:
            one_g = 12900
        else:
            one_g = 8600
    aawa = 0
    if one_c - (w2params[4] + one_g) > 0:
        aawa = one_c - (w2params[4] + one_g)
    return aawa


def adjustedannualwageamountold(w2params):
    one_c = w2params[0] * payfreq["Biweekly"]
    aawa = max(one_c - w2params[2] * 4300, 0)
    return aawa


def federalwithholding(neww2trigger, w2params):

    adjustedawa = adjustedannualwageamountold(w2params)
    if neww2trigger:
        adjustedawa = adjustedannualwageamountnew(w2params)

    tablevals = [0, 0, 0]
    # Remember, in w2params 2, 0 means single or married filing separately, 1 = married joint, 2= HoH
    if w2params[3]:
        if w2params[1] == 0:
            tablevals = lookup(adjustedawa, singlesepcheck)
        elif w2params[1] == 1:
            tablevals = lookup(adjustedawa, marriedjointcheck)
        elif w2params[1] == 2:
            tablevals = lookup(adjustedawa, Headofhouseholdcheck)
    if not w2params[3]:
        if w2params[1] == 0:
            tablevals = lookup(adjustedawa, singlesepNOcheck)
        elif w2params[1] == 1:
            tablevals = lookup(adjustedawa, marriedjointNOCheck)
        elif w2params[1] == 2:
            tablevals = lookup(adjustedawa, HeadofhouseholdNOcheck)

    two_h = (((adjustedawa - tablevals[0]) * (tablevals[2] * .01)) + tablevals[1]) / payfreq["Biweekly"]
    three_c = 0
    if two_h - w2params[5] / payfreq["Biweekly"] > 0:
        three_c = two_h - w2params[5] / payfreq["Biweekly"]

    finalwihholding = three_c + w2params[6]

    return round(finalwihholding)


def lookup(wage, paytable):
    for i in paytable:
        if i[0] <= wage < i[1]:
            paytabletuple = [i[0], i[2], i[3]]
            return paytabletuple
    return ValueError


def FICA_SS(wage):
    # Social Security is 6.2% of taxable pay
    return round((wage * .062), 2)


def FICA_MC(wage):
    # Medicare is 1.45% of taxable pay
    return round((wage * .0145), 2)


def testfunction():
    neww2re = re.compile('new', flags=re.IGNORECASE)
    headofre = re.compile('head', flags=re.IGNORECASE)
    marriedre = re.compile("married", flags=re.IGNORECASE)
    higherre = re.compile("higher", flags=re.IGNORECASE)
    truefalsere = re.compile("true", flags=re.IGNORECASE)

    trigger = False
    testtuple = [0, 0, 0, 0, 0, 0, 0, 0]
    print(("--------------------------------------------------------------------\n"
           "                  Federal Withholding tester                        \n"
           "--------------------------------------------------------------------\n"))
    while 1:
        crsr = input("\n"  "Is this a new (post-2020) W4 or an old one? " "\n")

        if neww2re.match(crsr):
            trigger = True

            while 1:
                testtuple[0] = float(input("\n" "Taxable Wage" "\n").replace(',', '').replace('$', ''))
                fedtaxstatus = input("\n" "Federal Tax Status (single/married)" "\n")
                # testtuple[1] is initialized as zero or single
                if headofre.match(fedtaxstatus):
                    testtuple[1] = 2
                if not higherre.match(fedtaxstatus) and marriedre.match(fedtaxstatus):
                    testtuple[1] = 1

                testtuple[2] = float(input("\n" "Amount on line 4a" "\n").replace(',', '').replace('$', ''))
                boxcheck = input("\n" "Checked box True/False" "\n")
                testtuple[3] = False
                if truefalsere.match(boxcheck):
                    testtuple[3] = True
                testtuple[4] = float(input("\n" "Amount on line 4b" "\n").replace(',', '').replace('$', ''))
                testtuple[5] = float(input("\n" "Amount on step 3" "\n").replace(',', '').replace('$', ''))
                testtuple[6] = float(
                    input("\n" "Additional amount of withholding" "\n").replace(',', '').replace('$', ''))

                fict = federalwithholding(trigger, testtuple)
                ficass = FICA_SS(testtuple[0])
                ficamc = FICA_MC(testtuple[0])

                print("Federal Income Tax Withholding: $%.2f" % fict, "\n"
                      "Social Security Withholding: $%.2f" % ficass, "\n"
                      "Medicare Withholding: $%.2f" % ficamc, "\n"
                      "Pay after federal deductions: $%.2f" % (testtuple[0] - (fict + ficass + ficamc)))
                return

        elif not trigger:
            while 1:
                testtuple[0] = float(input("\n" "Taxable Wage (for pay period)" "\n").replace(',', '').replace('$', ''))
                fedtaxstatus = input("\n" "Federal Tax Status (married/single)" "\n")
                # testtuple[1] is initialized as zero or single
                if headofre.match(fedtaxstatus):
                    testtuple[1] = 2
                if not higherre.match(fedtaxstatus) and marriedre.match(fedtaxstatus):
                    testtuple[1] = 1

                testtuple[2] = int(input("\n" "Number of allowances" "\n").replace(',', '').replace('$', ''))

                testtuple[6] = float(
                    input("\n" "Additional amount of withholding" "\n").replace(',', '').replace('$', ''))

                fict = round(federalwithholding(trigger, testtuple), 2)
                ficass = round(FICA_SS(testtuple[0]), 2)
                ficamc = round(FICA_MC(testtuple[0]), 2)

                print("Federal Income Tax Withholding: %.2fUSD" % fict, "\n"
                      "Social Security Withholding: %.2fUSD" % ficass, "\n"
                      "Medicare Withholding: %.2fUSD" % ficamc, "\n"
                      "Pay after federal deductions: %.2fUSD" % (testtuple[0]-(fict+ficass+ficamc)))
                return