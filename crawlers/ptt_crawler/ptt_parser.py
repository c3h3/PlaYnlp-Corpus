'''
Created on Feb 3, 2014

@author: c3h3
'''


import requests
from pyquery import PyQuery
import re

import lxml 


gen_ptt_board_page_url = lambda b_name: "http://www.ptt.cc/bbs/%s/index.html" % b_name


def get_ptt_article_url_lists(one_ptt_url):
    res = requests.get(one_ptt_url)
    S = PyQuery(res.text)
    _article_urls = S(".title a").map(lambda :PyQuery(this).attr("href"))
    article_urls = ["http://www.ptt.cc%s" % one_url for one_url in _article_urls if one_url.startswith("/bbs")]
    return article_urls

def get_max_pages(one_ptt_board_url):
    res = requests.get(one_ptt_board_url)
    S = PyQuery(res.text)
    return int(PyQuery(S("div.btn-group.pull-right > a")[1]).attr("href").split("index")[1].split(".")[0])


def get_all_pages_url(one_ptt_board_url):
    max_n = get_max_pages(one_ptt_board_url)
    url_head = one_ptt_board_url.split("index")[0]
    all_urls = [ url_head + "index%s.html" % ii for ii in [""] + range(max_n)]
    return all_urls



def get_one_article_meta_data(one_article_url):
    one_article_res = requests.get(one_article_url)
    SS = PyQuery(one_article_res.text)
    one_article_data = {}
    one_article_data["Board"] = SS(".article-metaline-right > .article-meta-value").text()
    one_article_data.update(dict(zip(["user","title","time"],SS(".article-metaline > .article-meta-value").map(lambda :PyQuery(this).text()))))
    author_meta = re.search(r"(?P<user_id>\S+)\s(?P<user_nickname>\S+)",one_article_data['user'])
    one_article_data.update(author_meta.groupdict())
    one_article_data["user_nickname"] = one_article_data["user_nickname"][1:-1]
    
    SS("#main-content > div.article-metaline").remove()
    SS("#main-content > div.article-metaline-right").remove()
    one_article_data["text"] = "".join(map(lambda xx:PyQuery(xx).text() if isinstance(xx,lxml.html.HtmlElement) else xx,
                                           SS("#main-content").contents()))
    one_article_data["url"] = one_article_res.url
    
    push_meta_data = SS("div.push").map(lambda:{"tag":PyQuery(this)(".push-tag").text(),
                                                "userid":PyQuery(this)(".push-userid").text(),
                                                "content":PyQuery(this)(".push-content").text(),
                                                "datetime":PyQuery(this)(".push-ipdatetime").text(),
                                                "url": one_article_res.url
                                                })
    return_dict = {}
    return_dict["article_data"] = one_article_data
    return_dict["push_data"] = push_meta_data
    
    
    return return_dict

if __name__ == '__main__':
    pass


    board_name = "R_Language"

    r_lang_url = gen_ptt_board_page_url(board_name)
    print r_lang_url
    
    print get_ptt_article_url_lists("http://www.ptt.cc/bbs/BuyTogether/index.html")
    print get_max_pages("http://www.ptt.cc/bbs/BuyTogether/index.html")
    print get_all_pages_url("http://www.ptt.cc/bbs/BuyTogether/index.html")
    
    res = requests.get(r_lang_url)
    S = PyQuery(res.text)

    _article_urls = S(".title a").map(lambda :PyQuery(this).attr("href"))
    article_urls = ["http://www.ptt.cc%s" % one_url for one_url in _article_urls if one_url.startswith("/bbs")]
    
    print get_one_article_meta_data(article_urls[3])