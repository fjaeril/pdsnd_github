>**Note**: Please **fork** the current Udacity repository so that you will have a **remote** repository in **your** Github account. Clone the remote repository to your local machine. Later, as a part of the project "Post your Work on Github", you will push your proposed changes to the remote repository in your Github account.

# Basic data exploration of Bikeshare data using pandas

### Description
This project was part of the Udacity Nandodegree "Python programming for data science". The Python program allows the user to do a basic data exploration of predefined data sets.

** Optional filter options **
When running the program, the user is first requested to enter the name of the city for which the data assessment is to be carried out. Afterwards the user may define filters for month and the week day. Both are optional.
* Month: 1 (January) to 12 (December)
* Week day: 1 (Monday) to 7 (Sunday)

** Data exploration **
Based on the user input the program extracts and calculates basic statistical information about trips, stations and the users.
* Most frequent times of travel (month, week day, start hour)
* Most popular start end end stations as well as trips
* Total and mean travel time
* User statistics (type, gender, birth year,)

** Raw data view **
After the basic data exploration, user can request raw data to be displayed. Per request 5 lines of raw data is shown

### Files used
* bikeshare.py - Actual Python script
* chicago.csv - Bike rental raw data of Chicago
* new_york_city.csv - Bike rental raw data of New York City
* washington.csv - Bike rental raw data of Washington

### Built with
* Pyhton 3.9.13
* pandas library
* numpy library
* time library
* calendar library
* datetime library
* Visual Studio Code

### Author
[fjaeril](https://github.com/fjaeril/) - Sole author

### Credits
* Udacity nanodegree and the provided sample file
* Human readable time deltas - [Stack Overflow](https://stackoverflow.com/questions/538666/format-timedelta-to-string)
* Getting Month name from number - [PYnative](https://pynative.com/python-get-month-name-from-number/)

