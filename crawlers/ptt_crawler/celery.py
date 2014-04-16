'''
Created on Oct 31, 2013

@author: c3h3
'''

from __future__ import absolute_import

from celery import Celery

celery = Celery('ptt_crawler.celery',
                broker='amqp://',
                backend="mongodb://localhost:27017/ptt_crawler_backend",
                include=['ptt_crawler.tasks'])



if __name__ == '__main__':
    celery.start()
