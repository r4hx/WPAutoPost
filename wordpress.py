#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
import logging
import os

import requests

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Wordpress:
    """
    Класс для работы с api wordpress
    """

    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.api = f"{self.url}/wp-json/wp/v2"
        self.credentials = f"{self.username}:{self.password}"
        self.token = base64.b64encode(self.credentials.encode())
        self.headers = {
            "Authorization": "Basic " + self.token.decode("utf-8"),
        }

    def upload_image(
        self, url: str, title: str, description: str
    ) -> requests.Response.json:
        """
        Загрузка изображения
        """
        self.url = url
        self.title = title
        self.description = description
        self.alt_text = description
        self.caption = title
        self.filename = os.path.basename(url)
        with open(self.filename, "wb") as self.f:
            self.response = requests.get(self.url, headers=self.headers)
            assert self.response.status_code == 200, "Error download cover image"
            self.f.write(self.response.content)
        self.response = requests.post(
            f"{self.api}/media",
            headers=self.headers,
            files={"file": open(self.filename, "rb")},
        )
        os.remove(self.filename)
        if self.response.status_code != 201:
            logging.debug(self.response.json())
            assert (
                self.response.status_code == 201
            ), "Post article in wordpress exception error"
        return self.response.json()

    def create_post(
        self,
        title: str,
        content: str,
        excerpt: str,
        featured_media: str,
        status="draft",
    ) -> requests.Response.json:
        """
        Создание публикации
        """
        self.title = title
        self.status = status
        self.content = content
        self.excerpt = excerpt
        self.featured_media = featured_media
        self.data = {
            "title": self.title,
            "status": self.status,
            "content": self.content,
            "excerpt": self.excerpt,
            "categories": 475,
            "featured_media": self.featured_media,
        }
        self.response = requests.post(
            f"{self.api}/posts", headers=self.headers, json=self.data
        )
        assert self.response.status_code == 201
        return self.response.json()

    def save_url_in_cache(self, url: str):
        """
        Сохранение обработанного url в локальном кеше
        """
        self.url = url
        with open("cached.txt", "+a") as self.f:
            self.f.write(f"{self.url}\n")
        logging.info(f"Url {self.url} saved in cache")
