""" Note :
Selenium : Memungkinkan kita mengotomatisasi web browser kita sehingga kita bisa go dan click semua gambar yang ingin didonwload (Dapatkan sumbernya, lalu unduh sumber gambarnya)
Request : Digunakan untuk mengambil data gambar yang ingin diunduh 
Web driver : File yang dapat dieksekusi untuk mengotomatisasi browser yang sesuai (Chrome)
NB:Unduh web driver untuk digunakan bersamaan dengan selenium
NB:Selenium v4.6.0 ke atas tidak harus set path driver.exe,
Selenium dapat menangani browser dan driver dengan sendirinya.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import os

option = webdriver.ChromeOptions()
option.add_argument('--ignore-certificate-errors')
wd = webdriver.Chrome(options=option)

def get_images(wd, delay, max_img):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down
        time.sleep(delay) # Memberikan delay saat load image saat scroll down

    # URL kolom search google
    url = "https://www.google.com/search?q=buah+kencur&tbm=isch&ved=2ahUKEwj6mual6ayCAxXIm2MGHdvRA1IQ2-cCegQIABAA&oq=buah+kencur&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgYIABAFEB46BAgjECc6BggAEAcQHjoICAAQBRAHEB46CAgAEAgQBxAeUJYIWJwLYM0OaABwAHgAgAFuiAHkA5IBAzMuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=foVHZfrjLsi3juMP26OPkAU&bih=945&biw=958"
    wd.get(url) # Load page url menggunakan wd
    
    image_urls = set() # Memastikan tidak ada url duplikat
    skips = 0
    
    while len(image_urls) + skips < max_img:
        scroll_down(wd)
        
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd") # Temukan tag berdasarkan nama class
        
        for img in thumbnails[len(image_urls) + skips:max_img + 1]: # Iterasi dari 
            try:
                img.click()
                time.sleep(delay)
            except:
                print('error')
            
            images = wd.find_elements(By.CLASS_NAME, "iPVvYb") # Temukan tag berdasarkan nama class
            for img in images:
                if img.get_attribute('src') in image_urls: # Skip jika foto sudah pernah diklik
                    max_img += 1
                    skips += 1
                    break
                
                if img.get_attribute('src') and 'http' in img.get_attribute('src'): # Ambil source image
                    image_urls.add(img.get_attribute('src'))
                    print(f'Found {len(image_urls)}')
        
    return image_urls
        
def image_downloader(download_folder, url, content, file_name):
    target_folder = os.path.join(download_folder, content) # Join folder berdasarkan path
    
    if not os.path.exists(target_folder): # Memeriksa apakah folder sudah ada
        os.mkdir(target_folder) # Membuat folder jika belum ada
    
    
    try:
        image_content = requests.get(url).content # Get konten gambar berdasarkan url
        image_file = io.BytesIO(image_content) # Menyimpan konten sebagai tipe data biner di memori komputer
        image = Image.open(image_file) # Konversi data biner ke gambar Pillow
        file_path = target_folder + file_name # Generate file_path
    
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
            
        print("Success")
    except Exception as e:
        print('Failed - ', e)
        
urls = get_images(wd, 1, 10)

for i, url in enumerate(urls):
	image_downloader("images", url, 'kencur',  str(i + 1) + ".JPEG")
wd.quit()
