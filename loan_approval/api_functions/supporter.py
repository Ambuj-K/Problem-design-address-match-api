# system imports followed by custom imports
import datetime, math, string, pylev
import configparser
from collections import Counter
from polyleven import levenshtein

from .reject_status import *

reject_flag = False
reject_log = ""

#  rejectstatus class object
rejectc = RejectStatusCodeGenerator()


# support api functions

def matching(address1, address2):
    # upper case and remove spaces to calculate minimum word level
    # transformations required
    # check 80 percent match

    origLen2 = len(address2)
    # print(address1)
    # print(address2)
    # aaddress1 = address1.upper().translate(str.maketrans('', '',
    #                                                      string.whitespace))
    # aaddress2 = address2.upper().translate(str.maketrans('', '',
    #                                                      string.whitespace))
    # m = len(aaddress1)
    # n = len(aaddress2)
    #
    # # mnemonic table vs trie for fast diff
    # # can use pylev.lev library for the now uppercase two words
    # table = [[0] * (n + 1) for _ in range(m + 1)]
    #
    # for i in range(m + 1):
    #     table[i][0] = i
    # for j in range(n + 1):
    #     table[0][j] = j
    #
    # for i in range(1, m + 1):
    #     for j in range(1, n + 1):
    #         if aaddress1[i - 1] == aaddress2[j - 1]:
    #             table[i][j] = table[i - 1][j - 1]
    #         else:
    #             table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1],
    #                                   table[i - 1][j - 1])
    # print(m, n)
    # print(table[-1][-1])
    # print(int((origLen2 - table[-1][-1])/origLen2 * 100))
    # return (n - table[-1][-1])/n * 100

    # word level doesn't take care of minor misspellings in individual
    # so gives lower match score and does not take care of abbreviations
    # words
    # add1_arr = address1.split(" ")
    # add2_arr = address2.split(" ")
    # print(add1_arr)
    # print(add2_arr)
    # print(pylev.levenshtein(add1_arr, add2_arr))
    # print(int((len(add2_arr) - pylev.levenshtein(add1_arr, add2_arr)) / len(
    #     add2_arr)*100))
    # return int((len(add2_arr)-pylev.levenshtein(add1_arr, add2_arr))/len(
    #     add2_arr)*100)

    # percentage match = (
    # (bureau_address_len-difference_score)/bureau_address_len *100)
    # return int((origLen2 - table[-1][-1]) / origLen2 * 100)

    add1_freq_dict = Counter(address1.strip().upper().split(" "))
    add2_freq_dict = Counter(address2.strip().upper().split(" "))
    # print(add1_freq_dict)
    # print(add2_freq_dict)

    for key in add1_freq_dict.keys():
        if key in add2_freq_dict.keys():
            add1_freq_dict[key] -= 1
            add2_freq_dict[key] -= 1
    print(add1_freq_dict)
    print(add2_freq_dict)

    str1 = "".join(i * add1_freq_dict[i] for i in
                   add1_freq_dict.keys() if add1_freq_dict[i] > 0)
    str2 = "".join(i * add2_freq_dict[i] for i in
                   add2_freq_dict.keys() if add2_freq_dict[i] > 0)
    # print(str1)
    # print(str2)

    m = len(str1)
    n = len(str2)

    # can use pylev.lev library for the now uppercase two words
    table = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        table[i][0] = i
    for j in range(n + 1):
        table[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1],
                                      table[i - 1][j - 1])

        # if not the actual full matching score required
        # if int((origLen2 - table[i][j]) / origLen2 * 100) < 80:
        #     return 79

    # Polyleven with threshold
    # min_change = levenshtein(str1,str2)
    # return int((origLen2 - min_change) / origLen2 * 100)
    # heuristics to check if the two words are of what difference
    # percentage match = (
    # (bureau_address_len-difference_score)/bureau_address_len *100)
    return int((origLen2 - table[-1][-1]) / origLen2 * 100)


# calculating age
def age_string_calculator(dob):
    dob = datetime.datetime.strptime(dob, '%d/%m/%Y')
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob
                                                               .day))
    return age


# calculating line assignment and reject flag change
def calculate_line_assign(existingemi, allowedfoir, income, loantenure):
    global reject_flag, reject_log
    headroom = income * allowedfoir - existingemi
    loanamount = int(math.floor((headroom * loantenure) / 100)) * 100
    if 10000 > loanamount:
        reject_flag = True
        reject_log = rejectc.loanamount_error()
    elif 500000 < loanamount:
        loanamount = 500000
    return loanamount


def calculate_loan_prerequisites(age, income, bureauscore, applicationscore,
                                 maxDelL12M, address_matching_score):
    global reject_flag, reject_log
    config = configparser.ConfigParser()
    config.read("../config_reject_parameters_limit.ini")
    age_min = config["Age"]["min"]
    age_max = config["Age"]["max"]
    income_min = config["Income"]["min"]
    bureauscore_min = config["BureauScore"]["min"]
    applicationscore_min = config["ApplicationScore"]["min"]
    MaxDelL12M = config["MaxDelL12M"]["max"]
    min_address_match_percent = config["address_matching_score"]["min"]

    if not int(age_min) <= age <= int(age_max):
        reject_flag = True
        reject_log = rejectc.age_error()
    elif not income > int(income_min):
        reject_flag = True
        reject_log = rejectc.income_error()
    elif not bureauscore >= int(bureauscore_min):
        reject_flag = True
        reject_log = rejectc.bureauscore_error()
    elif not applicationscore >= int(applicationscore_min):
        reject_flag = True
        reject_log = rejectc.applicationscore_error()
    elif not maxDelL12M <= int(MaxDelL12M):
        reject_flag = True
        reject_log = rejectc.maxdelim_error()
    elif not address_matching_score > int(min_address_match_percent):
        reject_flag = True
        reject_log = rejectc.addressmatchingscore_error()

    return [reject_flag, reject_log]

# print(levenshtein("mom watch", "watch momma"))