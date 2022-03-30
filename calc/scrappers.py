from calc.scrapper_marjane import scrape,scrape_product_name,scrape_from_last
from calc.celery_app import appli

URL="https://www.marjane.ma"
@appli.task
def scrapetask(URL):
    scrape_from_last("https://www.marjane.ma")

@appli.task
def d():
    return 1+1

appli.conf.beat_schedule = {
    'add-every-3-seconds': {
        'task': 'celery_app.d',
        'schedule': 3.0,
    },
}
appli.conf.timezone = 'UTC+1'