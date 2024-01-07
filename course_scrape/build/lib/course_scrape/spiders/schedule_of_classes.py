import scrapy
from scrapy.crawler import CrawlerProcess

class ScheduleOfClassesSpider(scrapy.Spider):
    name = "schedule_of_classes"
    allowed_domains = ["classes.uwaterloo.ca"]

    def __init__(self, level=None, term=None, subject=None, cournum=None, desired_class_num=None, *args, **kwargs):
        super(ScheduleOfClassesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?level={level}&sess={term}&subject={subject}&cournum={cournum}"]
        self.desired_class_num = desired_class_num

    def parse(self, response):
        #selection = response.xpath('//main/text()[3]').getall()
        rows = response.xpath('//table/tr[4]/td[2]/table/tr')

        for row in rows:
            class_num = row.xpath('./td[1]/text()').get()

            try:
                if (class_num.strip() == self.desired_class_num):
                    section = row.xpath('./td[2]/text()').get()
                    location = row.xpath('./td[3]/text()').get()
                    enrl_cap = row.xpath('./td[7]/text()').get()
                    enrl_tot = row.xpath('./td[8]/text()').get()
                    time_days = row.xpath('./td[11]/text()').get()

                    yield {
                        'classnum': class_num.strip(),
                        'section': section.strip(),
                        'location': location.strip(),
                        'enrl_cap': enrl_cap.strip(),
                        'enrl_tot': enrl_tot.strip(),
                        'time_days': time_days.strip()
                    }
            except:
                pass

process = CrawlerProcess()
process.crawl(ScheduleOfClassesSpider, level=input("Enter level:"), term=input("Enter term:"), subject=input("Enter subject:"), cournum=input("Enter course number:"), desired_class_num=input("Enter desired class number:"))
process.start()
