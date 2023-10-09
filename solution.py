"""
CITS1401 Project 2
Full Name: Tong LAN
Student ID: 24056082
"""


def read_file(csvfile: str) -> list:
    try:
        with open(csvfile, 'r') as f:
            data = f.readlines()
            return data
    except IOError:
        print("Cannot open file:[%s]" % csvfile)
        return None


def save_file_data(read_data: list) -> list:
    data_list = []
    # get csv header
    header = read_data[0].lower().strip().split(',')
    # save to a dictionary list
    organisation_id_set = set()
    organisation_duplicate_id_set = set()
    for i in range(1, len(read_data)):
        line = read_data[i].lower().strip()
        # empty line
        if len(line) == 0:
            continue
        data = line.split(',')
        # save to a dictionary
        data_dict = dict(zip(header, data))
        # get organisation id
        organisation_id = data_dict['organisation id']
        if organisation_id not in organisation_id_set:
            organisation_id_set.add(organisation_id)
        elif organisation_id not in organisation_duplicate_id_set:
            organisation_duplicate_id_set.add(organisation_id)
        # ignore invalid data
        if invalid_data(data_dict):
            continue
        # add valid data
        data_list.append(data_dict)
    # omit duplicate organisation id datas
    if len(organisation_duplicate_id_set) > 0:
        print("Duplicate organisation id:{}".format(organisation_duplicate_id_set))
        data_list = [x for x in data_list if x['organisation id'] not in organisation_duplicate_id_set]
    return data_list


def invalid_data(data_dict: dict) -> bool:
    # check country
    if 'country' not in data_dict.keys() or len(data_dict['country']) == 0:
        print("Invalid country, data:{}".format(data_dict))
        return True
    # check category
    if 'category' not in data_dict.keys() or len(data_dict['category']) == 0:
        print("Invalid category, data:{}".format(data_dict))
        return True
    # check organisation id, alphanumeric only
    if ('organisation id' not in data_dict.keys()
            or len(data_dict['organisation id']) == 0
            or not data_dict['organisation id'].isalnum()):
        print("Invalid organisation id, data:{}".format(data_dict))
        return True
    # check number of employees, numeric only
    if ('number of employees' not in data_dict.keys()
            or len(data_dict['number of employees']) == 0
            or not data_dict['number of employees'].isnumeric()):
        print("Invalid number of employees, data:{}".format(data_dict))
        return True
    # check median salary, numeric only
    if ('median salary' not in data_dict.keys()
            or len(data_dict['median salary']) == 0
            or not data_dict['median salary'].isnumeric()):
        print("Invalid median salary, data:{}".format(data_dict))
        return True
    # check profits in 2020(million), numeric only
    if ('profits in 2020(million)' not in data_dict.keys()
            or len(data_dict['profits in 2020(million)']) == 0
            or not data_dict['profits in 2020(million)'].isnumeric()):
        print("Invalid profits in 2020(million), data:{}".format(data_dict))
        return True
    # check profits in 2021(million), numeric only
    if ('profits in 2021(million)' not in data_dict.keys()
            or len(data_dict['profits in 2021(million)']) == 0
            or not data_dict['profits in 2021(million)'].isnumeric()):
        print("Invalid profits in 2021(million), data:{}".format(data_dict))
        return True
    return False


def save_data_in_dict(data_list: list, key_name: str) -> dict:
    data_dict = {}
    for data in data_list:
        # extract key value
        key = data[key_name]
        if key not in data_dict:
            # if key not exists, create a new value list
            data_dict[key] = [data]
        else:
            # if key exists, append to the value list
            value_data_list = data_dict[key]
            value_data_list.append(data)
            data_dict[key] = value_data_list
    return data_dict


def t_test_score_minkowski_distance(data_dict: dict) -> dict:
    country_dict = {}
    for country, country_data_list in data_dict.items():
        # calculate t_test score
        t_test_score = cal_t_test_score(country_data_list)
        # calculate Minkowski distance
        minkowski_distance = cal_minkowski_distance(country_data_list, 3)
        country_dict[country] = [t_test_score, minkowski_distance]
    return country_dict


def cal_t_test_score(data_list: list) -> float:
    # get profits list
    profit_2020_list = [int(x['profits in 2020(million)']) for x in data_list]
    profit_2021_list = [int(x['profits in 2021(million)']) for x in data_list]
    # sample size
    number_of_employees_size = len(profit_2020_list)
    if number_of_employees_size == 0:
        print("number_of_employees is 0, can not calculate t_test score")
        return 0
    median_salary_size = len(profit_2021_list)
    if median_salary_size == 0:
        print("median_salary is 0, can not calculate t_test score")
        return 0
    # sample mean
    number_of_employees_mean = sum(profit_2020_list) / number_of_employees_size
    median_salary_mean = sum(profit_2021_list) / median_salary_size
    # sample standard deviation
    number_of_employees_sd = calculate_sd(profit_2020_list)
    median_salary_sd = calculate_sd(profit_2021_list)
    # calculate t-test score
    molecule = number_of_employees_mean - median_salary_mean
    denominator = (
                          number_of_employees_sd ** 2 / number_of_employees_size + median_salary_sd ** 2 / median_salary_size) ** 0.5
    return round(molecule / denominator, 4) if denominator != 0 else 0


def calculate_sd(data_list: list) -> float:
    # check input size
    if len(data_list) <= 1:
        return 0
    # calculate length
    length = len(data_list)
    # calculate mean
    mean = sum(data_list) / length
    # calculate standard deviation
    diff_sq_sum = sum([(x - mean) ** 2 for x in data_list])
    return (diff_sq_sum / (length - 1)) ** 0.5


def cal_minkowski_distance(data_list: list, similarity: int) -> float:
    if similarity == 0:
        print("similarity is 0, can not calculate Minkowski distance")
        return 0
    # get number of employees list and median salary list
    number_of_employees_list = [int(x['number of employees']) for x in data_list]
    median_salary_list = [int(x['median salary']) for x in data_list]
    # calculate Minkowski distance
    distance_list = []
    for i in range(len(number_of_employees_list)):
        distance_list.append((abs(number_of_employees_list[i] - median_salary_list[i])) ** similarity)
    return round(sum(distance_list) ** (1 / similarity), 4)


def category_dictionary(data_dict: dict) -> dict:
    category_dict = {}
    for category, category_data_list in data_dict.items():
        # rank of organisation
        organisation_rank_dict = cal_rank_of_organisation(category_data_list)
        # get organisation data in the category
        organisation_dict = save_data_in_dict(category_data_list, "organisation id")
        for organisation_id, organisation_data_list in organisation_dict.items():
            # get organisation data, if there are multiple data, use the first one
            organisation_data = organisation_data_list[0]
            number_of_employees = int(organisation_data['number of employees'])
            profit_in_2020 = int(organisation_data['profits in 2020(million)'])
            absolute_profit_change = organisation_data['absolute_profit_change']
            profit_percent_change = round(cal_absolute_profit_change(absolute_profit_change, profit_in_2020), 4)
            rank_of_organisation = organisation_rank_dict[organisation_id]
            # save data to the organisation dictionary
            organisation_dict[organisation_id] = [number_of_employees, profit_percent_change, rank_of_organisation]
        # save data to the category dictionary
        category_dict[category] = organisation_dict
    return category_dict


def cal_rank_of_organisation(category_data_list: list) -> dict:
    # add profits_change to the data for sorting
    for data in category_data_list:
        data['absolute_profit_change'] = abs(
            int(data['profits in 2020(million)']) - int(data['profits in 2021(million)']))
    # sort by number of employees desc and then profits_change desc
    rank_list = sorted(category_data_list, key=lambda x: (-int(x['number of employees']), -x['absolute_profit_change']))
    # create the rank dictionary, rank starts from 1
    rank_dict = {}
    for i in range(len(rank_list)):
        rank_dict[rank_list[i]['organisation id']] = i + 1
    return rank_dict


def cal_absolute_profit_change(absolute_profit_change: float, profit_2020: int) -> float:
    return (absolute_profit_change / profit_2020) * 100


def main(csvfile):
    # check input params
    if len(csvfile) == 0:
        print("Please input the valid params")
        return {}, {}
    # read file
    read_data = read_file(csvfile)
    if read_data is None or len(read_data) == 0:
        print("Input file:[] is empty or not exists".format(csvfile))
        return {}, {}
    # store data to a list and filter by country
    data_list = save_file_data(read_data)
    if len(data_list) == 0:
        print("Input file:[] contains no data".format(csvfile))
        return {}, {}
    # store data in a dictionary with country as key
    data_dict = save_data_in_dict(data_list, "country")
    # t_test score and Minkowski distance in each country
    country_dict = t_test_score_minkowski_distance(data_dict)
    # store data in a dictionary with category as key
    data_dict = save_data_in_dict(data_list, "category")
    # nested dictionary with category as key and organisation id as key
    category_dict = category_dictionary(data_dict)
    return country_dict, category_dict
