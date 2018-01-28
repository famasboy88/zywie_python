# -*- coding: utf-8 -*-
import scrapy
import firebase_admin
from firebase_admin import db

class EatingwellSpider(scrapy.Spider):
    name = 'eatingwell'
    allowed_domains = ['eatingwell.com']
    start_urls = ['http://www.eatingwell.com/recipes/17965/main-dishes/']

    def parse(self, response):
        food_list = db.reference().child("food_title").get()
        print("This is from Eating Well");
    #     for x in range(1, 20):
    #         link = "http://www.eatingwell.com/recipes/17965/main-dishes/?page=" + str(x)
    #         link = response.urljoin(link)
    #         yield scrapy.Request(link, callback=self.getFoodLink)
    #
    # def getFoodLink(self, response):
    #     links = response.css('article.gridCol--fixed-tiles > a::attr(href)').extract()
    #     for link in links:
    #         if(link is not None):
    #             link = response.urljoin(link)
    #             yield scrapy.Request(link, callback=self.getFoodDetails)
    #
    # def getFoodDetails(self, response):
    #     name_food = response.css('div.recipeDetailSummaryDetails > h3.recipeDetailHeader::text').extract_first()
    #     list_recipe = response.css('ul.multiColumn > li.checkListListItem > span::text').extract()
    #     description = response.css('div.recipeSubmitter > p::text').extract_first()
    #     if(description is not None):
    #         description = description.replace('\r\n                    ', '')
    #         description = description.replace('\r\n', '')
    #     photo_url = response.css('img.recipeDetailSummaryImageMain::attr(src)').extract_first()
    #     if(photo_url is None):
    #         photo_url = "http://images.media-allrecipes.com/global/recipes/nophoto/nopicture-910x511.png"
    #     procedure = response.css('ol.recipeDirectionsList > li > span::text').extract()
    #     prep_time = response.css('time > span::text').extract_first()
    #     if(prep_time is None):
    #         prep_time = "N/A"
    #     db.reference().child('food_title').child(name_food).update({
    #         'category_id': 'Healthy Main Dishes',
    #         'link': response.url,
    #         'name_food': name_food,
    #         'list_recipe': list_recipe,
    #         'description': description,
    #         'photo_url': photo_url,
    #         'procedure': procedure,
    #         'prep_time': prep_time
    #     })
