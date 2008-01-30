from mod_python import apache
from web import sql

def handler(req):
    db=sql.connect_db()
    req.content_type='text/plain'

    logins=sql.login_list(db)
    tags=sql.tag_list(db)
    services=sql.service_list(db)

    req.write('kolmognus info:\n')
    req.write('\tusers: '+' '.join(logins)+'\n')
    req.write('\ttags: '+' '.join(tags)+'\n')
    req.write('\nservice:\n')
    req.write('\t'+'\n\t'.join(["%s: %s" % service for service in services])+'\n')
    return apache.OK
