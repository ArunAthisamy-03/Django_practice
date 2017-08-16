import httplib, urllib, base64

def LuisGetIntent(questions):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b80fbddec8b74d2685df91ac6eac2125',
    }

    params = urllib.urlencode({
        # Request parameters
        'timezoneOffset': '0',
        'verbose': 'true',
        'spellCheck': 'true',
        'staging': 'true',
    })

    try:
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("GET", "/luis/v2.0/apps/4346869a-e0ff-4a7b-b114-3bf5c02f26cd?q={q}&%s" % params, questions, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
