# -*- coding: utf-8 -*-
import scrapy
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class AllrecipeSpider(scrapy.Spider):
    name = 'allrecipe'
    allowed_domains = ['allrecipes.com']
    start_urls = ['http://allrecipes.com/recipes/84/healthy-recipes']

    def parse(self, response):
        for x in range(1, 216):
            link = "http://allrecipes.com/recipes/84/healthy-recipes/?page=" + str(x)
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.getFoodLink)

    def getFoodLink(self, response):
        links = response.xpath('//article[@class="fixed-recipe-card"]/div[@class="fixed-recipe-card__info"]/h3[@class="fixed-recipe-card__h3"]/a[@class="fixed-recipe-card__title-link"]/@href').extract()
        for link in links:
            if(link is not None):
                link = response.urljoin(link)
                yield scrapy.Request(link, callback=self.getFoodDetails)

    def getFoodDetails(self, response):
        name_food = response.xpath('//div[@class="summary-background"]/div[contains(@class, "summaryGroup")]/section[contains(@class, "recipe-summary")]/h1/text()').extract_first()
        list_recipe = response.xpath('//ul[contains(@class, "checklist dropdownwrapper")]/li[@class="checkList__line"]/label/span/text()').extract()
        list_recipe.pop()
        description = response.xpath('//div[@class="summary-background"]/div[contains(@class, "summaryGroup")]/section[contains(@class, "recipe-summary")]/div[@class="submitter"]/div[@class="submitter__description"]/text()').extract_first()
        if(description is not None):
            description = description.replace('\r\n\"', '')
            description = description.replace('\"        ', '')
        photo_url = response.css('img.rec-photo::attr(src)').extract_first()
        procedure = response.css('div.directions--section__steps > ol > li ::text').extract()
        prep_time = response.css('span.prepTime__item--time::text').extract_first()
        if(prep_time is None):
            prep_time = "N/A"
        db.reference().child('food_title').child(name_food).update({
            'category_id': 'Healthy Food',
            'link': response.url,
            'name_food': name_food,
            'list_recipe': list_recipe,
            'description': description,
            'photo_url': photo_url,
            'procedure': procedure,
            'prep_time': prep_time
        })
