from scrapy.crawler import CrawlerProcess
# from zywie_pinoy_scraper.spiders.testspider1 import Testspider1Spider
# from zywie_pinoy_scraper.spiders.testspider2 import Testspider2Spider
from zywie_scraper.spiders.pinoy_recipe import PinoyRecipeSpider
from zywie_scraper.spiders.allrecipe import AllrecipeSpider
from zywie_scraper.spiders.eatingwell import EatingwellSpider
from zywie_scraper.spiders.usda import UsdaSpider
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler

process = CrawlerProcess(get_project_settings())
sched = TwistedScheduler()
sched.add_job(process.crawl, 'cron', args=[PinoyRecipeSpider], minute="*", second="59")
sched.add_job(process.crawl, 'cron', args=[AllrecipeSpider], minute="*", second="59")
sched.add_job(process.crawl, 'cron', args=[EatingwellSpider], minute="*", second="59")
sched.add_job(process.crawl, 'cron', args=[UsdaSpider], minute="*", second="59")
sched.start()
process.start(False)
