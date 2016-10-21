#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import geocoder, scrapy

class MySpider(scrapy.Spider):
  name='idealista'
  allowed_domains=["idealista.com"]
  start_urls=['https://www.idealista.com/alquiler-viviendas/madrid/chamberi/']

  def parseflat(self,response):

    size=""
    orientation=""
    rooms=""
    misc_data_flat=response.xpath("//*[@id='details']/div[3]/ul/*/text()").extract()
    for i in misc_data_flat:
      if u"m²" in i: size=i
      if u"Orientación" in i: orientation=i
      if "habitaciones" in i: rooms=i

    floor=""
    int_ext=""
    lift=""
    misc_data_bldg=response.xpath("//*[@id='details']/div[4]/ul/*/text()").extract()
    for i in misc_data_bldg:
      if "Planta" in i: floor=i
      if "interior" in i: int_ext="interior"
      if "exterior" in i: int_ext="exterior"
      if "ascensor" in i: lift=i

    addr_approx=response.xpath("//*[@class='main-info']/h1/span/text()")[0].extract().split(' en ')[-1]
    geodata=geocoder.google(addr_approx)
    gps=" ".join([str(i) for i in geodata.latlng])
    cp=geodata.postal
    publicdistance="?"
    
    price=response.xpath("//*[@class='price']/text()")[0].extract().split()[0]
    contact=response.xpath("//*[@class='contact-phones']/*/p/text()")[0].extract()
    #pics="|".join(response.xpath("//img/@src").extract())
    deposit=""
    try: 
      more=response.xpath("//*[@class='more-details']/text()")[0].extract()
      deposit=more[0] if "Fianza" in more[0] else "unknown"
    except: pass
    description=response.xpath("//*[@class='commentsContainer']/div/text()")[0].extract()

    return {'url':response.url,
            'size':size,
            'orientation': orientation,
            'rooms': rooms,
            'floor': floor,
            'int_ext': int_ext,
            'lift': lift,
            'addr_approx': addr_approx,
            'gps': gps,
            'cp': cp,
            'publicdistance': publicdistance,
            'price': price,
            'contact': contact,
            #'pics': pics,
            'deposit': deposit,
            'description': description}

  def parse(self,response):

    flats=[i for i in response.xpath("//a/@href").extract() if "/inmueble/" in i]

    for flat in flats:
      flaturl=response.urljoin(flat)
      yield scrapy.Request(flaturl,callback=self.parseflat)
    
    nexturl=response.xpath('//*[@class="next"]/a/@href').extract()
    if nexturl: nexturl=response.urljoin(nexturl[0])
    yield scrapy.Request(nexturl, callback=self.parse)
