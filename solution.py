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
    for i in range(1, len(read_data)):
        line = read_data[i].lower().strip()
        if invalid_data(line):
            continue
        data = line.split(',')
        # save to a dictionary
        data_dict = dict(zip(header, data))
        data_list.append(data_dict)
    return data_list


def invalid_data(line: str) -> bool:
    if len(line) == 0:
        return True
    # todo more invalid rules


def t_test_score_minkowski_distance(data_list: list) -> dict:
    return_dict = {}
    country_list = [x['country'] for x in data_list]
    country_list = list(set(country_list))
    for country in country_list:
        # calculate t_test score
        profit_2020_list = [int(y['profits in 2020(million)']) for y in data_list if y['country'] == country]
        profit_2021_list = [int(y['profits in 2021(million)']) for y in data_list if y['country'] == country]
        t_test_score = cal_t_test_score(profit_2020_list, profit_2021_list)
        # calculate Minkowski distance
        number_of_employees_list = [int(y['number of employees']) for y in data_list if y['country'] == country]
        median_salary_list = [int(y['median salary']) for y in data_list if y['country'] == country]
        minkowski_distance = cal_minkowski_distance(number_of_employees_list, median_salary_list)
        return_dict[country] = [t_test_score, minkowski_distance]
    return return_dict


def cal_t_test_score(profit_2020_list: list, profit_2021_list: list) -> float:
    number_of_employees_size = len(profit_2020_list)
    median_salary_size = len(profit_2021_list)
    number_of_employees_mean = sum(profit_2020_list) / number_of_employees_size
    median_salary_mean = sum(profit_2021_list) / median_salary_size
    number_of_employees_sd = calculate_sd(profit_2020_list)
    median_salary_sd = calculate_sd(profit_2021_list)
    molecule = number_of_employees_mean - median_salary_mean
    denominator = (
                          number_of_employees_sd ** 2 / number_of_employees_size + median_salary_sd ** 2 / median_salary_size) ** 0.5
    return round(molecule / denominator, 4) if denominator != 0 else 0


def calculate_sd(data_list: list) -> float:
    # calculate length
    length = len(data_list)
    # calculate mean
    mean = sum(data_list) / length
    # calculate standard deviation
    diff_sq_sum = sum([(x - mean) ** 2 for x in data_list])
    return (diff_sq_sum / (length - 1)) ** 0.5


def cal_minkowski_distance(number_of_employees_list: list, median_salary_list: list) -> float:
    distance_list = []
    for i in range(len(number_of_employees_list)):
        distance_list.append((abs(number_of_employees_list[i] - median_salary_list[i])) ** 3)
    return round(sum(distance_list) ** (1 / 3), 4)


def create_category_dictionary(data_list: list) -> dict:
    category_dict = {}
    category_list = [x['category'] for x in data_list]
    category_list = list(set(category_list))
    for category in category_list:
        organisation_dict = {}
        organisation_list = [x['organisation id'] for x in data_list if x['category'] == category]
        organisation_data_list = [x for x in data_list if
                                  x['organisation id'] in organisation_list and x['category'] == category]
        organisation_rank_dict = cal_rank_of_organisation(organisation_data_list)
        for organisation_data in organisation_data_list:
            organisation_id = organisation_data['organisation id']
            number_of_employees = int(organisation_data['number of employees'])
            absolute_profit_change = cal_absolute_profit_change(organisation_data)
            rank_of_organisation = organisation_rank_dict[organisation_id]
            organisation_dict[organisation_id] = [number_of_employees, absolute_profit_change, rank_of_organisation]
        category_dict[category] = organisation_dict
    return category_dict


def cal_rank_of_organisation(organisation_list: list) -> dict:
    rank_list = sorted(organisation_list, key=lambda x: (-int(x['number of employees']), x['name']))
    rank_dict = {}
    for i in range(len(rank_list)):
        rank_dict[rank_list[i]['organisation id']] = i + 1
    return rank_dict


def cal_absolute_profit_change(data: dict) -> float:
    profit_2020 = int(data['profits in 2020(million)'])
    profit_2021 = int(data['profits in 2021(million)'])
    return round((abs(profit_2021 - profit_2020) / profit_2020) * 100, 4)


def main(csvfile):
    # check input params
    if len(csvfile) == 0:
        print("Please input the valid params")
        return {}, {}
    # read file
    read_data = read_file(csvfile)
    if read_data is None or len(read_data) == 0:
        print("Input file:[] is empty or not exists" % csvfile)
        return {}, {}
    # store data to a list and filter by country
    data_list = save_file_data(read_data)
    if len(data_list) == 0:
        print("Input file:[] contains no data" % csvfile)
        return {}, {}
    # t_test score and Minkowski distance
    country_dict = t_test_score_minkowski_distance(data_list)
    # create category dictionary
    category_dict = create_category_dictionary(data_list)
    return country_dict, category_dict


if __name__ == '__main__':
    csvfile = './Organisations.csv'
    output1, output2 = main(csvfile)
    print(output1['brazil'])
    print(output2['biotechnology'])
    print(output1['afghanistan'])
    print(output2['accounting'])
