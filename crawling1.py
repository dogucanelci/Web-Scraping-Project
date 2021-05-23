import requests
from bs4 import BeautifulSoup
import os
page = requests.get("https://www.spreadthesign.com/tr.tr/search/by-category/")
#print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')

a=soup.find_all("a",href=True)
int = 10
general_list = []
bool1 = False
for i in a:
    str = i['href']
    str = "https://www.spreadthesign.com"+str   #renkler
    if(str=="https://www.spreadthesign.com/tr.tr/search/by-category/255/bebek-isaretleri/"):
        bool1=True
    if(bool1):
        nextpage = False
        if(int<10):
            int+=1
            pass
        else:
            counter=str.count("by-category")
            if(counter!=0):
                print(i['href'], i.get_text())
                page1=requests.get(str)
                soup1 = BeautifulSoup(page1.content,"html.parser")
                a1=soup1.find_all("a",href=True)
                while(nextpage==False):
                    for j in a1:
                        str1 = j['href']
                        str1="https://www.spreadthesign.com"+str1
                        counter = str1.count("?q=")
                        if(j.get_text()=="Sonraki sayfa"):
                            nextpagestr=j['href']
                            nextpage=True
                        if (counter != 0):
                        #    print(str1) #bej
                            page2 = requests.get(str1)
                            soup2=BeautifulSoup(page2.content,"html.parser")
                            a2=soup2.find_all(class_="js-enforce-speed")
                            if(a2):
                                new_element=[]
                                for k in a2:
                                    new_element.append(k["src"])
                                #    print(k["src"])
                                a2 = soup2.find_all("h2")
                                for k in a2:
                                    name = k.get_text()
                                    name = name.replace("\n","")
                                    name = name.replace(" ", "")
                                    new_element.append(name)
                                #    print(name)
                                #print("*********************")
                                general_list.append(new_element)
                    if(nextpage==True):
                        str_next = str + nextpagestr
                        page1 = requests.get(str_next)
                        soup1 = BeautifulSoup(page1.content, "html.parser")
                        a1 = soup1.find_all("a", href=True)
                        nextpage=False
                    else:
                        nextpage=True
        for i in general_list:
            cont = i[1].count("/")
            if(cont>0):
                i[1] = i[1].replace("/"," ")
            else:
                try:
                    r = requests.get(i[0], allow_redirects=True)
                    os.makedirs("./sozlukcu"+"/"+i[1])
                    with open("./sozlukcu/" +  i[1] + "/" + i[1] + ".mp4", 'wb') as f:
                        f.write(r.content)
                except:
                    with open("./" + i[1] + ".mp4", 'wb') as f:
                        f.write(r.content)
        general_list=[]
print(general_list)