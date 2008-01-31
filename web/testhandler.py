from mod_python import apache
from web import sql

def handler(req):
    req.content_type='text/plain'

    logins=sql.login_list()
    tags=sql.tag_list()
    services=sql.service_list()

    req.write('kolmognus info:\n')
    req.write('\tusers: '+' '.join(logins)+'\n')
    req.write('\ttags: '+' '.join(tags)+'\n')
    req.write('\nservice:\n')
    req.write('\t'+'\n\t'.join(["%s: %s" % service for service in services])+'\n')
    return apache.OK
