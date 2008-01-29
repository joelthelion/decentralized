from mod_python import apache
from web import sql

def handler(req):
    req.content_type='text/plain'
    req.write('hello how are you??\n')
    db=sql.connect_db()
    logins=sql.login_list(db)
    req.write(' '.join(logins)+'\n')
    req.write('bye!!\n')
    return apache.OK
