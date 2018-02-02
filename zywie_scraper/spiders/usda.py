# -*- coding: utf-8 -*-
import scrapy
import firebase_admin
from firebase_admin import db
import re


class UsdaSpider(scrapy.Spider):
    name = 'usda'
    allowed_domains = ['googleapis.com']
    start_urls = ['https://api.nal.usda.gov/ndb/search/?format=xml&offset=0&sort=r&q=carrot&ds=Standard%20Reference&fg=Vegetables%20and%20Vegetable%20Products&api_key=fCaQFZDctF3YHA85VzFd4eHphM9GukBUWFJh2Uld']

    rootDB = db.reference()
    food_list = db.reference().child("food_title").get()

    def parse(self, response):
        rootDB = db.reference()
        ref_food_exchange = rootDB.child('food_exchange_list_tag').get()
        for key, food_item in ref_food_exchange.items():
            for value in food_item:
                link = "https://api.nal.usda.gov/ndb/search/?format=xml&offset=0&sort=r&q="+value+"&ds=Standard%20Reference&api_key=fCaQFZDctF3YHA85VzFd4eHphM9GukBUWFJh2Uld"
                link = response.urljoin(link)
                request = scrapy.Request(link, callback=self.getSearch, dont_filter=True)
                request.meta['exchange_category'] = key
                request.meta['food_item'] = value
                yield request
                print(value)

    def getSearch(self, response):
        ndbno = response.xpath('//item/ndbno/text()').extract_first()
        if(ndbno != None):
            link = "https://api.nal.usda.gov/ndb/reports?ndbno="+ndbno+"&type=b&format=xml&api_key=fCaQFZDctF3YHA85VzFd4eHphM9GukBUWFJh2Uld"
            link = response.urljoin(link)
            request = scrapy.Request(link, callback=self.getDetail, dont_filter=True)
            request.meta['exchange_category'] = response.meta['exchange_category']
            request.meta['food_item'] = response.meta['food_item']
            yield request
        else:
            return

    def getDetail(self, response):
        cnt = 0
        for food_key, food_details in self.food_list.items():
            list_recipe = food_details.get("list_recipe")
            if(list_recipe is not None):
                r = re.compile("\\b" + response.meta['food_item'] + "\\b", re.IGNORECASE)
                result = filter(r.search, list_recipe)
                if (list(result)):
                    cnt+=1
                    description = food_details.get("description")
                    photo_url = food_details.get("photo_url")
                    if(photo_url is None):
                        photo_url = "http://images.media-allrecipes.com/global/recipes/nophoto/nopicture-910x511.png"
                    proximity = response.xpath('//nutrient[@group="Proximates"]/@name').extract()
                    measurement = response.xpath('//nutrient[@name="Energy"]/measures/measure/@label').extract()
                    usda_kcal = response.xpath('//nutrient[@name="Energy"]/@value').extract_first()
                    usda_value_grams = response.xpath('//nutrient[@name="Energy"]/measures/measure/@qty').extract_first()
                    if(measurement is not None):
                        for measure in measurement:
                            eqv = response.xpath('//nutrient[@name="Energy"]/measures/measure[@label="'+measure+'"]/@eqv').extract_first()
                            qty = response.xpath('//nutrient[@name="Energy"]/measures/measure[@label="'+measure+'"]/@qty').extract_first()
                            value = response.xpath('//nutrient[@name="Energy"]/measures/measure[@label="'+measure+'"]/@value').extract_first()

                            eunit = response.xpath('//nutrient[@name="Energy"]/measures/measure[@label="'+measure+'"]/@eunit').extract_first()
                            measure = measure.replace('/','_S')
                            db.reference().child("usda_food_measurement").child(response.meta['food_item']).child(measure).update({
                                'eqv': float(eqv),
                                'qty': float(qty),
                                'value': float(value),
                                'eunit': eunit
                            })
                    if(proximity is not None):
                        for proxi in proximity:
                            unit = response.xpath('//nutrient[@name="'+proxi+'"]/@unit').extract_first()
                            value = response.xpath('//nutrient[@name="'+proxi+'"]/@value').extract_first()
                            db.reference().child('usda_food_exchange_nutrients').child(response.meta['exchange_category']).child(response.meta['food_item']).child(proxi).update({
                                'unit': unit,
                                'value': float(value)
                            })

                    db.reference().child("foodex_usda").child(response.meta['exchange_category']).child(response.meta['food_item']).update({
                        "kcal": float(usda_kcal),
                        "value_grams": float(usda_value_grams),
                        "no_food_items": cnt
                    })

                    db.reference().child("food_each_category").child(response.meta['exchange_category']).child(response.meta['food_item']).child(food_key).update({
                        "list_recipe": list_recipe,
                        "photo_url": photo_url,
                        "description": description
                    })
