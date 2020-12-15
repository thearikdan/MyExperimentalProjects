# https://towardsdatascience.com/google-trends-api-for-python-a84bc25db88f

import pandas as pd
from pytrends.request import TrendReq

pytrend = TrendReq()

pytrend.build_payload(kw_list=["TQQQ"])

df = pytrend.interest_by_region()
print (df)
df.to_html("temp.html")
#print(df.head(150))

related_queries = pytrend.related_queries()
print (related_queries.values())

related_topics = pytrend.related_topics()
print (related_topics.values())

keywords = pytrend.suggestions(keyword='TQQQ')
df = pd.DataFrame(keywords)
df.drop(columns='mid')
print (df)



df = pytrend.trending_searches(pn='united_states')
#print (df.head())

df = pytrend.today_searches(pn='US')
#print (df.head())

df = pytrend.top_charts(2020, hl='en-US', tz=300, geo='GLOBAL')
#print (df.head())