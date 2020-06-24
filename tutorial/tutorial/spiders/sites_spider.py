import scrapy
import os
import re

urls_doc = input('Type the urls doc name with the extension: ')
lista_urls = [i.replace('\n','') for i in open(urls_doc,'r').readlines()]

class QuotesSpider(scrapy.Spider):

    name = "sites"
    start_urls = lista_urls.copy()

    def parse(self, response):
        page = response.css('body')
        #Format (xxx) xxx-xxxx
        telefones = []
        clear_phones = []
        for numb in page:
            ph = numb.re(r'\(\d{1,5}\)[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}')
            telefones.append(ph)

        for i in list(range(0,len(telefones))):
            ks = len(telefones[i])
            for k in list(range(0,ks)):
                l = telefones[i][k].replace('(','').replace(')','').replace('-', ' ').replace('.', ' ')
                clear_phones.append(l)
        non_duplicate_phones = list(dict.fromkeys(clear_phones))
        #Format + xxx [xxx or (xxx)] xxx-xxxx
        telefones2 = []
        clear_phones2 = []
        for numb in page:
            ph2 = page.re(r'\+[\s]??\d{1,3}[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}|\+[\s]??\d{1,3}[-\.\s]??\(\d{1,5}\)[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}')
            telefones2.append(ph2)

        for i in list(range(0,len(telefones2))):
            ks = len(telefones2[i])
            for k in list(range(0,ks)):
                l = telefones2[i][k].replace('(','').replace(')','').replace('-', ' ').replace('.', ' ')
                clear_phones2.append(l)
        non_duplicate_phones2 = list(dict.fromkeys(clear_phones2))
        #Format + xxx [xxx or (xxx)] xxx xx-xx
        telefones3 = []
        clear_phones3 = []
        for numb in page:
            ph2 = page.re(r'\+[\s]??\d{1,3}[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}|\+[\s]??\d{1,3}[-\.\s]??\(\d{1,5}\)[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}[-\.\s]??\d{1,5}')
            telefones3.append(ph2)

        for i in list(range(0,len(telefones3))):
            ks = len(telefones3[i])
            for k in list(range(0,ks)):
                l = telefones3[i][k].replace('(','').replace(')','').replace('-', ' ').replace('.', ' ')
                clear_phones3.append(l)
        non_duplicate_phones3 = list(dict.fromkeys(clear_phones3))

        #Tirando as duplicatas de final_phones, que contem todos os telefones de todos os formatos
        final_phones = non_duplicate_phones.copy() + non_duplicate_phones2.copy()# + non_duplicate_phones3.copy()# + non_duplicate_phones3.copy() + non_duplicate_phones4.copy() + non_duplicate_phones5.copy()
        nova_lista = final_phones.copy()
        for g in list(range(0,len(nova_lista))):
            nova_lista1 = nova_lista.copy()
            k = nova_lista1.pop(g)
            for i in nova_lista1:
                n1 = i
                n2 = k
                n1limpo = n1.replace('(','').replace(')','').replace('-', ' ').replace(' ','').replace('+','').replace('.','')
                n2limpo = n2.replace('(','').replace(')','').replace('-', ' ').replace(' ','').replace('+','').replace('.','')
                if len(n1limpo) > len(n2limpo):
                    dif = len(n1limpo) - len(n2limpo)
                    num_to_compare = n1limpo[dif:len(n1limpo)]
                    if num_to_compare == n2limpo:
                        try:
                            final_phones.remove(n2)
                        except:
                            pass

                elif len(n1limpo) == len(n2limpo):
                    if n1limpo == n2limpo:
                        try:
                            final_phones.remove(n2)
                        except:
                            pass

                else:
                    dif = len(n2limpo) - len(n1limpo)
                    num_to_compare = n2limpo[dif:len(n2limpo)]
                    if num_to_compare == n2limpo:
                        try:
                            final_phones.remove(n1)
                        except:
                            pass

        #Extracting logo
        ext_list = [".png", ".gif", ".jpg", ".tif", ".tiff", ".bmp", ".svg"]
        img_url_list = []
        url_list = []
        case_list = []
        homepage = response.url.split('/')[0] + "//" + response.url.split('/')[2]

        #First Case
        CHECK = False
        for tag_a in response.xpath('//a'):
            for tag_img in tag_a.xpath('.//img'):
                img_url = str(tag_img.xpath('@src').extract()).replace("['", "").replace("']", "")
                if img_url[0] == '/':
                    img_url = homepage + img_url
                else:
                    img_url = str(tag_img.xpath('@src').extract()).replace("['", "").replace("']", "")
                #img_url = self.clean_url(img_url)
                ind = img_url.find('logo')
                if ind > 0:
                    CHECK = True
                    img_url_list.append(img_url)

        #Second Case
        if not CHECK:
            for tag_div in response.xpath('//div'):
                for tag_img in tag_div.xpath('.//img'):
                    img_url = str(tag_img.xpath('@src').extract()).replace("['", "").replace("']", "")
                    if img_url[0] == '/':
                        img_url = homepage + img_url
                    else:
                        img_url = str(tag_img.xpath('@src').extract()).replace("['", "").replace("']", "")
                    ind = img_url.find('logo')
                    if ind > 0:
                        CHECK = True
                        img_url_list.append(img_url)

        #Third Case
        if not CHECK:
            for tag_a in response.xpath('//a'):
                a_href = str(tag_a.xpath('@href').extract()).replace("['", "").replace("']", "").lower()
                if a_href[:6] == str("index.") or a_href == homepage:
                    for tag_img in tag_a.xpath('.//img'):
                        img_url = str(tag_img.xpath('@src').extract()).replace("['", "").replace("']", "")
                        img_name, img_ext = os.path.splitext(img_url)

                        tag_class = str(tag_img.xpath('@class').extract()).lower().strip()
                        title = str(tag_img.xpath('@title').extract()).lower().strip()
                        alt = str(tag_img.xpath('@alt').extract()).lower().strip()

                        if img_ext in ext_list or tag_class.find("logo") > 0 or title.find("logo") > 0 or \
                                        alt.find("logo") > 0:
                            CHECK = True
                            if img_url[0] == '/':
                                img_url = homepage + img_url
                            else:
                                img_url = str(tag_img.xpath('@src').extract()).replace("['", "").replace("']", "")

                            img_url_list.append(img_url)

        yield {
            'logo': img_url_list,
            'phones': final_phones,
            'website': response.url
        }
