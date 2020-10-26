#!/usr/bin/python
import re
import argparse
from bs4 import BeautifulSoup as BS
from operator import itemgetter

parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store', dest='input_file', help='input file name')
parser.add_argument('-o', action='store', dest='output_file', help='input file name')

output_file_name = parser.parse_args().output_file
input_file_name = parser.parse_args().input_file


with open(input_file_name, "r") as f:
    html = f.read()
    soup = BS(html, 'html.parser')

lan_info_odd_list = soup.findAll(class_ = ['view-content'])[0].findAll(class_="views-row-odd")
lan_info_even_list = soup.findAll(class_ = ['view-content'])[0].findAll(class_="views-row-even")

lan_info_list = lan_info_odd_list + lan_info_even_list

def get_lan_info(lan_info, *args):

    # language name
    lan_name = lan_info.find('div', {'class': 'title'}).text.strip()



    # language info
    info = lan_info.find('div', {'class': 'content'})
    info_title_list = [ title_bs.text for title_bs in info.findAll('em') ]
    info_contents = [ info.string.strip() for info in info.contents ]

    

    def find_info(title, lan_name=lan_name):
        result = ''
        title += ':'
        for i, content in enumerate(info_contents):
            if content == title:
                result = info_contents[i+1]
        return result



    lan_class = [ x.strip() for x in find_info("Classification")[:-1].split(",") ]
    lan_dialects = find_info("Dialects")[:-1]
    lan_dialects = re.sub(r'\n', ' ', lan_dialects) # remove linebreak

    lan_class.append(lan_name)
    lan_class.append(lan_dialects)

    return lan_class




lan_list = []
for lan in lan_info_list:
    result = tuple(get_lan_info(lan))
    lan_list.append(result)


lan_list_sorted = sorted(lan_list)

with open(output_file_name, 'w') as f:
    for lan in lan_list_sorted:
        line = ";".join(lan) 
        f.writelines(f"{line}\n")
