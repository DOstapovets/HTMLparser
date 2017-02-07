import csv
import urllib
import urllib2
from lxml import html


class Params:
    def __init__(self, url, selectors, req):
        self.url = url
        self.data = {}
        self.selectors = selectors
        for key, val in req.iteritems():
            self.data[key] = val


class Flat:
    def __init__(self, url, img, address, price, *other):
        self.url = url
        self.img = img
        self.address = address
        self.price = price
        for key, val in other:
            self[key] = val


class Parser:
    def __init__(self, param):
        self.params = param
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }
        self.flats = []

    def getAllFlats(self):
        params = self.params

        while True:

            data = urllib.urlencode(params.data)
            req = urllib2.Request(url=params.url, data=data, headers=self.headers)
            response = urllib2.urlopen(req)

            htm = response.read()
            dom = html.fromstring(htm)

            apart_list = dom.xpath(params.selectors['list'] + params.selectors['item'])

            if not len(apart_list):
                return self.flats
            for item in apart_list:
                f_url = params.url + item.xpath(params.selectors['url'])[0].strip()
                f_img = params.url + item.xpath(params.selectors['img'])[0].strip()
                f_ttl = item.xpath(params.selectors['prc'])[0].strip()
                f_prc = item.xpath(params.selectors['ttl'])[0].strip()
                flat = Flat(url=f_url, img=f_img, address=f_ttl, price=f_prc)
                self.flats.append(flat)
                params.data["start"]+=1

output_file = open("out.csv", "wb")
wr = csv.writer(output_file)

<<<<<<< HEAD
# parameters for site oktv
# selector must be in XPath
req = Params("http://oktv.ua/search", selectors={
    "list": '//div[@class = "ajax-pagination-content"]',
    "item": '//div[@class = "object_v_spiske"]',
    "url": './/div/a/@href',
    "img": './/div//img/@src',
    "prc": './/div[@class = "object_price"]/text()',
    "ttl": './/div[@class = "object_title"]/text()'
}, req={'order_start': "09.02.2017",
        'order_finish': "10.02.2017",
        "start": 0})

Oktv = Parser(req)
oktv_flats = Oktv.getAllFlats()
for flat in oktv_flats:
    wr.writerow([flat.url.encode('raw-unicode-escape'), flat.img.encode('raw-unicode-escape'), flat.address.encode('raw-unicode-escape'),flat.price.encode('raw-unicode-escape')])
=======
page = 0
date_start = datetime.date(2017, 02, 07)
date_finish = (date_start + datetime.timedelta(days=1))
while True:
    values = {'order_start': date_start.strftime("%d.%m.%Y"),
              'order_finish': date_finish.strftime("%d.%m.%Y"),
              'start': page}
    data = urllib.urlencode(values)
    req = urllib2.Request(url=url, data=data, headers=headers)
    response = urllib2.urlopen(req)

    html = response.read()
    soup = BeautifulSoup(html)
    apart_list = soup.find('div', {'class': 'ajax-pagination-content'}).findAll('div', {'class': 'object_v_spiske'})
    if not len(apart_list):
        break
    for item in apart_list:
        apart = []
        apart.append(url+item.find('a').get('href'));
        apart.append(url+item.find('img').get('src'))
        apart.append(''.join(item.find('div', {'class': 'object_price'}).findAll(text=True)).strip())
        apart.append(''.join(item.find('div', {'class': 'object_title'}).findAll(text=True)).strip())
        ul = item.find('ul').findAll('li')
        for li in ul:
            apart.append(''.join(li.findAll(text=True)).strip())
        wr.writerow([unicode(s).encode("utf-8") for s in apart])
    page += 12
output_file.close()
>>>>>>> parent of f5fb163... Structerd
