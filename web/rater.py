#!/usr/bin/env python

import sql

if __name__ == '__main__':
    rerate_delay=2 #Number of days before a URL is rerated
    stories=sql.request("select url_md5,url,symbols from story where (not isnull(fetch_date)) and (isnull(rated_date) or addtime(rated_date,'%d 00:00:00') < now())" % rerate_delay)
    users=sql.request("select login from kolmognus_user")
    classifiers={}
    for umd5,url,symbols in stories:
        for user in users:
            if not user in classifiers:
                classifiers["user"]=BayesianClassifier(user)
            print user,url
            
        
