import time
import pandas as pd
import numpy as np

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    ###
    # asks user to specify a city, month, and day to analyze.
    ###
    # returns:
    #    (str) city - name of the city to analyze
    #    (str) month - name of the month to filter by, or "all" to apply no month filter
    #    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    ###

    print('Welcome! Let\'s explore some US bikeshare data!\n')

    ### get user input for city (chicago, new york city, washington).
    city_string = "Which city would you like to see data for? (Enter a number)\n";
    idx = 1
    for city in CITY_DATA.keys():
        city_string += str(idx) + '. ' + city + '\n';
        idx += 1
    city_string += '\nSelection: '

    while True:
        try:
            city_num = int(input(city_string)) - 1
            if city_num >= 0 and city_num < len(CITY_DATA):
                city = list(CITY_DATA)[city_num]
                print(" ", city, "\n")
                break
            else:
                print("Invalid selection. Please enter a valid city number.\n")
        except:
            print("You Must Enter A Number.\n")

    ### get user input for month
    month_string = ''

    for month in MONTHS:
        month_string += str(MONTHS.index(month)) + '. ' + month + '\n'
    month_string += '\nSelection: '

    while True:
        try:
            month_num = int(input(month_string))
            if month_num >= 0 and month_num < len(MONTHS):
                month = MONTHS[month_num]
                print(" ", str(month), "\n")
                break
            else:
                print("Invalid selection. Please enter a valid month number.\n")
        except:
            print("You Must Enter A Number.\n")


    ### get user input for day
    while True:
        day = input("Do you want details specific to a particular day? If yes, type day of the week or type 'all'\n")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid selection. Please enter a valid day\n")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    ###
    # Loads data for the specified city and filters by month and day if applicable.
    ###
    # Args:
    #   (str) city - name of the city to analyze
    #   (str) month - name of the month to filter by, or "all" to apply no month filter
    #   (str) day - name of the day of week to filter by, or "all" to apply no day filter
    # Returns:
    #   df - Pandas DataFrame containing city data filtered by month and day
    ###

    ### load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    ### convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    ### extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    ### filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month)

        # filter by month
        df = df[df['month'] == month]

    ### filter by day of week if applicable
    ### TODO Ensure code runs when no data
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    ### displays statistics on the most frequent times of travel.

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    ### display the most common month
    print("The most common month is:", df['month'].mode()[0], "\n")

    ### display the most common day of week
    print("The most common day of week is:", df['day_of_week'].mode()[0], "\n")

    ### display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    ### displays statistics on the most popular stations and trip.

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    ### display most commonly used start station
    print("The most commonly used start station is:", df['Start Station'].mode()[0], "\n")

    ### display most commonly used end station
    print("The most commonly used end station is:", df['End Station'].mode()[0], "\n")

    ### display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip is:", df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    ### displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("The total travel time is ", end='')
    trip_dur_hours = df['Trip Duration'].sum()/60/60
    if trip_dur_hours/24/365 >= 1:
        print("%.1f years\n" % (trip_dur_hours/24/365))
    elif trip_dur_hours/24 >= 1:
        print("%.1f days\n" % (trip_dur_hours/24))
    else:
        print("%.1f hours\n" % (trip_dur_hours))


    print("The trip average time is %.1f minutes\n" % (df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    ### displays statistics on bikeshare users.

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    ### display counts of user types
    if 'User Type' in df.columns:
        user_types = df.groupby(['User Type'])['User Type'].count()
        print(user_types, "\n")
    else:
        print("No User Data")

    ### display counts of gender
    if 'Gender' in df.columns:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print(gender_count)
    else:
        print("No Gender Data")

    ### display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        young_yob = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        young_yob = int(young_yob)
        print("The most recent year of birth is:", young_yob, "\n")

        old_yob = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        old_yob = int(old_yob)
        print("The earliest year of birth is:", old_yob, "\n")

        common_yob = df['Birth Year'].mode()[0]
        common_yob = int(common_yob)
        print("The most common year of birth is:", common_yob, "\n")
    else:
        print("No Birth Year Data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    x = 1

    ### call for raw data output
    while True:
        raw = input('\nWould you like to see some raw data? Enter yes or no.\n')
        if raw.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        elif raw.lower() == 'no':
            break
    ### TODO handle running out of rows of raw data

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes to restart.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
