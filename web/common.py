from mod_python import util,Session
from web import sql
import time

def decode_param_strings(param):
    """This function is needed to decode the utf-8 returned by mod_python"""
    unicode_dict={}
    for f in param.list:
        unicode_dict[f.name.decode('utf-8')]=f.value.decode('utf-8') #there is no way to tell what encoding the user uses
    return unicode_dict

def html_page(header,main,footer,title="kolmognus"):
    template="""<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head><title>%s</title><link rel="stylesheet" href="/css/style.css"/></head><body><div class="header">%s</div><div class="main">%s</div><div class="footer">%s</div></body></html>"""
    return template % (title,header,main,footer)

def html_debug(param,request):
    template="""<div class="debug"><span class="key">parameters:</span> %s<br/><span class="key">uri:</span> %s<br/>generated in %.2fms</div>"""
    valid_template="""<div class="validation"><a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-xhtml11-blue" alt="Valid XHTML 1.1"/></a><a href="http://jigsaw.w3.org/css-validator/validator?uri=http%3A%2F%2Fsd-12155.dedibox.fr%3A8080%2Fcss%2Fstyle.css"><img src="http://www.w3.org/Icons/valid-css-blue" alt="Valid CSS!"/></a></div>"""
    formatted_param=' '.join(param.keys())
    return valid_template + template % (formatted_param,request.uri,1000*(time.time()-request.request_time))

def html_menu():
    menus=[
        ('/',"home"),
	('/feed',"feed"),
	('/story',"story"),
        ('/mp-info',"modpython")
    ]
    template="""<div class="menu"><a href="/"><img src="/image/logo.png" alt="KolmoGNUS"/></a><p>%s</p></div>"""
    menu_template="""<a href="%s">%s</a>"""
    return template % ' '.join([menu_template % (menu[0],menu[1].upper()) for menu in menus])

def html_session(param,request):
    template="""<div class="session">%s<p>%s</p></div>"""
    form_template="""<form action="" method="post"><p><input name="login" type="text" value="login" tabindex="1" onfocus="value=''"/><input name="passwd" type="password" value="****" tabindex="2" onfocus="value=''"/><input type="submit" value="go!!"/><input name="login_hidden" type="hidden"/></p></form>"""
    logged_template="""<p>Welcome %s!! <a href="?logout">logout</a></p>"""

    session=Session.Session(request,timeout=60)
    if param.has_key('logout'):
        session.invalidate()
        util.redirect(request,'/')
        return template % (form_template,'bye!!')
    if param.has_key('login_hidden') and param.has_key('login') and param.has_key('passwd'):
        login=param['login']
        passwd=param['passwd']
        if sql.request("select id from kolmognus_user where login=%s and pass=PASSWORD(%s)" , (login,passwd)):
            session['login']=login
            session['hits']=0
            session.save()
            return template % (logged_template % session['login'],"%d hits" % session['hits'])
        else:
            return template % (form_template,"bad login")
    elif not session.is_new():
        session['hits']+=1
        session.save()
        return template % (logged_template % session['login'],"%d hits" % session['hits'])
    else:
        session.invalidate()
        return template % (form_template,"please login")

