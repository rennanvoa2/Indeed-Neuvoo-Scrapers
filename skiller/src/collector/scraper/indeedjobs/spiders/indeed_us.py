# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import datetime



class IndeedUsSpider(CrawlSpider):
    def get_country(self,country,query,location):
        countries_begin_url = [
            "ar", #Argentina
            "ru", #Russia
            "de", #Germany
            "fi", #Finland
            "sg", #Singapore
            "se", #Sweden
            "it", #Italy
            "es", #Spain
            "be", #Belgium
            "at", #Austria
            "no", #Norway
            "ca", #Canada
            "au", #Australia
            "jp" #Japan
        ]
        end_countries_url = [
            "fr", #France
            "ch", #Switzerland
            "nl" #Netherlands
        ]

        #EXCEPTIONS

        #United States
        if country.lower() == "us":
            url = [f'https://www.indeed.com/jobs?q='+ query +'&l=' + location]
            domain = "www.indeed.com"

        #Brasil
        elif country.lower() == "br":
            url = [f'https://www.indeed.com.br/jobs?q='+ query +'&l=' + location]
            domain = "www.indeed.com.br"

        #United Kingdom
        elif country == "uk":
            url= [f'https://www.indeed.co.uk/jobs?q='+ query +'&l=' + location]
            domain = "www.indeed.co.uk"

        #Countries in the beginning of Indeed URL
        elif country in countries_begin_url:
            url= [f'https://'+country.lower() +'.indeed.com/jobs?q='+ query +'&l=' + location]
            domain = country.lower() + ".indeed.com"

        #Countries in the end of Indeed URL
        elif country in end_countries_url:
            url = [f'https://www.indeed.'+ country + '/jobs?q='+ query +'&l=' + location]
            domain = "www.indeed." + country

        else:
            raise Exception("Wrong country:",country)

        return url,domain

    def __init__(self, job_title='', country='',location='',**kwargs):
        job_title = job_title.lower()
        self._job_title = job_title.lower()
        query = self._job_title.replace(" ","+")
        self.country = country
        location=location.lower()
        location = location.replace(" ","+")
        self.start_urls,allowed_domains = self.get_country(country,query,location)
        super().__init__(**kwargs)  # python3

    name = 'indeed_us'
    download_delay = 0.2

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h2[@class='title']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="(//span[@class='pn']/span)[last()]"), follow=True)
    )

    def parse_item(self, response):

        #Scrap the description
        texto = ""

        if response.xpath("//div[@id='jobDescriptionText']//text()").get() != None:
            result = response.xpath("//div[@id='jobDescriptionText']//text()")
            for text in result:
                texto += text.get()
                texto += " "
        #If the first fail try this one
        if texto == "":
            #This is the best xpath to get the descriptions
            if response.xpath("//div[@id='jobDescriptionText']/descendant::text()").get() != None:
                result = response.xpath("//div[@id='jobDescriptionText']/descendant::text()")
                for text in result:
                    texto += text.get()
                    texto += " "



        #This is the last option because this go through all the possibilities and the structure its not good.
        if texto == "":
            if response.xpath("//div[@id='jobDescriptionText']/p").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/p"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "

            if response.xpath("//div[@id='jobDescriptionText']/div/p").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/div/p"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "

            if response.xpath("//div[@id='jobDescriptionText']/div/div/p").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/div/div/p"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "

            if response.xpath("//div[@id='jobDescriptionText']/div/ul/li").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/div/ul/li"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "

            if response.xpath("//div[@id='jobDescriptionText']/div/div/ul/li").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/div/div/ul/li"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "

            if response.xpath("//div[@id='jobDescriptionText']/ul/li").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/ul/li"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "

            if response.xpath("//div[@id='jobDescriptionText']/div/div/div/text()").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/div/div/div/text()"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "

            if response.xpath("//div[@id='jobDescriptionText']/div/div/div/div/text()").get() != None:
                for text in response.xpath("//div[@id='jobDescriptionText']/ul/li"):
                    selec = text.xpath(".//text()")
                    texto += selec.get()
                    texto += " "
        texto = texto.replace("\n", " ")


        #Companies
        if response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[1]/a/text()").get() != None:
            company = response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[1]/a/text()").get()

        if response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[1]/text()").get() != None:
            company = response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[1]/text()").get()


        #remove the beginning and end of the url to create a jobkey
        jobkey = str(response.url)

        #scrap how many days ago
        when_published = response.xpath("//div[@class='jobsearch-JobMetadataFooter']/text()").get()
        when_published = re.findall(r"\d+", str(when_published))

        #if the regex function return more than 1 item, get the first.
        if isinstance(when_published,list) and len(when_published) > 0:
            when_published = when_published[0]
        else:
            when_published = "Not found"

        #use the result from regex to create the date
        try:
            job_date = datetime.date.today() - datetime.timedelta(days=int(when_published))
            date = str(job_date.day)+"/"+str(job_date.month)+"/"+str(job_date.year)

        except:
            date = "Not Found"

        local = "Not Found"

        if response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[last()]/text()").get() is not None:
            local = response.xpath("//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch-DesktopStickyContainer-companyrating']/div[last()]/text()").get()

        if self.country == "com":
            self._country_output = "US"
        else:
            self._country_output = self.country

        if response.xpath("//div[@class='jobsearch-JobInfoHeader-title-container']/h1/text()").get() is not None:
            self.job_title_found = response.xpath("//div[@class='jobsearch-JobInfoHeader-title-container']/h1/text()").get()
        else:
            self.job_title_found = response.xpath("//div[@class='jobsearch-DesktopStickyContainer']/h1/text()").get()

        yield {
            "job_title" : self._job_title,
            "job_title_found" : self.job_title_found,
            "company": company,
            "location":local,
            "country": self._country_output,
            "sources": "Indeed",
            "jobkeys":jobkey,
            "dates" : date,
            "description": texto
            #"link": response.url
        }