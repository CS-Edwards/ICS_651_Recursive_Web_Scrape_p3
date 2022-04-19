'''
Created on Apr 9, 2022
@author: CS-Edwards
ICS-651 - Comp Networks Project 3
'''

import validators
import requests
import sys
from sys import argv
from bs4 import BeautifulSoup
#from pickle import TRUE
from lxml import etree

global rec_urls_list

global url_list
url_list = []

global count_list
count_list = []

global error_list
error_list = []

# args() terminates program for invalid (too few) command line entries
def args():
    arg_len = len(sys.argv)
    print(arg_len)
    
    if arg_len < 3:
        print("Too few command line arguments; terminating program")
        quit()

###RECURSIVE IMPLEMENTATION## TESTED IN SANDBOX
def append_to_url_list(build_rec,url):
    #if build starts with http:// , check starts with orig url -->append
    #e-if build starts with https:// , check starts with orig url -->append
    #e-if build starts with / --> add to root url, check url list, --> append
    #else add /xyz --> if does not contain . #invalid dont append
    if build_rec.startswith("http://"):
        print('**http**')
    
        if (build_rec not in rec_urls_list) and (build_rec.startswith(url)):
            rec_urls_list.append(build_rec)
            ##CALL RECURSSION
            rec_scrape(build_rec)
            
        else:
            #print(build_rec +' not added to url list -- either already in list or not below')
            print((build_rec + ' already in list') if build_rec in rec_urls_list else (build_rec + ' not hierarchically below target url'))
        
    
    elif build_rec.startswith("https://"):
        print('**https**')
        print(build_rec)
        
        if (build_rec not in rec_urls_list) and (build_rec.startswith(url)):
            rec_urls_list.append(build_rec)
            #CALL RECURSSION
            rec_scrape(build_rec)
            
        else:
            #print(build_rec +' not added to url list -- either already in list or not below')
            print((build_rec + ' already in list') if build_rec in rec_urls_list else (build_rec + ' not hierarchically below target url'))
        

    elif build_rec.startswith("/"):
        print('**starts with /**')
        print(build_rec)
        r_url = url+build_rec
        print(r_url)
            
        if (r_url not in rec_urls_list) and (r_url.find('.') != -1):
            rec_urls_list.append(r_url)
            #CALL RECURSSION
            rec_scrape(r_url)
        else:
            print((r_url + ' already in list') if r_url in rec_urls_list else (r_url + ' does not contain file extension'))
        
    else:
        print("other scenario")
        print(build_rec)
        
        
        r_url='/' #add slash
        r_url= r_url+build_rec #append build_rec
        print(r_url)
        
        if r_url.find('.') != -1: #syntax for file extension
            r_url=url+r_url
            print(r_url)
        
        
            if (r_url not in rec_urls_list):
                rec_urls_list.append(r_url)
                #CALL RECURSSION
                rec_scrape(r_url)
        else:
            print((r_url + ' already in list') if r_url in rec_urls_list else (r_url + ' does not contain file extension'))
        
        
        
        
    

    print('End append_func')

def rec_scrape(url):
    
    if url.endswith('/'):
        url=url[:-1] #remove /
        
    
    if url not in rec_urls_list:
        rec_urls_list.append(url)
    
    
    
    
   
    request = requests.get(url)
    
    print('print status_code')
    print(request.status_code)
    
    if request.status_code != 200: 
        print('****BAD STATUS***')
        
        try:
            rec_urls_list.remove(url)
        except Exception as e:
            error_list.append(e)
        
        return #get out of this itr of function
        
    html_source=request.text #convert to text *anoint
    
    #FOR TESTING
    #html_source=test_html_source
    
    
    src='src=\"'
    href = 'href=\"'
    itr = 0

    for i in str(html_source).split(' '):
        build_src=''
        build_href=''
    
    #print(i)
        if src in i:
            print('**found_src***')
            print(itr)
            build_src = build_src + str(html_source).split(' ')[itr]
            print(str(html_source).split(' ')[itr])
        
            print('build_src')
            build_src = build_src.split('"')[1::2]
            build_src=build_src[0] #get string out of list
            print(build_src)
            append_to_url_list(build_src, url)
        
        ##append to url function; call recursion
        
        if href in i:
            print('**found_href***')
            print(itr)
            build_href = build_href + str(html_source).split(' ')[itr]
            print(str(html_source).split(' ')[itr])
        
            print('build_href')
            build_href = build_href.split('"')[1::2]
            print(build_href)
            build_href=build_href[0] #get string out of list
            print(build_href)
        
        ##append to url function; call recursion
        #url = 'https://test.site'
            append_to_url_list(build_href, url)
            
        itr=itr+1
### end -RECURSIVE IMPLEMENTATION## TESTED IN SANDBOX

# rec() checks if request is recursive     
def rec():
    for a in sys.argv:
        if a == '-r':
            return True
    return False
        


def recSearch(str_search):
    print("**Recurssive Search - to be implemented**")
    
    for u in url_list:
        rec_scrape(u) #adds all recursive urls to rec_url_list

    find_web_rec(str_search)

def parse_url(url):
    # if valid append to url_list
    v = validators.url(url)  # #iftime own validation method with a stack
    if v:
        url_list.append(url)
        
    print(v) 
    
      
# ends program if all URLs are invalid
def invalid_url(url_list):
    if len(url_list) == 0:
        print("No valid URLs Entered; terminating program")
        quit()
    
    else:
        print(str(len(url_list)) + " valid url(s) found ..proceeding to get:")
    
# scan_argv scans argv for valid urls   
def scan_argv():
        
    for a in sys.argv:
        parse_url(a)
       
    # print(len(url_list))
    invalid_url(url_list)
    
    return sys.argv[1]  # string to search

def find_web_rec(str_search): 
    for a in rec_urls_list:
        drive_url(a,str_search)
       
def find_web(str_search):
    for a in url_list:
        print(a)
        drive_url(a, str_search)
    
def find_str(page_parse, str_search):
    html_str = str(page_parse).split(' ')  # html as text delimited by space
    counter = 0
    
    for i in html_str:
        try:
            print(i)
        except Exception as e:
            print(i.encode())
            error_list.append(e)
            
        if str_search in i:
            counter = counter + 1
    
    count_list.append(counter)
    
    print("count_list: ")
    print(count_list)
    
def drive_url(url, str_search):
    print("drive url --in prog")
    
    # ##get request
    page = requests.get(url)
    # print(page.status_code) ##if code == 200; successful get request else return
    if page.status_code != 200:
        print("get_req failed")
        print("status code: " + str(page.status_code))
        return  # to end function
    else:
        print("***successful get")
        print("status code: " + str(page.status_code))
    
    # ##parse html with BeautifulSoup
    print("parse page")
    page_parse = BeautifulSoup(page.text, 'html.parser')
    
    
    # ##check content type in meta
    print("**content type**")
    if not content_type(page, page_parse,url):
        print("Content type not text/html; terminating search in " + url)
        return 
    
    ####if{recursive search/find str()} else go to find_str() below
    ####find string
    find_str(page_parse, str_search)
    ##test with https://www.ics.hawaii.edu/ [[[FAILED]]]#########################################################
    pass

def content_type(page, page_parse,url): 
    print("content type -- in prog") 
    tag = page_parse.meta
    print(tag)

    if(con_type_html(tag) or con_type_http(url)):
        print("content type -- True") 
        return True
    else:
        print("content type -- False") 
        return False
     
def con_type_http(url): 
       headers = {'Content-Type': 'text/html/ charset=UTF-8'}
       page =requests.get(url,headers=headers)
       try:
        print(page.request.headers['Content-Type'])
        
        if page.request.headers['Content-Type'] == 'text/html/ charset=UTF-8':
            print("content type -pass")
            return True
            # works for project html, git hub, 
            
       except Exception as e:
            print(e)
            error_list.append(e)
            return False

def con_type_html(tag):
    
    try:
        t = str(tag.get('content'))
        t = t.split(';')
        print(t)

        for a in t:
            if a == 'text/html':
                    print("content_type_html: true*************")
                    print("content=text/html...continue scrape")
                    return True
        
        print("content_type_html: false*************")
        return False    
    
    except Exception as e:
        print(e)
        error_list.append(e) 
        return False    


if __name__ == '__main__':
        
    print("running main")
    args()
    str_search = scan_argv()  # str_search string to search on web pages
    r_flag = rec()  # recusive flag
    
    
     
    if r_flag:
        rec_urls_list=[]
        recSearch(str_search)
        
        i = 0
        print('**Final Output**')
        while(i < len(count_list)):
            print(str(count_list[i]) + " " + str(rec_urls_list[i]))
            i = i + 1
    
    else:
        find_web(str_search) 
        i = 0
        print('**Final Output**')
        while(i < len(count_list)):
            print(str(count_list[i]) + " " + str(url_list[i]))
            i = i + 1
    
    print("r_flag: ")
    print(rec())
    

    
 
