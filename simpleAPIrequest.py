import requests
from requests.models import Response
import pandas as pd
from pandas.io.parsers import read_csv
# Autenticação de uso da API do reddit
auth = requests.auth.HTTPBasicAuth('CtaOCXWP2juVX49NnU7uag', 'Kxu1zfNAf42Ss0jApRQ1QbiR6O9xrQ')

# Login e senha do usuário do reddit
data = {'grant_type': 'password',
        'username': 'pinducat',
        'password': 'Nnwvm7e5M3i5CCC6sYMe'}

# Breve descrição do "APP"
headers = {'User-Agent': 'pinduBot 0.1'}

# Envia o request de um OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value

TOKEN = f"bearer {res.json()['access_token']}"

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': TOKEN}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


lista_stocks = pd.DataFrame(read_csv("C:\\Users\\luis.meinert\\projects\\api\\nyse_stocks.csv"))
lista_stocks = lista_stocks['Symbol']
virouSerie = dict(lista_stocks.squeeze(axis=0))
stock_symbols = {}
for key, v in virouSerie.items():
    stock_symbols[v]=key
for k,v in stock_symbols.items():
    stock_symbols[k] = 0

params={'limit':100}
#dataframe inicial das respostas da API call
def df_from_responses(res):
        df = pd.DataFrame()
        for post in res.json()["data"]["children"]:
                df = df.append({
                        'subreddit': post['data']['subreddit'],
                        'title': post['data']['title'],
                        'selftext': post['data']['selftext'],
                        'upvote_ratio': post['data']['upvote_ratio'],
                        'ups': post['data']['ups'],
                        'downs': post['data']['downs'],
                        'score': post['data']['score'],
                        'kind':post['kind'],
                        'id': post['data']['id']
                }, ignore_index=True)
        return df



def getNewposts(subreddit):
        full_data = pd.DataFrame()
        for i in range(3):                        
                res = requests.get("https://oauth.reddit.com/r/{}/new".format(subreddit), 
                                headers=headers,
                                params=params)
                new_df = df_from_responses(res)
                row = new_df.iloc[len(new_df)-1]
                fullname = row['kind'] + '_' + row['id']
                params['after']= fullname
                full_data = full_data.append(new_df, ignore_index=True)
        #full_data = full_data.sort_values(by='score', ascending=False)
        #full_data = full_data.drop(columns=['kind','id'])
        #print(full_data.head(20))
        #print(df.shape)

def getHotposts(subreddit):
        full_data= pd.DataFrame()
        for i in range(3):
                res = requests.get("https://oauth.reddit.com/r/{}/hot".format(subreddit), 
                                headers=headers, 
                                params=params)
                new_df = df_from_responses(res)
                row = new_df.iloc[len(new_df)-1]
                fullname = row['kind'] + '_' + row['id']
                params['after']= fullname
                full_data = full_data.append(new_df, ignore_index=True)
        full_data = full_data.sort_values(by='score', ascending=False)
        full_data = full_data.drop(columns=['kind','id','selftext'])
        print(full_data.head(20))
        '''for word in stock_symbols:
                if word  in full_data['title']:
                        stock_symbols[word] += 1
        print(stock_symbols)


        full_data_count = 

        print(full_data_count)'''

listateste = ['TSLA','GME','AMC','DWAC','CLNE','WISH','CLOV','SPY']

#
# input('Wich subreddit you wanna check? \n')
getHotposts('wallstreetbets')
#getNewposts("askreddit")
#https://www.reddit.com/prefs/apps
#https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
#https://www.dataquest.io/blog/python-api-tutorial/