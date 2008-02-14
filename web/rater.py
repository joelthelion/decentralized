#!/usr/bin/env python

import sql
import classifier

if __name__ == '__main__':
    rerate_delay=2 #Number of days before a URL is rerated
    stories=sql.request("select id,url_md5,url,symbols from story where (not isnull(fetch_date)) and (isnull(rated_date) or addtime(rated_date,'%s 00:00:00') < now())" , rerate_delay)
    users=sql.request("select id,login from kolmognus_user")
    classifiers={}
    for user_id,login in users: #rate stories for each user
        if not user_id in classifiers:
            classifiers[user_id]=classifier.BayesianClassifier(user_id)
            #classifiers[user_id]=classifier.DumbClassifier()
        classif=classifiers[user_id]
        for url_id,umd5,url,symbols in stories:
            sql.query("insert into recommended_story (user_id,story_id,computed_rating)\
                values(%s,%s,%s)",(user_id,url_id,classif.rate(symbols.split())))

    for url_id,umd5,url,symbols in stories: #mark stories as rated
        print url_id
        sql.query("update story set rated_date=now() where id=%s;",url_id)
