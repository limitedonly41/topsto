import requests
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import time
import unicodedata
import math


def get_top_sto():
  
    URL = "https://topsto-crimea.ru/telefoniya/mobilnye-telefony/page-1/?features_hash=57415-23430325-17271447"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    # print(soup.prettify())
    pages = soup.find('div', attrs = {'class':'ty-pagination'}) 

    number_pages = pages.findAll('a') 

    max_page = max([a.text for a in number_pages])



    items = []

    for p in range(1,int(max_page)+1):
        url = URL.replace('page-1', f'page-{p}')

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        items_list = soup.find('div', attrs = {'id': 'categories_view_pagination_contents'})

        all_items = items_list.findAll('div', attrs = {'class': 'ty-column4'})


        for item in all_items:
            if not 'category-banner' in str(item):
                items.append(item)
        time.sleep(1)


    links = []
    for item in items:
        try:
            links.append(item.a['href'])
        except:
            continue



    data_phones = []
    for link in tqdm(links):

        features_dict = {}

        url = link

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        features_list = soup.find('div', attrs = {'id': 'content_features'})

        features = features_list.findAll('div', attrs = {'class': 'ty-product-feature'})

        price = soup.find('span', attrs = {'class': 'ty-price'}).text

        s = price.split('Р')[0]
        new_str = unicodedata.normalize("NFKD", s)
        price = new_str.strip().replace(' ','')

        brand = " ".join(features[0].text.strip().split(':')[1].split())
        model = " ".join(features[1].text.strip().split(':')[1].split())

        header = soup.find('h1').text

        memory = ''

        if 'Gb' in str(header):
            memory = header.split('Gb')[0].split()[-1]
        elif 'GB' in str(header):
            memory = header.split('GB')[0].split()[-1]
        else:
            memory = ''

        if '/' in memory:
            memory = memory.split('/')[1]

        features_dict['brand'] = brand
        features_dict['model'] = model
        features_dict['memory'] = memory
        features_dict['price'] = int(price)
        features_dict['url'] = url

        data_phones.append(features_dict)

        time.sleep(1)


    df = pd.DataFrame(data_phones)
    df['model'] = df['model'].str.lower()
    df['model'] = df['model'].str.replace('galaxy', '')

    return df


def get_park():

    URL = "https://park-mobile.ru/catalog/telefony_i_smart_chasy/smartfony/filter/att_brand-samsung/page-1/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
    # print(soup.prettify())
    pages = soup.find('ul', attrs = {'class':'pagination__list'}) 


    number_pages = pages.findAll('li') 
    # number_pages[-1].text

    # max_page = max([a.text for a in number_pages if type(a.text)==int])

    max_page = number_pages[-3].text
    max_page

    items = []

    for p in range(1,int(max_page)+1):
        url = URL.replace('page-1', f'page-{p}')

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        items_list = soup.findAll('div', attrs = {'id': 'big-list'})

    #     all_items = items_list.findAll('div', attrs = {'class': 'ty-column4'})
        links = ['https://park-mobile.ru' + item.a['href'] for item in items_list]

        items.extend(links)
        time.sleep(1)


    len(items)

    len(set(items))

    data_phones = []
    for link in tqdm(items):

        features_dict = {}

        url = link

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')

        try:
            features_list = soup.find('div', attrs = {'class': 'card-detail__bottom'}).ul
        except:
            continue
        features = features_list.findAll('li')

        price = soup.find('div', attrs = {'class': 'card-total__price'}).text

        s = price.split('Р')[0]
        new_str = unicodedata.normalize("NFKD", s)
        price = new_str.strip().replace(' ','')

    #     print(url)

        try:
            brand = " ".join(features[0].text.strip().split('Производитель')[1].split())
        except:
            itemscope_list = soup.find('ul', attrs = {'itemscope': 'itemscope'})
            itemscope = itemscope_list.findAll('li')
            texts = [f.text for f in features]
            brand = texts[-3]

        try:
            model = " ".join(features[1].text.strip().split('Название модели')[1].split())
        except:
            itemscope_list = soup.find('ul', attrs = {'itemscope': 'itemscope'})
            itemscope = itemscope_list.findAll('li')
            texts = [f.text for f in features]
            model = texts[-2].split()[-1]

        header = soup.find('h1').text

        memory = ''

        if 'Gb' in str(header):
            memory = header.split('Gb')[0].split()[-1]
        elif 'GB' in str(header):
            memory = header.split('GB')[0].split()[-1]
        else:
            if '/' in str(header):
                s = header.split()
                for i in s:
                    if '/' in i:
                        index = s.index(i)
                memory = s[index]

        if '/' in memory:
            memory = memory.split('/')[1]

        features_dict['brand'] = brand
        features_dict['model'] = model
        features_dict['memory'] = memory
        features_dict['price'] = int(price.replace('₽',''))
        features_dict['url'] = url

        brand, model, memory, price = ['','','',0]

        data_phones.append(features_dict)

        time.sleep(1)





    df2 = pd.DataFrame(data_phones)
    df2['model'] = df2['model'].str.lower()
    df2['model'] = df2['model'].str.replace('galaxy', '')
    
    return df2


def show_table(df, df2):

    df_full = df[df['brand'].str.contains('Samsung')]



    df_full['park_model'] = None
    df_full['park_memory'] = None
    df_full['park_url'] = None
    df_full['park_price'] = -math.inf

    for index, row in df2.iterrows():
        words = row['model'].split()
        
        if '+' in words:
            words.index('+').replace('+', ' plus')

        if 'fe' in words or 'plus' in words or 'ultra' in words:
            words[-2] = words[-2] + ' ' + words[-1]
            words = words[:-1]

        if 'flip' in words or 'fold' in words:


            words[-2] = words[-2] + ' ' + words[-1]
            words = words[:-1]

        for w in words:
            match_df = df_full[df_full['model'].str.contains(w)]
            if match_df.shape[0] > 0:
                mem_df = match_df[match_df['memory'].str.contains(row['memory'])]
                if mem_df.shape[0] > 0:

                    indexes = list(mem_df.index)

                    for i in indexes:
                        names = mem_df.loc[i,'model']
                        if not w in names.split():
                            continue

                        df_full.loc[i, 'park_model'] = row['model']
                        df_full.loc[i, 'park_memory'] = row['memory']
                        df_full.loc[i, 'park_url'] = row['url']
                        df_full.loc[i, 'park_price'] = row['price']


    df_full['diff'] = df_full["park_price"] - df_full["price"]
    df_full['diff_percent'] = df_full["park_price"] / df_full["price"]


    final_df = df_full.sort_values(by=['diff'], ascending=False)


    show_df = final_df[~final_df['model'].str.contains('z')]
    show_df = show_df.reset_index(drop=True)
    
    return show_df
    

def main():
    df1 = get_top_sto()
    df2 = get_park()

    df = show_table(df1, df2)

    return df, df1, df2