import time
import pandas as pd
import numpy as np
import click
#Global Variables
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
city=' '
months = ['January', 'February', 'March', 'April', 'May', 'June']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    """
     To handle unexpected input well without failing Click library was used for asking a valid response from a user.
     More details in the README file. 
    """
    # get user input for city (chicago, new york city, washington).
    cities = CITY_DATA.keys()
    #asking the user for the city input
    city = click.prompt('Please select one of the following cities', type=click.Choice(cities, case_sensitive=False))

    # get user input for month (all, january, february, ... , june)
    mchoices= months.copy()
    mchoices.insert(0,'all')
    #asking the user for month input
    month=click.prompt('Would you like to filter the data by specific month, or all?\nPlease choose one of the following options\n', type=click.Choice(mchoices, case_sensitive=False))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    wchoices=np.array(['all','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
    #asking the user for the day input
    day=click.prompt('Would you like to filter the data by specific day of the week, or all?\nPlease choose one of the following options\n', type=click.Choice(wchoices, case_sensitive=False))

    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA [city])
    # convert the Start Time column to datetime
    df['Start Time'] =pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1
        # filter by month to create the new dataframe
        df =  df[df['month']==month]
    # filter by day of week if applicable
    if day != 'all':
       # filter by day of week to create the new dataframe
       df = df[df['day_of_week']== day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        Dataframe df. 
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour, month, day of the week from the Start Time column to create three columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # find the most common hour, month, and day of the week using mode function 
    popular_hour = df['hour'].mode()[0]
    popular_month = df['month'].mode()[0]
    #extracting the name based on it's number from the months' list
    month = months[popular_month-1]
    popular_dayOfWeek = df['day_of_week'].mode()[0]
    # display the most common start hour
    print('Most Frequent Start Hour:', popular_hour)
    # display the most common month
    print('Most Frequent Start Month:', month)
     # display the most common day of week
    print('Most Frequent Start Day of Week:', popular_dayOfWeek)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
       Args: 
        Dataframe df.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # find the most commonly used start station
    popular_startStation = df['Start Station'].mode()[0]
    # display most commonly used start station
    print('Most Frequent Start Station:', popular_startStation)
    # find the most commonly used end station
    popular_endStation = df['End Station'].mode()[0]
    # display most commonly used end station
    print('Most Frequent End Station:', popular_endStation)
    # find the most commonly combination of start station and end station trip using groupby function , size , and idmax
    MostComb=df.groupby(['Start Station', 'End Station']).size().idxmax()
    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station',MostComb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
        Args:
            Dataframe df.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # find the sum of the trip duration
    total_travel_time =df['Trip Duration'].sum()
    # display total travel time
    print('Total travel time:', total_travel_time)
    # find the average of the trip duration
    average_travel_time =df['Trip Duration'].mean()
    # display mean travel time
    print('Average travel time:', average_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users.
        Args:
            (str) city - name of the city to analyze
            Dataframe df.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # find the counts for each user type
    user_types = df['User Type'].value_counts()
    # print value counts for each user type
    print(user_types)
    #Checking the city name because the gender and the birth are only available for NYC and Chicago
    if((city == 'new york') or (city == 'chicago')):
       
        # find the counts for each user gender
        user_gender = df['Gender'].value_counts()
        # Display counts of gender
        print(user_gender)
        # Find earliest(min), most recent(max), and most common(mode) year of birth
        earliest_YB=df['Birth Year'].min()
        mostRecent_YB=df['Birth Year'].max()
        mostCommon_YB=df['Birth Year'].mode()
        # Display earliest, most recent, and most common year of birth
        print('Earliest, most recent, most common year of birth respectively: ', earliest_YB,mostRecent_YB,mostCommon_YB)
         
    else:
        print("There is no gender or birth data for the users.")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def ask_rowData(df):
    """ Asking if the user wants to see the raw data.
        Args:
            Dataframe df. 
    """
    row_data = input('Would you like to view 5 rows of the data at a time? Enter yes or no\n').lower()
    startIndex = 0
    yes_Cont = True
    if row_data.lower() == 'yes':
        while yes_Cont :
            print(df.iloc[startIndex:startIndex + 5])
            startIndex +=5
            row_data = input('Would you like to view more rows of the data? Enter yes or no\n').lower()
            if row_data.lower() == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        ask_rowData(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
