import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Sabitler
N = 10  # Grid boyutu
max_steps = 10  # Zaman adımı sayısı (dens0_t0.csv, dens0_t1.csv, ..., dens0_t9.csv)

# CSV dosyasını okuma fonksiyonu
def read_csv(filename):
    # CSV dosyasını pandas ile oku, ';' ile ayırarak
    data = pd.read_csv(filename, header=None, delimiter=';')  # Noktalı virgülle ayır
    data = data.astype(float)  # Verileri float türüne dönüştür
    return data.values  # Pandas DataFrame'ini numpy array'e dönüştür

# Grafik oluşturma
fig, ax = plt.subplots(figsize=(8, 6))  # Tek bir büyük grafik

# X ve Y etiketlerini ayarla
ax.set_xlabel('Column')
ax.set_ylabel('Row')

# Başlangıç verisini oku ve ilk plotu oluştur
initial_data = read_csv('dens0_t0.csv')  # İlk zaman adımındaki veriyi oku
im = ax.imshow(initial_data, cmap='viridis', interpolation='nearest', vmin=0, vmax=10)

# Renk barını oluştur
cbar = fig.colorbar(im)

# Plot güncelleme fonksiyonu
def update_plot(step):
    # Zaman adımına göre dosya adını oluştur
    filename = f'dens0_t{step}.csv'
    
    # Dosyanın var olup olmadığını kontrol et
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return
    
    # Veriyi oku
    data = read_csv(filename)

    print(data[2][3])
    # Grafik nesnesini güncelle
    im.set_data(data)  # Yeni veri ile plotu güncelle
    
    # Başlık güncelle
    ax.set_title(f'Time Step: {step}')
    
    # Yeniden çizim yap
    plt.draw()  # Grafik güncellenir
    plt.pause(0.5)  # 0.5 saniye bekleyerek güncellenmesini sağla

# Zaman adımlarını işle
for t in range(max_steps):
    print(f"Processing time step: {t}")  # Debug mesajı
    update_plot(t)

# Tüm adımlar bittikten sonra grafiği göster
plt.show()
