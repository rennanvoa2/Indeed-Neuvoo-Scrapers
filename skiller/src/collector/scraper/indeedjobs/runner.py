import sys
sys.path.append('...')

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.indeed_us import IndeedUsSpider
import pandas as pd
import os
from collector import Collector
from datetime import datetime
import random
import urllib.request


class IndeedScraper(Collector):

    def __init__(self, **args):
        super(IndeedScraper, self).__init__()
        self.now = datetime.now()

        #Collector.__init__(self, name=args.get('name'))
        self._name = "Indeed"

        self._user_agents =[
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            ]


    def get_proxies(self,country):
        """
        This function download a proxy list to a file taking into consideration the continent.
        """
        americas = [
            "ar", #Argentina
            "ca", #Canada
            "us", #United States
            "br" #Brazil
        ]

        #Europe
        europe = [
            "uk", #United Kingdom
            "fr", #France
            "ru", #Russia
            "de", #Germany
            "fi", #Finland
            "se", #Sweden
            "it", #Italy
            "es", #Spain
            "be", #Belgium
            "at", #Austria
            "no", #Norway
            "ch", #Switzerland
            "nl" #Netherlands

        ]

        #Asia + Oceany
        asia = [
            "sg", #Singapore
            "jp", #Japan
            "au" #Australia
        ]

        if country in europe:
            #France proxies
            url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=FR&ssl=all&anonymity=all'
            urllib.request.urlretrieve(url, '../../../skiller/data/input/proxy-list.txt')

        elif country in americas:
            #US proxies
            url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=all&anonymity=all'
            urllib.request.urlretrieve(url, '../../../skiller/data/input/proxy-list.txt')

        elif country in asia:
            #Use Thayland proxies
            url = 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=TH&ssl=all&anonymity=all'
            urllib.request.urlretrieve(url, '../../../skiller/data/input/proxy-list.txt')
        else:
            raise Exception("Proxy URL not found, country:",country)



    def run (self, job_title_list, country, location_list):

        #If the temp directory don't exist, create it.
        if not os.path.exists(r"temp/"):
            os.makedirs(r"temp/")

        #Download the proxy list file
        self.get_proxies(country)

        #Crawl indeed for each job title in job_title_list
        for job_ in job_title_list:
            for location in location_list:
                #Instanciate settings
                settings = get_project_settings()

                #Choose format
                settings['FEED_FORMAT'] = 'csv'

                #Choose output folder
                settings['FEED_URI'] = 'temp/' + job_ + '.csv'

                # #Enable proxy
                # settings['PROXY_POOL_ENABLED'] = True


                # settings['ROTATING_PROXY_LIST_PATH'] = '../../../skiller/data/input/proxy-list.txt'
                # settings['DOWNLOADER_MIDDLEWARES'] = {
                # # ...
                # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
                # # ...
                # }

                #Instanciate the Process
                process = CrawlerProcess(settings=settings)

                #Crawl
                process.crawl(IndeedUsSpider, job_title=job_, country=country, location=location)

        #Start
        process.start(stop_after_crawl=True)

        #Make a list with each file from temp directory
        files_list = list(os.listdir("temp"))

        #start the Dataframe as None
        df = None
        #iterate over the other files appending to df dataframe
        for index,file in enumerate(files_list):
            try:
                #Avoid mac hide file
                if file == '.DS_Store':
                    continue

                else:
                    #If still None create the dataframe of the first file
                    if df is None:
                        df = pd.read_csv("temp/"+ file)

                    #If It's not null append file to the dataframe
                    else:
                        file = pd.read_csv("temp/"+ files_list[index])
                        df = pd.concat([df, file], ignore_index=True)
            except:
                print("No data in ",file)

        #clear the directory
        for file in files_list:
            os.remove("temp/"+file)

        #Remove the null values on description
        try:
            df = df[~df['description'].isnull()]
        except:
            pass
        #Remove the wrong scrapped rows
        df = df.loc[~(df["job_title"] == "job_title")]

        return df