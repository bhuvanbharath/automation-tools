import smtplib, requests, csv, os
from bs4 import BeautifulSoup
URL = 'https://www.udemy.com/course/ethereum-and-solidity-the-complete-developers-guide/'
page = requests.get(URL)    
soup = BeautifulSoup(page.content,'html.parser')
#print(page.text)
results = soup.find('div', attrs = {'class':'ud-component--course-landing-page-udlite--curriculum'})
#print(results)
section_elements = results.find_all('span', class_='section--section-title--8blTh')
sections_list=[]
names_list=[]
sectionNo = 1

for section_element in section_elements:
    section_element = section_element.text.strip()
    section_element = "Section "+str(sectionNo)+'. '+section_element
    sections_list.append(section_element)
    sectionNo=sectionNo+1

name_elements = results.find_all('div', class_='section--row--3PNBT')
for name_elem in name_elements:
    name_elem = name_elem.text.strip()
    print(name_elem, end="\n"*2)
    names_list.append(name_elem)

cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))

with open(r"C:\\Users\\Bhuvan Bharath T\\OneDrive\\Documents\\GitHub\\automation-tools\\Scrap Udemy web\\section_contents.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    for secName in sections_list:
        writer.writerow([secName])
    writer.writerow([" "])
    for Name in names_list:
        writer.writerow([Name])
# print("SECTION LIST\n")
# for elem in sections_list:
#     print(elem, end="\n"*2)




    

