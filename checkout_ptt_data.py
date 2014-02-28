'''
Created on Feb 28, 2014

@author: c3h3
'''


import sys

#print sys.argv
#print type(sys.argv)
#print len(sys.argv)

OUTPUT_FILE_PREFIX = "PTT___"

if len(sys.argv) > 1:
    board_name = str(sys.argv[1])
    print "Hello argv[1]! %s!" % board_name
    
    board_name_list = board_name.split(",")
    print "board_name_list = ",board_name_list
    
    from pymongo import MongoClient
    mongo_client = MongoClient()
    ptt_crawler_db = mongo_client.ptt_crawler_db
    ptt_article = ptt_crawler_db.ptt_article
    ptt_article_push = ptt_crawler_db.ptt_article_push
    
    import pandas as pd 
    articles_df = pd.DataFrame(list(ptt_article.find({"Board":{"$in":board_name_list}})))
    
    print "articles_df.head() = "
    print articles_df.head()
    print "articles_df.shape = ",articles_df.shape
    
    if articles_df.shape[0] > 0:

        articles_push_df = pd.DataFrame(list(ptt_article_push.find({"url":{"$in":list(articles_df["url"])}})))
        
        import pickle
        
        output_pickle_filename = OUTPUT_FILE_PREFIX + "_".join(board_name_list) + ".pickle"
        with open(output_pickle_filename,"wb") as output_pickle_file:
            pickle.dump((articles_df,articles_push_df),output_pickle_file)
            
        output_tar_filename = OUTPUT_FILE_PREFIX + "_".join(board_name_list) + ".tar.gz"
        import tarfile
        tar = tarfile.open(output_tar_filename, "w:gz")
        tar.add(output_pickle_filename)
        tar.close()
    else:
        print "There is no data in: ",board_name_list
    
else:
    print "Please Input Board Name ... "







