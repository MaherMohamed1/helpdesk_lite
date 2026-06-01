import urllib.request

paths = ['/', '/login', '/signup', '/tickets', '/submit']
for p in paths:
    try:
        r = urllib.request.urlopen('http://127.0.0.1:8000' + p)
        print(p, r.getcode())
    except Exception as e:
        print(p, 'ERROR', e)
