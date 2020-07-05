from functools import partial

from .preprocessing import (
    transform_items_ads_impressions,
    transform_items_counter,
    transform_items_js,
    transform_items_none,
    transform_items_regions,
    transform_items_subset,
    transform_items_topics,
)

base_url = "https://political-dashboard.com/json_files/"

facebook = [
    {
        "type": "js",
        "url": "ads_top10.js",
        "key": "ads",
        "func": partial(transform_items_js, keys=["advertiser", "count"]),
    },
    {
        "type": "js",
        "url": "ads_impressions.js",
        "key": "ads_impressions",
        "func": transform_items_ads_impressions,
    },
    {
        "type": "json",
        "url": "ads_regions.json",
        "key": "ads_regions",
        "func": transform_items_regions,
    },
    {
        "type": "json",
        "url": "counter_ads.json",
        "key": "ads_count",
        "func": transform_items_counter,
    },
    {
        "type": "json",
        "url": "fb_spiderplot.json",
        "key": "reactions",
        "func": transform_items_none,
    },
    {
        "type": "json",
        "url": "fb_sentiment.json",
        "key": "sentiment",
        "func": transform_items_none,
    },
    {
        "type": "json",
        "url": "fb_posts.json",
        "key": "posts",
        "func": transform_items_subset,
    },
    {
        "type": "json",
        "url": "fb_shares.json",
        "key": "shares",
        "func": transform_items_subset,
    },
    {
        "type": "json",
        "url": "fb_likes.json",
        "key": "likes",
        "func": transform_items_subset,
    },
]

media = [
    {
        "type": "js",
        "url": "urls_top_facebook.js",
        "key": "urls",
        "func": partial(transform_items_js, keys=["text", "count"]),
    },
    {
        "type": "json",
        "url": "news_party_attention.json",
        "key": "attention",
        "func": transform_items_subset,
    },
    {
        "type": "json",
        "url": "topics_news.json",
        "key": "topics",
        "func": transform_items_topics,
    },
    {
        "type": "json",
        "url": "spiderplot_news.json",
        "key": "topics_by_media_source",
        "func": transform_items_none,
    },
]

twitter = [
    {
        "type": "js",
        "url": "urls.js",
        "key": "urls",
        "func": partial(transform_items_js, keys=["text", "count"]),
    },
    {
        "type": "json",
        "url": "spiderplot.json",
        "key": "hashtags_by_party",
        "func": transform_items_none,
    },
    {
        "type": "json",
        "url": "hashtags.json",
        "key": "hashtags",
        "func": transform_items_subset,
    },
    {
        "type": "json",
        "url": "CSU.json",
        "key": "hashtags",
        "func": transform_items_subset,
        "party": "CSU",
    },
    {
        "type": "json",
        "url": "SPD.json",
        "key": "hashtags",
        "func": transform_items_subset,
        "party": "SPD",
    },
    {
        "type": "json",
        "url": "CDU.json",
        "key": "hashtags",
        "func": transform_items_subset,
        "party": "CDU",
    },
    {
        "type": "json",
        "url": "AfD.json",
        "key": "hashtags",
        "func": transform_items_subset,
        "party": "AfD",
    },
    {
        "type": "json",
        "url": "FDP.json",
        "key": "hashtags",
        "func": transform_items_subset,
        "party": "FDP",
    },
    {
        "type": "json",
        "url": "Gruenen.json",
        "key": "hashtags",
        "func": transform_items_subset,
        "party": "Gruenen",
    },
    {
        "type": "json",
        "url": "Linke.json",
        "key": "hashtags",
        "func": transform_items_subset,
        "party": "Linke",
    },
]
