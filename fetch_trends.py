import json
import pandas as pd
from pytrends.request import TrendReq

# Inisialisasi pytrends
pytrends = TrendReq(hl='id-ID', tz=420)

# Diberikan input 8 jenis frase tren penelusuran
keywords = ["untuk", "yang", "ini", "itu", "cara", "apa", "dan", "dalam"]

# Build payload sesuai kriteria URL (now 7-d dan geo ID)
pytrends.build_payload(kw_list=keywords, timeframe='now 7-d', geo='ID')

# Ambil data kueri terkait untuk semua kata kunci
related_queries = pytrends.related_queries()

all_top_frames = []
all_rising_frames = []

# Ambil data kueri terpopuler dan makin populer dari masing-masing kata kunci
for kw in keywords:
    kw_data = related_queries.get(kw, {})
    
    top_df = kw_data.get('top')
    if top_df is not None and not top_df.empty:
        all_top_frames.append(top_df)
        
    rising_df = kw_data.get('rising')
    if rising_df is not None and not rising_df.empty:
        all_rising_frames.append(rising_df)

# --- Olah Data Kueri Terpopuler ---
if all_top_frames:
    combined_top = pd.concat(all_top_frames, ignore_index=True)
    # Urutkan berdasarkan nilai minat penelusuran tertinggi dan hapus duplikat kueri
    combined_top = combined_top.sort_values(by='value', ascending=False).drop_duplicates(subset=['query'])
    top_10 = combined_top.head(10)['query'].tolist()
else:
    top_10 = []

# --- Olah Data Kueri yang Makin Populer ---
if all_rising_frames:
    combined_rising = pd.concat(all_rising_frames, ignore_index=True)
    # Urutkan berdasarkan persentase kenaikan tertinggi dan hapus duplikat kueri
    combined_rising = combined_rising.sort_values(by='value', ascending=False).drop_duplicates(subset=['query'])
    rising_10 = combined_rising.head(10)['query'].tolist()
else:
    rising_10 = []

# Simpan hasil berupa daftar nama kueri saja ke data.json
result = {
    "top": top_10,
    "rising": rising_10
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
