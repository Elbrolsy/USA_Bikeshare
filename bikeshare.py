import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


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
    city = ''
    while city == '':
        print("\nEnter The Desired City Name: (chicago, new york city, washington)")
        city = input().lower()
        if city == "chicago" or city == 'new york city' or city == 'washington':
            city = city
        else:
            city = ''
            print("Enter a Vallid City Name.")

    # get user input for month (all, january, february, ... , june)
    month = ''
    months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun':6, 'all': 'all'}

    while month == '':
        print("\nEnter The Desired Month: (jan, feb, mar, apr, may, jun) or 'all' for no filter")
        month = input().lower()
        if month == "jan" or month == "feb" or month == "mar" or month == "apr" or month == "may" or month == "jun" or month == "all":
            month = months[month]
        else:
            month = ''
            print("This is Not a Vallid Option, Enter a Vallid Month.\n")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    days = {'sa': 'Saturday', 'su': 'Sunday', 'mo': 'Monday', 'tu': 'Tuesday', 'we': 'Wednesday', 'th':'Thursday', 'fr':'Friday', 'all': 'all'}

    while day == '':
        print("Enter The Desired Day: (sa, su, mo, tu, we, th, fr) or 'all' for no filter")
        day = input().lower()
        if day == "sa" or day == "su" or day == "mo" or day == "tu" or day == "we" or day == "th" or day == "fr" or day == "all":
            day = days[day]
        else:
            day = ''
            print("This is Not a Vallid Option, Enter a Vallid Day.\n")
            
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    print('-'*80)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]  
    months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun'}
    popular_month = months[popular_month]
    print('Most Common Month is:', popular_month)

    # display the most common day of week
    popular_day = df['day'].mode()[0]  
    days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    popular_day = days[popular_day]

    print('Most Common Day is:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]  
    print('Most Common Start Hour is:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    popular_start_station_df = df[df['Start Station'] == popular_start_station]
    popular_start_station_count = popular_start_station_df['Start Station'].value_counts()[0]
    print('Most Popular Start Station is: ({}) with Count of: ({}) Starting Trip'.format(popular_start_station,popular_start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    popular_end_station_df = df[df['End Station'] == popular_end_station]
    popular_end_station_count = popular_end_station_df['End Station'].value_counts()[0]
    print('Most Popular End Station is: ({}) with Count of: ({}) Ending Trip'.format(popular_end_station,popular_end_station_count))

    # display most frequent combination of start station and end station trip
    popular_combo = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most Frequent Combination of Start and End Stations is: ({}) and ({})".format(popular_combo[0], popular_combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time']-df['Start Time']

    # display total travel time
    total_travel_time = pd.Timedelta.total_seconds(df['Travel Time'].sum())
    print('Total Travel Time is: {} Seconds'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = pd.Timedelta.total_seconds(df['Travel Time'].mean())
    print('Average Travel Time is: {} Seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The Count of Each User Type is: ")
    print(user_types, '\n')
    head = []
    for col in df.columns:
        head.append(col)

    # Display counts of gender
    if len(head) > 7:
        if head[7] == 'Gender':
            gender_count = df['Gender'].value_counts()
            print("The Gender Count is: ")
            print(gender_count,'\n')

    # Display earliest, most recent, and most common year of birth
    if len(head) > 7:
        if head[8] == 'Birth Year':
            earliest = int(df['Birth Year'].min())
            most_recent = int(df['Birth Year'].max())
            most_common = int(df['Birth Year'].mean())

            print("The Oldest Person Was Born in: ", earliest)
            print("The Youngest Person Was Born in: ", most_recent)
            print("The Most Common Year of Birth is: ", most_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def raw_data(df):
    print_data = True
    print("Do you want to see the first 5 rows of the data? (yes or no)")
    x = input()
    if x == 'yes':
        print_data = True
    else:
        print_data = False
    n = 0    
    while print_data == True:
        print(df.iloc[n:n+5,:])
        print("Do you want to see the next 5 rows of the data? (yes or no)")
        x = input()
        if x == 'yes':
              n += 5
              print_data = True
        else:
              print_data = False
    
def main():
    while True:
        #Define parameters and DataFrame
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #Initiate all functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        #End condition
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()