import simplejson, urllib
apikey = "{발급 받은 키를 입력하세요.}"
SEARCH_BASE ="http://apis.daum.net/search/knowledge"

def search(query, **args):
    args.update({
            'apikey': apikey,
            'q': query,
            'output': 'json'
    })

    #호출할 url을 만든다
    url = SEARCH_BASE + '?' + urllib.urlencode(args)
    
    #json으로 응답을 받는다.
    result = simplejson.load(urllib.urlopen(url))

    return result['channel']

info = search('OpenAPI')
for item in info['item']:
    print item['title']
