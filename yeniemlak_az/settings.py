import scrapy.downloadermiddlewares.retry
from scrapy.downloadermiddlewares.retry import RetryMiddleware

BOT_NAME = "yeniemlak_az"

SPIDER_MODULES = ["yeniemlak_az.spiders"]
NEWSPIDER_MODULE = "yeniemlak_az.spiders"

ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'yeniemlak_az.middlewares.TooManyRequestsRetryMiddleware': 543,

}

CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 1

CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    'data.json': {
        'format': 'json',
        'overwrite': True,
    },
}

# HTTPERROR_ALLOWED_CODES  =[404,429]

COOKIES_ENABLED = True
USER_AGENT_ROTATION_ENABLED = True
RETRY_HTTP_CODES = [429, 503]
RETRY_TIMES = 5
DOWNLOAD_TIMEOUT = 15
