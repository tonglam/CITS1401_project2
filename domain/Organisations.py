class Organisations:

    def __init__(self, organisation_id, name, website, country, founded, category, number_of_employees, median_salary,
                 profits_in_2020_million, profits_in_2021_million):
        self.organisation_id = organisation_id
        self.name = name
        self.website = website
        self.country = country
        self.founded = founded
        self.category = category
        self.number_of_employees = number_of_employees
        self.median_salary = median_salary
        self.profits_in_2020_million = profits_in_2020_million
        self.profits_in_2021_million = profits_in_2021_million

    def __str__(self):
        return_list = [
            self.organisation_id,
            self.name,
            self.website,
            self.country,
            self.founded,
            self.category,
            self.number_of_employees,
            self.median_salary,
            self.profits_in_2020_million,
            self.profits_in_2021_million
        ]
        return ",".join([str(x) for x in return_list]) + "\n"

    def get_organisation_id(self):
        return self.organisation_id

    def set_organisation_id(self, organisation_id):
        self.organisation_id = organisation_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_website(self):
        return self.website

    def set_website(self, website):
        self.website = website

    def get_country(self):
        return self.country

    def set_country(self, country):
        self.country = country

    def get_founded(self):
        return self.founded

    def set_founded(self, founded):
        self.founded = founded

    def get_category(self):
        return self.category

    def set_category(self, category):
        self.category = category

    def get_number_of_employees(self):
        return self.number_of_employees

    def set_number_of_employees(self, number_of_employees):
        self.number_of_employees = number_of_employees

    def get_median_salary(self):
        return self.median_salary

    def set_median_salary(self, median_salary):
        self.median_salary = median_salary

    def get_profits_in_2020_million(self):
        return self.profits_in_2020_million

    def set_profits_in_2020_million(self, profits_in_2020_million):
        self.profits_in_2020_million = profits_in_2020_million

    def get_profits_in_2021_million(self):
        return self.profits_in_2021_million

    def set_profits_in_2021_million(self, profits_in_2021_million):
        self.profits_in_2021_million = profits_in_2021_million
