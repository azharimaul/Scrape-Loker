import scrapy


class GlintsSpider(scrapy.Spider):
    name = 'glints'
    allowed_domains = ['glints.com']
    start_urls = ['https://glints.com/id/opportunities/jobs/explore?country=ID&locationName=Indonesia&sortBy=LATEST&jobTypes=INTERNSHIP&page=1']

    def parse(self, response):
        jobs = response.css("div.JobCardsc__JobcardContainer-sc-1f9hdu8-0")
        for job in jobs:
            item = {
            'judul' : job.css("h2::text").get(),
            'company' : job.css("a.CompactOpportunityCardsc__CompanyLink-sc-1y4v110-8::text").get(),
            'link' : '=HYPERLINK("'+"https://glints.com/"+job.css("a.CompactOpportunityCardsc__CardAnchorWrapper-sc-1y4v110-18::attr(href)").get()+'", "'+job.css("h2::text").get()+'")',
            'lokasi' : job.css("div.CompactOpportunityCardsc__OpportunityInfo-sc-1y4v110-13").css("span::text").get()
            }
            yield item

            next_page = "https://glints.com" + response.css("div.AnchorPaginationsc__PaginationContainer-sc-1etfdu-0").css("a::attr(href)").getall()[5] 
            if int(response.css("div.AnchorPaginationsc__PaginationContainer-sc-1etfdu-0").css("a::attr(href)").getall()[5][-1]) < 5:
                yield response.follow(next_page, callback = self.parse)
