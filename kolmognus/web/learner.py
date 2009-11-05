#!/usr/bin/env python

import sql
import time

def increment(dic,user_id,symbol):
    if not dic.has_key(user_id): dic[user_id]={}
    try:
        dic[user_id][symbol]+=1
    except KeyError : dic[user_id][symbol]=1

if __name__=='__main__':
    goods={}
    bads={}
    all_symbols=set()
    all_users=set()
    all_stories=set()
    learned=[]
    header_printed=False
    for user_id,story_id,user_rating,symbols in sql.request("select user_id,story_id,user_rating,symbols from recommended_story,story \
            where id=story_id and user_rating != '?' and isnull(learned)"):
        if not header_printed:
            print "INFO: (%s) :"%time.asctime(),
            header_printed=True
        print ".",
        all_users.add(user_id)
        learned.append((user_id,story_id))
        for s in symbols.split():
            all_symbols.add(s)
            if user_rating=='G':
                increment(goods,user_id,s)
            else:
                increment(bads,user_id,s)
    for user in all_users:
        for s in all_symbols:
            g_inc,b_inc=(goods.get(user,{}).get(s,0),bads.get(user,{}).get(s,0))
            if b_inc!=0 or g_inc!=0:
                sql.request("insert into bayes_data values (%s,%s,%s,%s)\
                    on duplicate key update\
                    good_count=good_count+%s, bad_count=bad_count+%s",(user,s,g_inc,b_inc,g_inc,b_inc))
    for recom in learned:
        sql.query("update recommended_story set learned=1 where user_id=%s and story_id=%s",recom)


    sql.db.close()
