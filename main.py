import scraping

import json
import time

#for timing seconds
def max_seconds(max_seconds, *, interval=1):
    interval = int(interval)
    start_time = time.time()
    end_time = start_time + max_seconds
    yield 0
    while time.time() < end_time:
        if interval > 0:
            next_time = start_time
            while next_time < time.time():
                next_time += interval
            time.sleep(int(round(next_time - time.time())))
        yield int(round(time.time() - start_time))
        if int(round(time.time() + interval)) > int(round(end_time)): 
            return

print('You can request stats for the following ticker symbols:')
ticker = scraping.scrapeGoogleFinance()["interested_in"]["top_position"]
print("index : ticker/name")
for item in ticker:
    if(item["quote"] == "Index"):
        print (item["index"], "    :  ", item["title"])
        continue
    print(item["index"], "    :  ", item["quote"])
print('Enter an index for the respective ticker symbol to get stats for it:')
ticker_choice = input()
ticker_found = False;
print("How many minutes would you like to scrape for? (Reminder: Scraping is best done on open market hours)")
scrape_time = int(input())*60


for sec in max_seconds(scrape_time):
    ticker = scraping.scrapeGoogleFinance()["most_followed_on_google"]
    if(sec%60 == 0):
        print(json.dumps(scraping.scrapeGoogleFinance(), indent=2, ensure_ascii=False))
    
