import json
from pytrends.request import TrendReq

# Inisialisasi pytrends
pytrends = TrendReq(hl='id-ID', tz=420)

# Build payload sesuai filter: kata kunci "parenting", geo "ID", timeframe 1 hari (now 1-d)
pytrends.build_payload(kw_list=['parenting'], timeframe='now 1-d', geo='ID')

# Ambil data kueri terkait
related_queries = pytrends.related_queries()
parenting_data = related_queries.get('parenting', {})

# Ekstrak Kueri Terpopuler (Top) & Makin Populer (Rising)
top_df = parenting_data.get('top')
rising_df = parenting_data.get('rising')

result = {
    "top": top_df.to_dict(orient="records") if top_df is not None else [],
    "rising": rising_df.to_dict(orient="records") if rising_df is not None else []
}

# Simpan ke data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
