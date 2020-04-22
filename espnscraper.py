import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import re
from pandas.io.html import read_html
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Create the master array and data frame
master_list = []
master_frame = pd.DataFrame(master_list)

# This is the year. We'll be iterating over this for a bit.
year = 2018
# This is the text of the ESPN site, minus the year
site = "http://www.espn.com/mlb/attendance/_/year/"

# Begin the loop!
while year > 2000:

    # Put the URL of the site we want and put it in a string, URL
    # Then, grab the HTML and put it in a string, html
    url = site + str(year)
    html = urlopen(url)

    # Extract the soup from the HTML code
    soup = BeautifulSoup(html, 'lxml')

    # We only want the table rows, 'tr'. So we'll grab those from the soup.
    all_rows = soup.find_all('tr')

    # Now get each row and put in an array
    list_rows = []
    for row in all_rows:
        cells = row.find_all('td')
        str_cells = str(cells)
        clean = re.compile('<.*?>')
        clean2 = (re.sub(clean, '', str_cells))
        list_rows.append(clean2)

    # Put the array in a DataFrame
    df = pd.DataFrame(list_rows)
    # clip off just the data we want -- the last 30 rows
    df1 = df.tail(30)
    # Split the columns by commas -- don't forget the space!
    df2 = df1[0].str.split(', ', expand=True)
    # There's an extra bracket, get rid of it
    df2[0] = df2[0].str.strip('[')
    # Insert a column with the year
    df2['Year'] = year
    # Add it to the master data frame
    master_frame = master_frame.append(df2)
    # Decrease the year
    year -= 1

# Once the loop is done, send the master frame to a CSV
master_frame.to_csv(r'C:\Users\evilg\Downloads\attendance_output.csv', header=False)



