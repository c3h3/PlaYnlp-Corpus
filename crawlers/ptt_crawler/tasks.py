'''
Created on Feb 3, 2014

@author: c3h3
'''

from __future__ import absolute_import

from ptt_crawler.celery import celery

from pymongo import MongoClient
mongo_client = MongoClient()
ptt_crawler_db = mongo_client.ptt_crawler_db
ptt_article = ptt_crawler_db.ptt_article
ptt_article_push = ptt_crawler_db.ptt_article_push

from ptt_crawler import ptt_parser 


@celery.task(rate_limit = "180/m",ignore_result = True, max_retries = 20, queue = "ptt_posts")
def get_data_from_article_page(one_article_url, updating=False):
#    print "[in get_data_from_article_page]"
    
    
    try:
#        print "[in get_data_from_article_page][try area]"
#        print "[in get_data_from_article_page][try area] updating",updating
#        pass
        if updating:
#            print "[in get_data_from_article_page][try area][updating]"
            
            result_dict = ptt_parser.get_one_article_meta_data(one_article_url)
            ptt_article.insert(result_dict["article_data"])
            ptt_article_push.insert(result_dict["push_data"])
            
            print "[updating] one_article_url = ",one_article_url
            
        else:
            
#            print "[in get_data_from_article_page][try area][not updating]"
            
            checking_db = ptt_article.find({"url":one_article_url}).count()
#            print "[in get_data_from_article_page][try area][not updating] checking_db =",checking_db
            
            if checking_db > 0:
                pass
            else:
#                print "[in get_data_from_article_page][try area][new_data]"
                
                result_dict = ptt_parser.get_one_article_meta_data(one_article_url)
                ptt_article.insert(result_dict["article_data"])
                ptt_article_push.insert(result_dict["push_data"])
                print "[new_data] one_article_url = ",one_article_url
                
                
    
    except Exception as e:
        # FIXME: Cannot Retry ...... 
        raise get_data_from_article_page.retry(exc=e, countdown=10)


@celery.task(rate_limit = "60/m",ignore_result = True, max_retries = 20, queue = "ptt_pages")
def parse_article_list_page(one_ptt_url):
    try:
#        pass
        result_urls = ptt_parser.get_ptt_article_url_lists(one_ptt_url)
        for one_article_url in result_urls:
            print "one_article_url = ",one_article_url
            get_data_from_article_page.apply_async(kwargs = {"one_article_url":one_article_url})
        
    except Exception as e:
        # FIXME: Cannot Retry ...... 
        raise parse_article_list_page.retry(exc=e, countdown=10)



@celery.task(ignore_result = True, max_retries = 20, queue = "ptt_pages")
def submit_all_subpages_of_a_board(board_name):
    try:
#        pass
        board_url = ptt_parser.gen_ptt_board_page_url(board_name)
        all_article_pages_list = ptt_parser.get_all_pages_url(board_url)
        
        for one_article_list_page_url in all_article_pages_list:
            print "one_article_list_page_url = ",one_article_list_page_url
            parse_article_list_page.apply_async(kwargs = {"one_ptt_url":one_article_list_page_url})
        
    except Exception as e:
        # FIXME: Cannot Retry ...... 
        raise submit_all_subpages_of_a_board.retry(exc=e, countdown=10)




if __name__ == '__main__':
    pass
