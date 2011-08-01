import simplejson, urllib
apikey = "{발급 받은 키를 입력하세요.}"
SEARCH_BASE ="http://apis.daum.net/search/knowledge"

def search(query, **args):
    args.update({
            'apikey': apikey,
            'q': query,
            'output': 'json'
    })

    url = SEARCH_BASE + '?' + urllib.urlencode(args)
    result = simplejson.load(urllib.urlopen(url))

    return result['channel']

info = search('OpenAPI')
for item in info['item']:
    print item['title']
