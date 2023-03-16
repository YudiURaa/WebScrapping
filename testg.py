import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import filedialog
import time

class App:
    def __init__(self, master):
        self.master = master
        master.title("Locate Family Scraper")

        self.label = tk.Label(master, text="Enter start and end pages:")
        self.label.pack()

        self.start_entry = tk.Entry(master)
        self.start_entry.pack()

        self.end_entry = tk.Entry(master)
        self.end_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.scrape_button = tk.Button(master, text="Scrape", command=self.scrape)
        self.scrape_button.pack()

        self.status = tk.Label(master, text="")
        self.status.pack()
        
        self.pause_button = tk.Button(master, text='Pause', command=self.pause_scrape)
        self.pause_button.pack()
    
        
        self.is_stoped = False
        
    def browse_file(self):
        self.filename = filedialog.asksaveasfilename(initialdir=".", title="Select Output File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        self.status.config(text=f"Output file: {self.filename}")
        self.status.update()

    def scrape(self):
        start_page = int(self.start_entry.get())
        end_page = int(self.end_entry.get())

        datas = []
        self.stop = False
        self.stop_button.config(state=tk.NORMAL)
        
        for i in range(start_page, end_page + 1):
            url = f'https://www.locatefamily.com/Street-Lists/Indonesia/index-{i}.html'
            proxies = {'socks4': '103.77.227.201:4153'}
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'}
            result = None
             # melakukan request dan handling jika respons bukan 200
            while result is None or result.status_code != 200:
                if result is not None and result.status_code is not 200:
                    print("Terlalu banyak permintaan. Menunggu 5 detik...")
                    time.sleep(5)
                result = requests.post(url, headers=headers, proxies=proxies)
                print(result)
            soup = BeautifulSoup(result.text, 'html.parser')

            items = soup.findAll('li', 'list-group-item')

            for it in items:
                address = it.find('span', {'itemprop': 'streetAddress'}).text if it.find('span', {'itemprop': 'streetAddress'}) else ''
                city = it.find('span', {'itemprop': 'addressLocality'}).text if it.find('span', {'itemprop': 'addressLocality'}) else ''

                phone_element = it.find('li', {'itemprop': 'telephone'})
                phone = phone_element.text if phone_element else 'N/A'

                name1 = it.find('span', {'itemprop': 'givenName'}).text
                name2 = it.find('span', {'itemprop': 'familyName'}).text

                datas.append([address, city, phone, name1, name2])

            kepala = ['address', 'city', 'phone', 'name1', 'name2']

            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(kepala)

                for d in datas:
                    writer.writerow(d)

            self.status.config(text=f"Response code for page {i}: {result.status_code}")
            self.status.update()

        self.status.config(text=f"Scraping completed. Output file: {self.filename}")
        self.status.update()

    def pause_scrape(self):
        while self.is_paused : True
        self.status.config(text=f"Scraping paused")
        self.scrape_button.config(text='Resume')
        self.status.update()

    def stop_scrape(self):
        self.is_stoped = True
        self.status.config(text=f"Scraping continued")
        self.status.update()
        
root = tk.Tk()
app = App(root)
root.mainloop()

