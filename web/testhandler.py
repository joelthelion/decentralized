from mod_python import apache

def handler(req):
    req.content_type='text/plain'
    req.write('hello how are you??')
    return apache.OK
