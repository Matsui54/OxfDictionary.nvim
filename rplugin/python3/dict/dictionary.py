import requests
import json


class OxfordDict:
    base_url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/'

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.fields = 'definitions'
        self.strictMatch = 'false'
        self.language = 'en-us'

    def get_definition(self, word_id):
        url = self.base_url + self.language + '/' + word_id.lower() + '?fields=' + self.fields + '&strictMatch=' + self.strictMatch;

        r = requests.get(url, headers = {'app_id': self.app_id, 'app_key': self.app_key})

        if r.status_code == 200:
            json_load=json.loads(r.text)
        elif r.status_code == 404:
            return 'No definition found', -1
        else:
            return 'Internal error', -1

        '''
        #test____________________________
        json_open = open('ace.json', 'r')
        json_load = json.load(json_open)
        #end test________________________
        '''

        definitions = []
        cntcol=0
        max_width = 10
        for jresult in json_load['results']:
            for jle in jresult['lexicalEntries']:
                lCategory = jle['lexicalCategory']['text']
                definitions.append(lCategory)
                cntcol+=1
                for ent in jle['entries']:
                    for sen in ent['senses']:
                        for defn in sen['definitions']:
                            definitions.append('- '+defn)
                            cntcol+=1
                            max_width = max(max_width, min(len(defn)+2, 101))
                            if len(defn)>100:
                                cntcol+=1
                                if len(defn)>199:
                                    cntcol+=1
        return definitions, cntcol, max_width

