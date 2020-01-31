"""
Small program just to train web scrapping.
Receives the imdb page from show/movie, 
and checks if there are any actors that participated in Dr.Who.
Todo:
    -   If there arent any actors in said show/movie, calculate how many steps away from Dr.Who 
        it is.
    -   Check from a list of movies/shows
"""
import sys
import pandas as pd 
from bs4 import BeautifulSoup as bs 
import requests
import pprint as pp 


# DW page from imdb
dwURL="https://www.imdb.com/title/tt0436992/"
# Requesting the contents of the url and storing them
def actorslist(url):
    """
    First, get the full cast link from page
    """
    html_page = requests.get(url)
    soup = bs(html_page.content,'html.parser')
    links = []
    for link in soup.findAll('a',text="See full cast",href=True):
        if link.text:
            url = url+link['href']
    tables = pd.read_html(url)
    """
    Series Cast List
    1. Gets the actors table
    2. Filter out nan values from the actors column
    3. Turn it into a list
    """
    return tables[2].dropna(subset=[1])[1].to_list()

def commonactors(list1,list2):
    #Creates a list with elements present in both lists
    return [element for element in list1 if element in list2]
    
if __name__ == "__main__":
    dwcast = actorslist(dwURL)
    cast = actorslist(sys.argv[1])
    intersect = commonactors(dwcast,cast)
    if not intersect:
        print("No common actors")
    else:
        print(f"There are {len(intersect)} common actors:")
        pp.pprint(intersect)
    pass
