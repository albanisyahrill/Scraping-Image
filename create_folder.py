import os

download_folder = 'images'
content = 'kencur'

if not os.path.exists(download_folder): # Memeriksa apakah folder sudah ada
    os.mkdir(download_folder) # Membuat folder jika belum ada
    
target_folder = os.mkdir(os.path.join(download_folder, content)) # Membuat folder jika belum ada