import sys
import random
import configparser
from functools import reduce
from sheets_api import api_call


def main(participants):
    config = configparser.ConfigParser()
    config.read('random_movie.ini')

    previous_selectee = config['random_movie']['previous_selectee']
    spreadsheet_range = f'{config["random_movie"]["spreadsheet_tab"]}!A:B'
    results = api_call(range=spreadsheet_range)

    if participants == "ALL":
        participants = reduce(lambda accum, val: 
                              accum + [val[1].strip()] if val[1].strip() not in accum and val[1].strip() != "Submitter"
                              else accum, results, [])

    print(participants)
    participants = list(filter(lambda x: x.upper() != previous_selectee.upper(), participants ))

    random_user = random.choice(participants)
    print(f"This week's movie was nominated by {random_user}")
    
    filtered_results = filter(lambda x: x[1].upper() == random_user.upper(), results)
    results = list(filtered_results)
    
    print(f"Your randomly selected movie is {random.choice(results)[0]}")

    config['random_movie']['previous_selectee'] = random_user
    with open('random_movie.ini','w') as configfile:
        config.write(configfile)
    
if __name__ == "__main__":
    user_list = sys.argv
    del user_list[0]

    if len(user_list) == 0:
        user_list = "ALL"
    else:
        user_list = list(map(lambda x: x.upper(), user_list))

    main(user_list)