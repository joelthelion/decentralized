#!/usr/bin/env python

import sql

#param number decorator
def has_param_number(n_params):
    def test_param(func):
        def new_func(params):
            if len(params)>=n_params or n_params<0:
                return func(params)
            else:
                return func.__name__+func.__doc__
        new_func.__name__=func.__name__
        new_func.__doc__=func.__doc__
        return new_func
    return test_param

#commands implementation
#help
@has_param_number(0)
def usage(params):
    """: display commands help"""
    functions={}
    for command,function in commands.items():
        if function in functions:
            functions[function].append(command)
        else:
            functions[function]=[command]
    return '\n'.join([','.join(cmds)+function.__doc__ for function,cmds in functions.items()])

#fetcher oriented command
@has_param_number(0)
def cleartags(params):
    """: clear fetcher tags"""
    if sql.query("truncate table tag"):
        return "tags cleared"

@has_param_number(0)
def clearincoming(params):
    """: Clear incomming table"""
    if sql.query("truncate table incoming_url"):
        return "incoming urls cleared"

@has_param_number(1)
def addtags(params):
    """ tag tag ... : add tags to fetcher"""
    added_tags=0
    for tag in params:
        if sql.query("insert into tag (name,fetched_count) values ('%s',0)" % tag):
            added_tags=added_tags+1
        else:
            return "can't add tag %s..." % tag
    return "added %d tags" % added_tags

@has_param_number(0)
def listtag(params):
    """:list fetcher tag"""
    return 'tags: '+' '.join(sql.tag_list())

#user oriented command
@has_param_number(2)
def adduser(params):
    """ login password: add user to database"""
    login=params[0]
    passwd=params[1]

    if sql.query("insert into kolmognus_user (login,pass) values ('%s',PASSWORD('%s'))" % (login,passwd)):
        return  "user %s added to database" % login  
    else:
        return "can't add user %s..." % login

@has_param_number(1)
def remuser(params):
    """ login: remove user from database"""
    login=params[0]

    if sql.query("delete from kolmognus_user where login='%s'" % login):
        return "user %s removed from database" % login
    else:
        return "can't remove user %s: not in database..." % login
        
@has_param_number(2)
def testlogin(params):
    """ login password: test password for user"""
    login=params[0]
    password=params[1]

    if sql.login_test(login,password):
        return "password ok"
    else:
        return "password err"

@has_param_number(0)
def listuser(params):
    """: list users in database"""
    return "users: "+" ".join(sql.login_list())

@has_param_number(0)
def quit(params):
    """: quit the command line"""
    import sys
    sys.exit()
    return "quitting..."

#commands binding
commands={
    'quit'          : quit,
    'q'             : quit,
    'usage'         : usage,
    'help'          : usage,
    'h'             : usage,

    'listuser'      : listuser,
    'list'          : listuser,
    'ls'            : listuser,
    'adduser'       : adduser,
    'add'           : adduser,
    'remuser'       : remuser,
    'rm'            : remuser,
    'testlogin'     : testlogin,
    'test'          : testlogin,

    'cleartags'     : cleartags,
    'cltags'        : cleartags,
    'addtags'       : addtags,
    'addt'          : addtags,
    'listtags'      : listtag,
    'tags'          : listtag,
        
    'clinc'         : clearincoming,
    'clearincoming' : clearincoming}

#user interface
def get_command():
    while True:
        words=[word for word in raw_input('kolmognus$ ').split(' ') if word]
        if len(words)==1:
            return words[0],[]
        elif len(words)>1:
            return words[0],words[1:]

def main():

    #main loop
    while True:
        try:
            action,params=get_command()
        except EOFError:
            break
        try:
            print commands[action](params)
        except KeyError:
            print "unknow command %s..." % action

if __name__=='__main__':
    main()
