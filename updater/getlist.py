#!/usr/bin/env python

import urllib
import lxml.html as lh

baseurl='https://www.idealista.com'
start_url='https://www.idealista.com/alquiler-viviendas/madrid/chamberi/'

loadpage=lambda url:lh.parse(urllib.urlopen(url))
nextpage=lambda page: baseurl+page.xpath('//*[@class="next"]/a/@href')[0]
allflats=lambda page: [baseurl+i for i in page.xpath("//a/@href") if "/inmueble/" in i]

pg=loadpage(start_url)

while 1:
  try:
    print "\n".join(allflats(pg))
    pg=loadpage(nextpage(pg))
  except IndexError:
    break

