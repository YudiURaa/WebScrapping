import requests
from bs4 import BeautifulSoup
import pandas as pd

# inisialisasi kolom data yang ingin disimpan ke dalam file
columns = ['Name', 'Address', 'Phone']

# inisialisasi DataFrame kosong
df = pd.DataFrame(columns=columns)

for i in range(5739, 7387):
    # membuat url
    url = f"https://www.locatefamily.com/Street-Lists/Indonesia/index-{i}.html"
    headers = {
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
    }
    
    # melakukan request ke url
    response = requests.get(url, headers=headers)

    # mengubah response menjadi objek BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # mencari semua tag <a> yang mengandung class 'listlink'
    list_links = soup.find_all('a', class_='listlink')

    # melakukan scraping pada setiap link yang ditemukan
    for link in list_links:
        # melakukan request ke halaman individu
        response = requests.get(link['href'])

        # mengubah response menjadi objek BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # mencari tag <h1> yang mengandung nama
        name_tag = soup.find('h1', class_='heading')
        name = name_tag.text.strip()

        # mencari tag <div> yang mengandung alamat dan nomor telepon
        address_div = soup.find('div', class_='address')
        address = address_div.find_all('p')[0].text.strip()
        phone = address_div.find_all('p')[1].text.strip()

        # menambahkan data ke dalam DataFrame
        df = df.append({'Name': name, 'Address': address, 'Phone': phone}, ignore_index=True)

# menyimpan DataFrame ke dalam file CSV
df.to_csv('data.csv', index=False)

# menyimpan DataFrame ke dalam file XLSX
df.to_excel('data.xlsx', index=False)
