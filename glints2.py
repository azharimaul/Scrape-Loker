import scrapy


class Glints2Spider(scrapy.Spider):
    name = 'glints2'
    allowed_domains = ['glints.com']
    start_urls = ['https://glints.com/id/opportunities/jobs/explore?country=ID&locationName=Indonesia&sortBy=LATEST&jobTypes=INTERNSHIP&page=1']

    def parse(self, response):
        for url in response.css("a.CompactOpportunityCardsc__CardAnchorWrapper-sc-1y4v110-18::attr(href)"):
            yield response.follow(url.get(), callback = self.parse_categories)
            
            next_page = "https://glints.com" + response.css("div.AnchorPaginationsc__PaginationContainer-sc-1etfdu-0").css("a::attr(href)").getall()[5] 
            if int(response.css("div.AnchorPaginationsc__PaginationContainer-sc-1etfdu-0").css("a::attr(href)").getall()[10][-1]) < 5:
                yield response.follow(next_page, callback = self.parse)
            
    def parse_categories(self, response):
        #for job in response.css("div.JobCardsc__JobcardContainer-sc-1f9hdu8-0"):
            detail = {
                "job": response.css("h1.TopFoldsc__JobOverViewTitle-sc-kklg8i-3::text").get(),
                "company": response.css("div.TopFoldsc__JobOverViewCompanyName-sc-kklg8i-5 a::text").get(),
                "location": response.css("a.Breadcrumbsc__BreadcrumbJobLink-sc-uhs14r-3.KHKYb::text").getall()[2],
                "req": response.css("div.public-DraftStyleDefault-block span span::text").getall()
                
            }
            yield detail
            
            