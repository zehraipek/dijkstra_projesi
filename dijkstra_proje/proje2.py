import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import heapq
import random
import time
import tracemalloc
import os
import customtkinter as ctk

# csv dosyasındaki şehir ve mesafe bilgilerini okuyarak grafiği oluşturuyoruz
dosya_yolu = os.path.join(os.path.dirname(__file__), "distances.csv")

df=pd.read_csv(dosya_yolu)

G=nx.Graph()
#csv içindeki verileri grafa ekliyoruz
for _,row in df.iterrows():

    G.add_edge(
        row["From"],
        row["To"],
        weight=row["Distance"]
    )

# Şehir koordinatları (bbu kısım harita çizimi için görsel amaçlı)

city_coords = {

"Adana":(35.32,37.00),
"Adıyaman":(38.27,37.76),
"Afyonkarahisar":(30.54,38.75),
"Ağrı":(43.05,39.72),
"Aksaray":(34.03,38.37),
"Amasya":(35.83,40.65),
"Ankara":(32.85,39.93),
"Antalya":(30.71,36.89),
"Ardahan":(42.70,41.11),
"Artvin":(41.82,41.18),
"Aydın":(27.84,37.84),
"Balıkesir":(27.88,39.64),
"Bartın":(32.34,41.63),
"Batman":(41.13,37.88),
"Bayburt":(40.23,40.25),
"Bilecik":(29.97,40.15),
"Bingöl":(40.50,38.88),
"Bitlis":(42.11,38.40),
"Bolu":(31.61,40.73),
"Burdur":(30.28,37.72),
"Bursa":(29.06,40.18),
"Çanakkale":(26.41,40.15),
"Çankırı":(33.62,40.60),
"Çorum":(34.95,40.55),
"Denizli":(29.09,37.77),
"Diyarbakır":(40.23,37.91),
"Düzce":(31.15,40.84),
"Edirne":(26.56,41.67),
"Elazığ":(39.22,38.68),
"Erzincan":(39.49,39.75),
"Erzurum":(41.27,39.90),
"Eskişehir":(30.52,39.77),
"Gaziantep":(37.38,37.06),
"Giresun":(38.39,40.91),
"Gümüşhane":(39.48,40.46),
"Hakkari":(43.74,37.57),
"Hatay":(36.16,36.20),
"Iğdır":(44.04,39.92),
"Isparta":(30.55,37.76),
"İstanbul":(28.97,41.01),
"İzmir":(27.14,38.42),
"Kahramanmaraş":(36.93,37.58),
"Karabük":(32.62,41.20),
"Karaman":(33.22,37.18),
"Kars":(43.10,40.60),
"Kastamonu":(33.78,41.38),
"Kayseri":(35.49,38.73),
"Kırıkkale":(33.51,39.85),
"Kırklareli":(27.23,41.73),
"Kırşehir":(34.16,39.15),
"Kilis":(37.12,36.72),
"Kocaeli (İzmit)":(29.91,40.76),
"Konya":(32.48,37.87),
"Kütahya":(29.98,39.41),
"Malatya":(38.31,38.35),
"Manisa":(27.43,38.62),
"Mardin":(40.74,37.31),
"Mersin":(34.64,36.80),
"Muğla":(28.36,37.21),
"Muş":(41.49,38.73),
"Nevşehir":(34.72,38.62),
"Niğde":(34.68,37.97),
"Ordu":(37.88,40.98),
"Osmaniye":(36.25,37.07),
"Rize":(40.52,41.02),
"Sakarya (Adapazarı)":(30.40,40.75),
"Samsun":(36.33,41.29),
"Siirt":(41.94,37.93),
"Sinop":(35.15,42.02),
"Sivas":(37.02,39.75),
"Şanlıurfa":(38.79,37.17),
"Şırnak":(42.49,37.52),
"Tekirdağ":(27.51,40.97),
"Tokat":(36.55,40.32),
"Trabzon":(39.72,41.00),
"Tunceli":(39.54,39.11),
"Uşak":(29.41,38.68),
"Van":(43.38,38.49),
"Yalova":(29.27,40.65),
"Yozgat":(34.81,39.82),
"Zonguldak":(31.79,41.45)

}

#Burda Dijkstra algoritmasını kullanarak başlangıç ve hedef 
# arasında en kısa yolu buluyoruz 

def dijkstra(graph,start,end):

    pq=[(0,start)]

    # başlangıçta bütün şehirler sonsuz uzaklıkta
    distances={

        node:float("inf")
        for node in graph.nodes()
    }

    previous={}

    distances[start]=0

    while pq:

        current_distance,current_node=heapq.heappop(pq)

        if current_node==end:
            break
#komşu şehirleri kontrol ediyoruz
        for neighbor in graph.neighbors(current_node):

            weight=graph[current_node][neighbor]["weight"]

            distance=current_distance+weight
# daha kısa bir yol bulursak güncelliyoruz
            if distance<distances[neighbor]:

                distances[neighbor]=distance

                previous[neighbor]=current_node

                heapq.heappush(
                    pq,
                    (
                        distance,
                        neighbor
                    )
                )
# en kısa yolu tekrar oluşturuyoruz
    path=[]

    node=end

    while node in previous:

        path.append(node)

        node=previous[node]

    path.append(start)

    path.reverse()

    return distances[end],path


# Harita çizimi için bir fonksiyon oluşturuyoruz

def draw_map(path):

    plt.figure(figsize=(14,8))
# tüm şehirleri harita üzerinde gösteriyoruz
    for city,(x,y) in city_coords.items():

        plt.scatter(
            x,
            y,
            color="lightgray",
            s=15
        )
# gidilen yolu farklı renklerle gösteriyoruz
    for i,city in enumerate(path):

        x,y=city_coords[city]

        if i==0:
            color="green"

        elif i==len(path)-1:
            color="blue"

        else:
            color="red"

        plt.scatter(
            x,
            y,
            color=color,
            s=150
        )

        plt.text(
            x+.1,
            y+.1,
            city,
            fontsize=8
        )
# şehirler arasındaki bağlantıları çiziyoruz
    for i in range(len(path)-1):

        city1=path[i]
        city2=path[i+1]

        x1,y1=city_coords[city1]
        x2,y2=city_coords[city2]

        plt.plot(
            [x1,x2],
            [y1,y2],
            color="red",
            linewidth=3
        )

    plt.title(
        "Türkiye Dijkstra En Kısa Yol"
    )

    plt.grid()

    plt.show()

# Burda performans testi yapıyoruz 
#düğüm arttıkça süre ve bellek değişimini görmek için 

def performance_test():

    sizes=[10,20,30,40,50]

    times=[]
    memories=[]

    for size in sizes:

        total_time=0
        total_memory=0

        for _ in range(30):

            nodes=random.sample(
                list(G.nodes()),
                size
            )

            sub=G.subgraph(nodes)

            s=random.choice(nodes)
            e=random.choice(nodes)

            tracemalloc.start()

            start=time.time()

            dijkstra(sub,s,e)

            elapsed=time.time()-start

            _,peak=tracemalloc.get_traced_memory()

            tracemalloc.stop()

            total_time+=elapsed
            total_memory+=peak/1024

        times.append(total_time/30)
        memories.append(total_memory/30)

    plt.figure(figsize=(12,5))

    plt.subplot(121)

    plt.plot(sizes,times,marker="o")
    plt.title("Zaman Karmaşıklığı")
    plt.xlabel("Düğüm Sayısı")
    plt.ylabel("Çalışma Süresi (saniye)")
    plt.grid()

    plt.subplot(122)

    plt.plot(sizes,memories,marker="o")
    plt.title("Bellek Karmaşıklığı")
    plt.xlabel("Düğüm Sayısı")
    plt.ylabel("Bellek Kullanımı (KB)")
    plt.grid()

    plt.tight_layout()
    plt.show()

    # tkinter arayüzü oluşturuyoruz

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1000x650")
root.title("En Kısa Yol Bulma Sistemi")
root.configure(fg_color="#F4F8FB")

# şehirleri sıralı şekilde göstermek için 
cities = sorted(
    list(G.nodes())
)

# Ana başlık
title_label = ctk.CTkLabel(
    root,
    text="Türkiye Şehirler Arası En Kısa Yol Bulma Sistemi",
    font=("Times New Roman", 28, "bold"),
    text_color="#1F3A5F"
)
title_label.pack(pady=(25, 5))

subtitle_label = ctk.CTkLabel(
    root,
    text="Dijkstra Algoritması ile En Kısa Rota Hesaplama",
    font=("Times New Roman", 16),
    text_color="#5D6D7E"
)
subtitle_label.pack(pady=(0, 20))

# Şehir seçim alanı
select_frame = ctk.CTkFrame(
    root,
    fg_color="#FFFFFF",
    corner_radius=18,
    border_width=1,
    border_color="#D6E3F0"
)
select_frame.pack(pady=10, padx=80, fill="x")

left_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
left_frame.pack(side="left", expand=True, fill="x", padx=25, pady=20)

right_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
right_frame.pack(side="right", expand=True, fill="x", padx=25, pady=20)

ctk.CTkLabel(
    left_frame,
    text="Başlangıç Şehri",
    font=("Times New Roman", 15, "bold"),
    text_color="#34495E"
).pack(anchor="w", pady=(0, 8))

start_combo = ctk.CTkComboBox(
    left_frame,
    values=cities,
    width=350,
    height=38,
    corner_radius=10,
    border_color="#C9D8E8",
    button_color="#D6EAF8",
    button_hover_color="#AED6F1",
    fg_color="#FFFFFF",
    text_color="#1F2D3D",
    dropdown_fg_color="#FFFFFF",
    dropdown_text_color="#1F2D3D"
)
start_combo.pack(anchor="w")

ctk.CTkLabel(
    right_frame,
    text="Hedef Şehir",
    font=("Times New Roman", 15, "bold"),
    text_color="#34495E"
).pack(anchor="w", pady=(0, 8))

end_combo = ctk.CTkComboBox(
    right_frame,
    values=cities,
    width=350,
    height=38,
    corner_radius=10,
    border_color="#C9D8E8",
    button_color="#D6EAF8",
    button_hover_color="#AED6F1",
    fg_color="#FFFFFF",
    text_color="#1F2D3D",
    dropdown_fg_color="#FFFFFF",
    dropdown_text_color="#1F2D3D"
)
end_combo.pack(anchor="w")

# Sonuç ve adım alanı
content_frame = ctk.CTkFrame(
    root,
    fg_color="#FFFFFF",
    corner_radius=18,
    border_width=1,
    border_color="#D6E3F0"
)
content_frame.pack(pady=25, padx=60, fill="both", expand=True)

result_frame = ctk.CTkFrame(
    content_frame,
    fg_color="transparent"
)
result_frame.pack(side="left", fill="both", expand=True, padx=25, pady=25)

step_frame = ctk.CTkFrame(
    content_frame,
    fg_color="transparent"
)
step_frame.pack(side="right", fill="both", expand=True, padx=25, pady=25)

ctk.CTkLabel(
    result_frame,
    text="Sonuç",
    font=("Times New Roman", 20, "bold"),
    text_color="#2471A3"
).pack(anchor="w", pady=(0, 15))

result_box = ctk.CTkFrame(
    result_frame,
    fg_color="#F7FBFF",
    corner_radius=15,
    border_width=1,
    border_color="#D6E3F0"
)
result_box.pack(fill="both", expand=True)

result = ctk.CTkLabel(
    result_box,
    text="Henüz bir şehir seçimi yapılmadı.",
    font=("Times New Roman", 18, "bold"),
    text_color="#1F3A5F",
    wraplength=350,
    justify="center"
)
result.pack(expand=True, padx=20, pady=20)

ctk.CTkLabel(
    step_frame,
    text="Adım Adım İşlem",
    font=("Times New Roman", 20, "bold"),
    text_color="#2471A3"
).pack(anchor="w", pady=(0, 15))

step_box = ctk.CTkTextbox(
    step_frame,
    width=420,
    height=230,
    corner_radius=15,
    border_width=1,
    border_color="#D6E3F0",
    fg_color="#F7FBFF",
    text_color="#2C3E50",
    font=("Times New Roman", 14)
)
step_box.pack(fill="both", expand=True)

# Butona basınca çalışacak fonksiyon oluşturuyoruz
def calculate():

    start = start_combo.get()

    end = end_combo.get()

    distance, path = dijkstra(
        G,
        start,
        end
    )

    result.configure(
        text=
        f"Toplam Mesafe: {distance} km\n\n" +
        " → ".join(path)
    )

    step_box.delete(
        1.0,
        tk.END
    )

    # gidilen şehir ve komşuları ekrana yazdırıyoruz
    for i in range(len(path)-1):

        city = path[i]

        next_city = path[i+1]

        text = f"\n{i+1}) {city}\n"

        text += "Komşular:\n"

        for neighbor in G.neighbors(city):

            dist = G[city][neighbor]["weight"]

            if neighbor == next_city:

                text += f"{neighbor} → {dist} km ✓\n"

            else:

                text += f"{neighbor} → {dist} km\n"

        step_box.insert(
            tk.END,
            text
        )

    draw_map(path)

# Butonlar
button_frame = ctk.CTkFrame(
    root,
    fg_color="transparent"
)
button_frame.pack(pady=(0, 25))

ctk.CTkButton(
    button_frame,
    text="En Kısa Yol Bul",
    command=calculate,
    width=230,
    height=48,
    corner_radius=18,
    fg_color="#5DADE2",
    hover_color="#3498DB",
    text_color="white",
    font=("Times New Roman", 17, "bold")
).pack(side="left", padx=15)

ctk.CTkButton(
    button_frame,
    text="Performans Analizi",
    command=performance_test,
    width=230,
    height=48,
    corner_radius=18,
    fg_color="#D5F5E3",
    hover_color="#ABEBC6",
    text_color="#117864",
    font=("Times New Roman", 17, "bold")
).pack(side="left", padx=15)

root.mainloop()


