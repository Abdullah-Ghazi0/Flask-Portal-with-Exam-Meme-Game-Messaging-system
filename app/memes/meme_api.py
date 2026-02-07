import requests
import random

def memer():
    url = "https://www.reddit.com/r/ProgrammerHumor/top.json?limit=5&t=day"

    headers = {
        "User-Agent": "NewFlaskapp/2.0"
    }
    response = requests.get(url, headers=headers)

    data = response.json()
    memes = []

    for post in data["data"]["children"]:
        post_data = post["data"]

        post_hint = post_data.get("post_hint")
        url = post_data.get("url", "")

        is_image = (
            post_hint == "image"
            or url.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))
        )

        if is_image:
            meme_data = {"title": post_data.get("title"), "image": url}
            memes.append(meme_data)


    meme = random.choice(memes) if memes else None
    return meme
