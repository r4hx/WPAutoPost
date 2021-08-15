#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
import time
from os import getenv

from macrumors import Macrumors
from neowin import Neowin
from translator import Translate
from wordpress import Wordpress

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


post_url = getenv("URL", None)
assert post_url is not None, "Please set URL"
login = getenv("LOGIN", None)
assert login is not None, "Please set LOGIN"
password = getenv("PASSWORD", None)
assert password is not None, "Please set PASSWORD"

if __name__ == "__main__":
    max_post_from_adapter = 10
    while True:
        n = Neowin()
        m = Macrumors()
        adapters = [n, m]
        for a in adapters:
            new_posts_urls = a.get_new_posts()
            t = Translate()
            w = Wordpress(post_url, login, password)
            i = 0
            for post_url in new_posts_urls:
                if i >= 10:
                    break
                try:
                    soup = a.get_context(post_url)
                    title = t.go(a.get_title(soup))
                    description = t.go(a.get_description(soup))
                    image_url = a.get_cover_image(soup)
                    content = t.go(a.get_content(soup))
                    image_upload = w.upload_image(image_url, title, description)
                    post_created = w.create_post(
                        title=title,
                        content=content,
                        excerpt=description,
                        featured_media=image_upload["id"],
                        status="publish",
                    )
                except Exception as e:
                    logging.warning(e)
                    logging.warning(sys.exc_info())
                finally:
                    w.save_url_in_cache(post_url)
                    i += 1
        logging.info("Sleep 1 hour")
        time.sleep(60 * 60 * 1)
