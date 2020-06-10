import math
import sys

credit_type = None
mon_payment = None
principal = None
periods = None
interest = None
nom_int_rate = None

args = sys.argv

# we cannot have less then 4 args:
if len(args) <= 4:
    print("Incorrect parameters")
    sys.exit()

# parse the input params otherwise, make sure they are > 0
for i in range(1, len(args)):
    [argument, value] = args[i].split(sep="=")
    if argument == "--type":
        credit_type = value
    elif argument == "--payment":
        mon_payment = float(value)
        if mon_payment < 0:
            print("Incorrect parameters")
            sys.exit()
    elif argument == "--principal":
        principal = float(value)
        if principal < 0:
            print("Incorrect parameters")
            sys.exit()
    elif argument == "--periods":
        periods = int(value)
        if periods < 0:
            print("Incorrect parameters")
            sys.exit()
    elif argument == "--interest":
        interest = float(value)
        nom_int_rate = interest / (12 * 100)
    else:
        print("Incorrect parameters")

# The interest must always be provided:
if interest is None:
    print("Incorrect parameters")
    sys.exit()

# If params ok: process!
if credit_type == "annuity":

    if periods is None:
        periods = math.log(mon_payment / (mon_payment - nom_int_rate*principal),
                           1 + nom_int_rate)
        periods = math.ceil(periods)
        years = periods // 12
        months = periods - 12 * years
        if years == 0:
            print(f"You need {months} months to repay this credit!")
        else:
            print(f"You need {years} years and {months} months to repay this credit!")
        overpayment = int(mon_payment * periods - principal)
        print(f"Overpayment = {overpayment}")

    elif mon_payment is None:
        mon_payment = principal * (nom_int_rate * (1 + nom_int_rate) ** periods) / \
                          ((1 + nom_int_rate) ** periods - 1)
        print(f"Your annuity payment = {math.ceil(mon_payment)}!")
        overpayment = int(math.ceil(mon_payment) * periods - principal)
        print(f"\nOverpayment = {overpayment}")

    elif principal is None:
        principal = mon_payment / ((nom_int_rate * (1 + nom_int_rate) ** periods) /
                                   ((1 + nom_int_rate) ** periods - 1))
        print(f"Your credit principal = {math.floor(principal)}!")
        overpayment = int(mon_payment * periods - math.floor(principal))
        print(f"Overpayment = {overpayment}")

elif credit_type == "diff":
    # for differentiated payment must be computed thus:
    if mon_payment is not None \
       or (periods or principal or nom_int_rate) is None:
        print("Incorrect parameters")
        sys.exit()

    # compute differentiated payments, total and overpayment
    total = 0
    for i in range(1, periods + 1):
        diff_payment = (principal / periods) + nom_int_rate * \
                       (principal - (principal * (i - 1) / periods))
        print(f"Month {i}: paid out {math.ceil(diff_payment)}")
        total += math.ceil(diff_payment)

    overpayment = int(total - principal)
    print(f"\nOverpayment = {overpayment}")
else:
    print("Incorrect parameters")
