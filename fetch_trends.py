import json
import pandas as pd
from pytrends.request import TrendReq

# Set proxy ke Workers Anda
PROXIES = [
    'https://trending.minixsrv.workers.dev/?url='
]

pytrends = TrendReq(
    hl='id-ID', 
    tz=420, 
    retries=3, 
    backoff_factor=1,
    proxies=PROXIES
)

keywords = ["untuk", "yang", "ini", "itu", "cara", "apa", "dan", "dalam"]

all_top_frames = []
all_rising_frames = []

# Google Trends hanya menerima maksimal 5 keywords per payload.
# Kita bagi keyword menjadi kelompok 4 item.
chunk_size = 4
for i in range(0, len(keywords), chunk_size):
    kw_chunk = keywords[i:i + chunk_size]
    
    try:
        pytrends.build_payload(kw_list=kw_chunk, timeframe='now 7-d', geo='ID')
        related_queries = pytrends.related_queries()
        
        for kw in kw_chunk:
            kw_data = related_queries.get(kw, {})
            top_df = kw_data.get('top')
            if top_df is not None and not top_df.empty:
                all_top_frames.append(top_df)
                
            rising_df = kw_data.get('rising')
            if rising_df is not None and not rising_df.empty:
                all_rising_frames.append(rising_df)
    except Exception as e:
        print(f"Gagal mengambil batch {kw_chunk}: {e}")

# Process & Output ke data.json
top_10 = pd.concat(all_top_frames, ignore_index=True).sort_values(by='value', ascending=False).drop_duplicates(subset=['query']).head(10)['query'].tolist() if all_top_frames else []
rising_10 = pd.concat(all_rising_frames, ignore_index=True).sort_values(by='value', ascending=False).drop_duplicates(subset=['query']).head(10)['query'].tolist() if all_rising_frames else []

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump({"top": top_10, "rising": rising_10}, f, ensure_ascii=False, indent=2)
