import requests, json, re
from parsel import Selector


def scrapeGoogleFinance():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36"
        }

    html = requests.get(f"https://www.google.com/finance/", headers=headers, timeout=30)
    selector = Selector(text=html.text)
    
    ticker_data = {
        "market_trends": [],
        "interested_in": {
            "top_position": [],
            "bottom_position": []
        },
        "earning_calendar": [],
        "most_followed_on_google": [],
        "news": [],
    }

    ticker_data["market_trends"] = selector.css(".gR2U6::text").getall()
    
    for mostFollowedGoogle in selector.css(".NaLFgc"):
        current_percent_change_raw_value = mostFollowedGoogle.css("[jsname=Fe7oBc]::attr(aria-label)").get()
        current_percent_change = re.search(r"by\s?(\d+\.\d+)%", mostFollowedGoogle.css("[jsname=Fe7oBc]::attr(aria-label)").get()).group(1)

        ticker_data["most_followed_on_google"].append({
            "title": mostFollowedGoogle.css(".TwnKPb::text").get(),
            "quote": re.search(r"\.\/quote\/(\w+):",mostFollowedGoogle.attrib["href"]).group(1),            # https://regex101.com/r/J3DDIX/1
            "following": re.search(r"(\d+\.\d+)M", mostFollowedGoogle.css(".Iap8Fc::text").get()).group(1), # https://regex101.com/r/7ptVha/1
            "percent_price_change": f"+{current_percent_change}" if "Up" in current_percent_change_raw_value else f"-{current_percent_change}"
        })

    for index, news in enumerate(selector.css(".yY3Lee"), start=1):
        ticker_data["news"].append({
            "position": index,
            "title": news.css(".Yfwt5::text").get(),
            "link": news.css(".z4rs2b a::attr(href)").get(),
            "source": news.css(".sfyJob::text").get(),
            "published": news.css(".Adak::text").get(),
            "thumbnail": news.css("img.Z4idke::attr(src)").get()
        })

    for index, interested_top in enumerate(selector.css(".sbnBtf:not(.xJvDsc) .SxcTic"), start=1):
        current_percent_change_raw_value = interested_top.css("[jsname=Fe7oBc]::attr(aria-label)").get()
        current_percent_change = re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%", interested_top.css("[jsname=Fe7oBc]::attr(aria-label)").get()).group()

        ticker_data["interested_in"]["top_position"].append({
            "index": index,
            "title": interested_top.css(".ZvmM7::text").get(),
            "quote": interested_top.css(".COaKTb::text").get(),
            "price_change": interested_top.css(".SEGxAb .P2Luy::text").get(),
            "percent_price_change": f"+{current_percent_change}" if "Up" in current_percent_change_raw_value else f"-{current_percent_change}"
        })

    for index, interested_bottom in enumerate(selector.css(".HDXgAf .tOzDHb"), start=1):

        current_percent_change_raw_value = interested_bottom.css("[jsname=Fe7oBc]::attr(aria-label)").get()
        current_percent_change = re.search(r"\d{1}%|\d{1,10}\.\d{1,2}%", interested_bottom.css("[jsname=Fe7oBc]::attr(aria-label)").get()).group()

        ticker_data["interested_in"]["bottom_position"].append({
            "position": index,
            "ticker": interested_bottom.css(".COaKTb::text").get(),
            "ticker_link": f'https://www.google.com/finance{interested_bottom.attrib["href"].replace("./", "/")}',
            "title": interested_bottom.css(".RwFyvf::text").get(),
            "price": interested_bottom.css(".YMlKec::text").get(),
            "percent_price_change": f"+{current_percent_change}" if "Up" in current_percent_change_raw_value else f"-{current_percent_change}"
        })

    return ticker_data