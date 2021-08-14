#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Macrumors:
    def __init__(self) -> None:
        self.feed = "https://www.macrumors.com/sitemap/sitemap-post-2021.xml"
        self.cached_file = "cached.txt"
        self.cached_urls = [
            self.i.strip() for self.i in open(self.cached_file, "r").readlines()
        ]

    def get_new_posts(self) -> list:
        """
        Получить список публикаций
        """
        self.response = requests.get(self.feed)
        assert self.response.status_code == 200, "Rss feed not responsed"
        self.soup = BeautifulSoup(self.response.text, features="html.parser")
        self.all_urls = [self.i.text for self.i in self.soup.find_all("loc")]
        assert len(self.all_urls) != 0, "Feed not returned items"
        self.urls = [
            self.u for self.u in self.all_urls if self.u not in self.cached_urls
        ]
        logging.info(f"macrumors new urls: {len(self.urls)}")
        return self.urls

    def get_context(self, url: str) -> BeautifulSoup:
        """
        Получить контекст для дальнейшей обработки
        """
        self.url = url
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, features="html.parser")
        return self.soup

    def get_title(self, soup: BeautifulSoup) -> str:
        """
        Получить заголовок статьи
        """
        self.soup = soup
        self.title = self.soup.find("meta", property="og:title")
        self.title = self.title.get("content", None)
        assert self.title is not None, "Title not parsed"
        # logging.info(f"title: {self.title}")
        return self.title

    def get_description(self, soup: BeautifulSoup) -> str:
        """
        Получить описание статьи
        """
        self.soup = soup
        self.description = self.soup.find("meta", property="og:description")
        self.description = self.description.get("content", None)
        assert self.description is not None, "Description not parsed"
        # logging.info(f"description: {self.description}")
        return self.description

    def get_cover_image(self, soup: BeautifulSoup) -> str:
        """
        Получить ссылку на обложку статьи
        """
        self.soup = soup
        self.cover_image = self.soup.find("meta", property="og:image")
        self.cover_image = self.cover_image.get("content", None)
        assert self.cover_image is not None, "Cover image not parsed"
        # logging.info(f"cover image: {self.cover_image}")
        return self.cover_image

    def get_content(self, soup: BeautifulSoup) -> str:
        """
        Получить содержимое статьи
        """
        self.soup = soup
        self.text = self.soup.find("article").text
        self.text = self.text.splitlines()
        self.text = "".join(f"{self.i.strip()}\n" for self.i in self.text)
        self.text = self.text.splitlines()
        self.text = "".join(f"{self.i}\n\n" for self.i in self.text[:-1])
        assert self.text != "", "Content not parsed"
        # logging.info(f"content: {self.text}")
        return self.text
