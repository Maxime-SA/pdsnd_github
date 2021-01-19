import time
import pandas as pd
import numpy as np
import calendar as cl


city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days_of_week = list(cl.day_name)

my_months = ['january', 'february', 'march', 'april', 'may', 'june']

my_hours = {'0' : '12 AM', '1' : '1 AM',  '2' : '2 AM', '3' : '3 AM', '4' : '4 AM', '5' : '5 AM', '6' : '6 AM', '7' : '7 AM', '8' : '8 AM', '9' : '9 AM',
            '10' : '10 AM', '11' : '11 AM', '12' : '12 PM', '13' : '1 PM', '14' : '2 PM', '15' : '3 PM', '16' : '4 PM', '17' : '5 PM', '18' : '6 PM', '19' : '7 PM', '20' : '8 PM', '21' : '9 PM', '22' : '10 PM', '23' : '11 PM'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = input('\nWould you like to see data for Chicago, New York City, or Washington? Just type in your choice!\n').lower()

    while city_input not in city_data:
        print('\nThe city you chose is not a valid key. Make sure you typed \'Chicago\', \'New York City\', or \'Washington\'.')
        city_input = input('Would you like to see data for Chicago, New York City, or Washington? Just type in your choice!\n').lower()

    print('{} it is!'.format(city_input.title()))

    # get user input for how they want to filter the data (month, day, or not at all)
    filter_input = input('\nWould you like to filter the data by month, day, for both (i.e., both), or not at all (i.e., none)? Just type in your choice!\n').lower()

    while filter_input not in ('month', 'day', 'both', 'none'):
        print('\nThe filter you chose is not a valid key. Make sure you typed \'month\', \'day\', \'both\' or \'none\'.')
        filter_input = input('Would you like to filter the data by month, day, for both (i.e., both), or not at all (i.e., none)? Just type in your choice!\n').lower()

    print('By {} it is!'.format(filter_input))

    # get user input for month (all, january, february, ... , june)
    if filter_input in ['month', 'both']:

        month_input = input('\nWould you like to see data for January, February, March, April, May, or June? Just type in your choice!\n').lower()

        while month_input not in my_months:
            print('\nThe month you chose is not a valid key. Make sure you typed \'January\', \'February\', \'March\', \'April\', \'May\', or \'June\'.')
            month_input = input('Would you like to see data for January, February, March, April, May, or June? Just type in your choice!\n').lower()

        print('{} it is!'.format(month_input.title()))

    else: month_input = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_input in ['day', 'both']:

        day_input = input('\nWould you like to see data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Just type in a number from 0 to 6 (i.e., 0 = Monday)!\n').lower()

        while day_input not in str(np.arange(0,7)):
            print('\nThe day you chose is not a valid key. Make sure you typed \'0 for Monday\', \'1 for Tuesday\', \'2 for Wednesday\', \'3 for Thursday\', \'4 for Friday\', \'5 for Saturday\', or \'6 for Sunday\'.')
            day_input = input('Would you like to see data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Just type in a number from 0 to 6 (i.e., 0 = Monday)!\n').lower()

        print('{} it is!'.format(days_of_week[int(day_input)]))

    else:
        day_input = '7'
        days_of_week.append('all')

    print('-'*40)
    return city_input, month_input, days_of_week[int(day_input)]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    df_length = len(df.index)

    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df['month'].unique()) != 1:
        print('The most common month is ... {} which represents {:,d} records out of {:,d} total records (i.e., {:.1%}).'.format(my_months[df['month'].mode()[0] - 1].title(), list(df['month'].value_counts())[0], df_length, list(df['month'].value_counts())[0] / df_length))

    # display the most common day of week
    if len(df['day_of_week'].unique()) != 1:
        print('The most common day of the week is ... {} which represents {:,d} records out of {:,d} total records (i.e., {:.1%}).'.format(df['day_of_week'].mode()[0], list(df['day_of_week'].value_counts())[0], df_length, list(df['day_of_week'].value_counts())[0] / df_length))

    # display the most common start hour
    print('The most common start hour for a trip is ... {} which represents {:,d} records out of {:,d} total records (i.e., {:.1%}).'.format(my_hours[df['Start Time'].dt.hour.mode()[0].astype(str)], list(df['Start Time'].dt.hour.value_counts())[0], df_length, list(df['Start Time'].dt.hour.value_counts())[0] / df_length))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    df_length = len(df.index)

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is ... {} which represents {:,d} records out of {:,d} total records (i.e., {:.1%}).'.format(df['Start Station'].mode()[0], list(df['Start Station'].value_counts())[0], df_length, list(df['Start Station'].value_counts())[0] / df_length))

    # display most commonly used end station
    print('The most commonly used end station is ... {} which represents {:,d} records out of {:,d} total records (i.e., {:.1%}).'.format(df['End Station'].mode()[0], list(df['End Station'].value_counts())[0], df_length, list(df['End Station'].value_counts())[0] / df_length))

    # display most frequent combination of start station and end station trip
    #df['Trip Combination'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    print('The most common combination of start and end station trip is ... {} which represents {:,d} records out of {:,d} total records (i.e., {:.1%}).'.format(('from ' + df['Start Station'] + ' to ' + df['End Station']).mode()[0], list(('from ' + df['Start Station'] + ' to ' + df['End Station']).value_counts())[0], df_length, list(('from ' + df['Start Station'] + ' to ' + df['End Station']).value_counts())[0] / df_length))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is ... {:,} seconds, {:,} minutes, {:,} hours, or {:,} days!'.format(df['Trip Duration'].sum().astype(int), int(df['Trip Duration'].sum() // 60), int(df['Trip Duration'].sum() // 3600), int(df['Trip Duration'].sum() // (86400))))

    # display mean travel time
    print('The mean travel time is ... {:,.1f} seconds or {:,.1f} minues!'.format(df['Trip Duration'].mean(), df['Trip Duration'].mean() / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    temp_df = pd.DataFrame(df['User Type'].value_counts())
    temp_df.rename(columns = {'User Type' : 'User Type Count'}, inplace = True)
    temp_df['% as of Total'] = temp_df['User Type Count'] / temp_df['User Type Count'].sum()
    print('The following shows the different types of users and their respective counts.')
    print(temp_df.to_string(formatters = {'User Type Count' : '{:,}'.format, '% as of Total' : '{:.1%}'.format}))

    # Display counts of gender
    if 'Gender' in df.columns:
        temp_df = pd.DataFrame(df['Gender'].value_counts())
        temp_df.rename(columns = {'Gender' : 'Gender Count'}, inplace = True)
        temp_df['% as of Total'] = temp_df['Gender Count'] / temp_df['Gender Count'].sum()
        print('\nThe following shows the count by gender.')
        print(temp_df.to_string(formatters = {'Gender Count' : '{:,}'.format, '% as of Total' : '{:.1%}'.format}))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe earliest birth year is ... {}.'.format(int(df['Birth Year'].min())))
        print('The most recent birth year is ... {}.'.format(int(df['Birth Year'].max())))
        print('The most common birth year is ... {} which represents {:,d} records out of {:,d} total records (i.e., {:.1%}).'.format(int(df['Birth Year'].mode()[0]), list(df['Birth Year'].value_counts())[0], len(df.index), list(df['Birth Year'].value_counts())[0] / len(df.index)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Will display the raw data 5 rows at a time"""

    raw_data_input = input('Would you like to see the first five rows of the raw data? Just type in yes or no!\n')
    i = 0

    while raw_data_input == 'yes':
        print()
        print(df.iloc[i:(i+5),:])
        raw_data_input = input('\nWould you like to see the next five rows of the raw data? Just type in yes or no!\n')
        i +=5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        chosen_filter = '\nThe following is for {} (i.e., city), {} (i.e., month) and {} (i.e., day)!'.format(city.upper(), month.upper(), day.upper())

        print(chosen_filter)
        time_stats(df)
        print(chosen_filter)
        station_stats(df)
        print(chosen_filter)
        trip_duration_stats(df)
        print(chosen_filter)
        user_stats(df)
        print()
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
