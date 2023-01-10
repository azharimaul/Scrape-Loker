import scrapy


class PtcitSpider(scrapy.Spider):
    name = 'ptcit'
    allowed_domains = ['www.daftarperusahaan.com']
    start_urls = ['https://www.daftarperusahaan.com/bisnis/kecamatan/citeureup?page=0']


    def parse(self, response):
        page = 1
        for url in response.css("div.clear-block").css("h2").css("a::attr(href)"):     #loop list
            yield response.follow("https://www.daftarperusahaan.com" + url.get(), callback = self.parse_categories)
            
            
            next_page = "https://www.daftarperusahaan.com/bisnis/kecamatan/citeureup?page=" + str(page)
            page += 1
            if page < 13:      #page limit
                yield response.follow(next_page, callback = self.parse)
            
    def parse_categories(self, response):
        #for job in response.css("div.JobCardsc__JobcardContainer-sc-1f9hdu8-0"):
            detail = {
                "pt": (response.css("div.content.clear-block").css("strong::text").get()).replace("Profil Bisnis ",""),
                "keterangan":(((((" ".join(response.css("div.content.clear-block::text").getall())).replace("\n\n", "")).replace("\t","")).replace("  ","")).replace("\n","")).replace("Alamat : Kecamatan Citeureup,Kabupaten Bogor,Provinsi Jawa Barat ",""),
                "jalan": response.css("div.content.clear-block").css("p::text").get()
            }
            yield detail
            
            
