import time
import calendar
import datetime
import numpy as np
import pandas as pd

######################## [ CUSTOM DATA FOLDER ] ########################
WORK_FOLDER = ""    # adjust path to sub folder containing data
########################################################################


KEY_CANCEL = "CANCEL"       # key word to end program
KEY_YES = "Y"               # key word for "Yes" when interacting with user
KEY_NO = "N"                # key word for "No" when interacting with user
CITY_DATA = {"chicago": "chicago.csv",
             "new york city": "new_york_city.csv",
             "washington": "washington.csv"}

def get_userinput_yesno(question, default_val=KEY_YES):
    """
    Asks user a simple yes/no question and returns the user input standardized as KEY_YES or KEY_NO

    Args:
        (str) question - Question user needs to answer with Yes or No
        (str) default_val - Default value to use in case user presses ENTER without input. If argument is not provided, default is KEY_YES.

    Returns:
        (boolean) get_userinput_yesno - User input (decision) in form of True (Yes) and False (No)
    """
    userinput = ""

    # Format yes/no text --> Default value = upper()
    if default_val == KEY_YES:
        yes_no = "({}/{})".format(KEY_YES, KEY_NO.lower())
    else:
        yes_no = "({}/{})".format(KEY_YES.lower(), KEY_NO)

    # get user input
    while userinput != KEY_YES and userinput != KEY_NO:
        userinput = input("{} {} ".format(question, yes_no))

        if len(userinput) == 0:
            userinput = default_val
        else:
            userinput = userinput.upper()

    if userinput == KEY_YES:
        get_userinput_yesno = True
    else:
        get_userinput_yesno = False
    return get_userinput_yesno


def get_filters():
    """
    Asks user to specify a city, month day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - number of the month (1-12) to analyze; 0 = ALL = no filter
        (int) weekday - number of the weekday (1 Mon - 7 Sun) to analyze; 0 = ALL = no filter
    """

    
    print("Hello! Let's explore some US bikshare data!")

    city_list = list (city.title() for city in CITY_DATA)
    city = ""
    month = -99
    weekday = -99

    # get city filter
    city_valid = False
    continue_loop = True
    while not city_valid and continue_loop:
        city_user = str(input("Please enter city {} for which you would like to analyze bike sharing data: ".format(city_list)))

        city_valid = city_user.lower() in CITY_DATA
        if city_valid:
            city = city_user.lower()
        else:
            print("ERROR: City '{}' was not found. Please check for typos. Valid options are: {}".format(city_user,city_list))
            continue_loop = get_userinput_yesno("Do you want to try again?")

    # get month filter
    month_valid = False
    while not month_valid and continue_loop:
        month_user = input("Filter a specific month? Enter a number (1 = Jan, ..., 12 = Dec)   -OR-   leave empty to skip: ")
        
        if month_user == "":    # blank = no filter = 0
            month_user = 0

        try:
            month = int(month_user)
            month_valid = month >= 0 and month <= 12
            if not month_valid: 
                print("ERROR: Incorrect value '{}'. Please enter a whole number from 1 to 12!".format(month_user))
                continue_loop = get_userinput_yesno("Do you want to try again?")

        except ValueError:
            print("ERROR: Incorrect value '{}'. Please enter a whole number from 1 to 12!".format(month_user))
            continue_loop = get_userinput_yesno("Do you want to try again?")

    # get weekday filter
    weekday_valid = False
    while not weekday_valid and continue_loop:
        weekday_user = input("Filter a specific week day? Enter a number (1 = Mon, ..., 7 = Sun)   -OR-   leave empty to skip: ")
        
        if weekday_user == "":    # blank = no filter = 0
            weekday_user = 0

        try:
            weekday = int(weekday_user)
            weekday_valid = weekday >= 0 and weekday <= 7
            if not weekday_valid: 
                print("ERROR: Incorrect value '{}'. Please enter a whole number from 1 (Monday) to 7 (Sunday)!".format(weekday_user))
                continue_loop = get_userinput_yesno("Do you want to try again?")

        except ValueError:
            print("ERROR: Incorrect value '{}'. Please enter a whole number from 1 (Monday) to 7 (Sunday)!".format(weekday_user))
            continue_loop = get_userinput_yesno("Do you want to try again?")

    
    # return values
    print('-'*40)
    if continue_loop:
        return city, month, weekday
    else:
        return KEY_CANCEL, month, weekday
    

def load_data(city, month, weekday):
    """
    Loads data for the specified city, and filters by month and weekday if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - number of the month (1-12) to filter by; 0 = no filter
        (int) weekday - number of the week day (0 Monday - 6 Sunday) to filter by; -1 = no filter

    Returns:
        (df) df - pandas DataFrame containing city data filtered by month an day
    """

    # load data into a dataframe
    df = pd.read_csv("./{}{}".format(WORK_FOLDER,CITY_DATA[city]))

    # add columns start_month, start_weekday
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["start_month"] = df["Start Time"].dt.month
    df["start_weekday"] = df["Start Time"].dt.day_of_week

    # apply filters
    if month > 0:
        df = df[df.start_month == month]
    
    if weekday >= 0:
        df = df[df.start_weekday == weekday]

    return df


def time_stats(df):
    """Displays statistics of the most frequent times of travel."""

    print("\nCALCULATING MOST FREQUENT TIMES OF TRAVEL FOR BIKE RENTALS...\n")
    start_time = time.time()

    # Display most common month
    most_common_start_months_int = df.start_month.mode()
    most_common_start_months_name = [calendar.month_name[month] for month in most_common_start_months_int]
    print("Most common month(s): {}".format(most_common_start_months_name))

    # Display the most common day of week
    most_common_start_weekday_int = df.start_weekday.mode()
    most_common_start_weekday_name = [calendar.day_name[weekday] for weekday in most_common_start_weekday_int]
    print("Most common weekday(s): {}".format(most_common_start_weekday_name))

    # Display the most common start hour
    most_common_start_hour_int = list(df["Start Time"].dt.hour.mode())
    print("Most common start hour(s): {}".format(most_common_start_hour_int))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCALCULATING THE MOST POPULAR STATIONS AND TRIP...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = list(df["Start Station"].mode())
    print("Most common Start Station(s): {}".format(most_common_start_station))

    # Display most commonly used end station
    most_common_end_station = list(df["End Station"].mode())
    print("Most common End Station: {}".format(most_common_end_station))

    # Display most frequent combination of start station and end station trip
    most_common_start_end_station_combi = list((df["Start Station"] + " --> " + df["End Station"]).mode())
    print("Most common Start - End station combination(s): {}".format(most_common_start_end_station_combi))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCALCULATING TRIP DURATIONS...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = str(datetime.timedelta(seconds=float(df["Trip Duration"].sum())))
    print("Total travel time: {}".format(total_travel_time))

    # Display mean travel time
    mean_travel_time = str(datetime.timedelta(seconds=float(df["Trip Duration"].mean())))
    print("Mean travel time: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCALCULATING USER STATS...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts per User Type:")
    try:
        counts_user_type = df["User Type"].value_counts()
        for index, val in counts_user_type.iteritems():
            print(" " * 4,"{}: {}".format(index, val))
    except KeyError:
        print(" " * 4, "User Type data assessment not possible for this data set. Column 'User Type' was not found.")

    # Display counts of gendera
    print("Counts per Gender:")
    try:
        counts_gender = df["Gender"].value_counts()
        for index, val in counts_gender.iteritems():
            print(" " * 4, "{}: {}".format(index, val))
        
    except KeyError:
        print(" " * 4, "Gender data assessment not possible for this data set. Column 'Gender' was not found.")

    # Display earliest, most recent, and most common year of birth
    print("Birth Year statistics:")

    try:
        min_birth_year = int(df["Birth Year"].min())
        print(" " * 4,"Earliest Birth Year: {}".format(min_birth_year))

        max_birth_year = int(df["Birth Year"].max())
        print(" " * 4,"Most recent Birth Year: {}".format(max_birth_year))

        most_common_birth_year = list(df["Birth Year"].mode())
        most_common_birth_year = [int(x) for x in most_common_birth_year]
        print(" " * 4,"Most common Birth Year(s): {}".format(most_common_birth_year))
    
    except KeyError:
        print(" " * 4, "Birth Year data assessment not possible for this data set. Column 'Birth Year' was not found.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def chunker(df, rows):
    """
    Generator returning a predefined number of items from a pandas DataFrame.

    Args:
        (df) df - Reference to pandas DataFrame
        (int) rows - number of rows to be returned
    """
    for i in range(0, len(df), rows):
        yield df[i:i+rows]


def main():
    run_assessment = True
    while run_assessment:
        city, month, weekday = get_filters()

        # Only excecute if user did not cancel any of the data input steps
        if not city == KEY_CANCEL:
            if weekday == 0:
                weekday_name = "All"
            else:
                weekday_name = calendar.day_name[weekday-1]

            message = "Your selection: City = {}, Month = {}, Weekday = {}".format(city.title(), calendar.month_name[month], weekday_name)
            print(message.replace("= ,", "= All,"))
            print("Loading data...")
            df = load_data(city, month, weekday-1)
        
            # cancel if no data was found
            if df.empty:
                message = "Your filter did not yield any records. Seems like there were no trips made in {} for this selection: Month = {}, Weekday = {}".format(city.title(), calendar.month_name[month], weekday_name)
                print(message.replace("= ,", "= All,"))
            
            # data assessment
            else:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)

                # Display chunks of raw data if requested
                if get_userinput_yesno("Do you want to see 5 lines of raw data?", default_val=KEY_NO):
                    for chunk in chunker(df, 5):
                        print(chunk)
                        # Display next 5 lines?
                        if not get_userinput_yesno("Do you want to see the next 5 lines of raw data?"):
                            break


        # Run another assesment?
        run_assessment = get_userinput_yesno("Do you want to analyze another set of data?")

if __name__ == "__main__":
    main()