import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup

# Create your views here.
@api_view(['GET'])
def get_details(request,country_name):
    r=requests.get("https://en.wikipedia.org/wiki/"+country_name)
    soup = BeautifulSoup(r.content,"html.parser")

    table_data = soup.find('table',{'class','infobox ib-country vcard'})
    flag_link = "https:"+table_data.find('img',{'class','thumbborder'})["src"]
    infobox_data = table_data.find_all('tr')

    for c in range(len(infobox_data)):
        th_data=infobox_data[c].find('th')

        if (th_data!=None and th_data.get_text()=="Capitaland largest city"):
            capitals = [i.get('title') for i in infobox_data[c].find_all('a') if i.get('title') is not None]
            large_cities=capitals

        if (th_data!=None and th_data.get_text()=="Capital"):
            capitals = [i.get('title') for i in infobox_data[c].find_all('a') if i.get('title') is not None]

        if (th_data!=None and th_data.get_text()=="Largest city"):
            large_cities = [i.get('title') for i in infobox_data[c].find_all('a') if i.get('title') is not None]

        if (th_data!=None and "Official" in th_data.get_text() and "languages" in th_data.get_text()):
            offical_languages = [i.get('title') for i in infobox_data[c].find('td').find_all('a') if i.get('title') is not None]

        if(th_data!=None and th_data.find('a')!=None and th_data.find('a').get_text()=="Area "):
            area_total= infobox_data[c+1].find('td').get_text().split('[')[0].split('(')[0]

        if(th_data!=None and th_data.find('a')!=None and th_data.find('a').get_text()=="Population"):
            population= infobox_data[c+1].find('td').get_text().split('[')[0].split('(')[0]

        if(th_data!=None and th_data.find('a')!=None and th_data.find('a').get_text()=="GDP" and th_data.find('span').get_text()=="(nominal)"):
            GDP_nominal= infobox_data[c+1].find('td').get_text().split('[')[0]

    return Response({"flag_link":flag_link,"capitals":capitals,"largest_city":large_cities,"offical_languages":offical_languages,"area_total":area_total,"population":population,"GDP_nominal":GDP_nominal})
