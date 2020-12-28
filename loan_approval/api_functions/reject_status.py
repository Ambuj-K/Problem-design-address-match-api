import configparser


class RejectStatusCodeGenerator:
    # config file to read reject code dynamically
    # dict holding all reject codes from config
    config = configparser.ConfigParser()
    config.read("../config_reject_codes.ini")
    reject_status_dict = {"Age LT 21 or GT 55": config["Default"]["age_code"],
                          "Income LT 20000": config["Default"]["income"],
                          "BureauScore LT 600": config["Default"]["beureauscore"],
                          "ApplicationScore LT 600": config["Default"]["applicationscore"],
                          "MaxDelL12M GT 30": config["Default"]["maxdel"],
                          "AddressMatchingScore LT 80": config["Default"]["address"],
                          "Loanamount LT 10000": config["Default"]["loanamt"]}

    # functions for individual case exceptions reject
    def age_error(self):
        return self.reject_status_dict["Age LT 21 or GT 55"] + " " \
               + "Age LT 21 or GT 55"

    def income_error(self):
        return self.reject_status_dict["Income LT 20000"] + " " \
               + "Income LT 20000"

    def bureauscore_error(self):
        return self.reject_status_dict["BureauScore LT 600"] + " " \
               + "BureauScore LT 600"

    def applicationscore_error(self):
        return self.reject_status_dict["ApplicationScore LT 600"] + " " \
               + "ApplicationScore LT 600"

    def maxdelim_error(self):
        return self.reject_status_dict["MaxDelL12M GT 30"] + " " \
               + "MaxDelL12M GT 30"

    def addressmatchingscore_error(self):
        return self.reject_status_dict["AddressMatchingScore LT 80"] + " " \
               + "AddressMatchingScore LT 80"

    def loanamount_error(self):
        return self.reject_status_dict["Loanamount LT 10000"] + " " \
               + "Loanamount LT 10000"
