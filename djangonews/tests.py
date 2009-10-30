import unittest
from django.test import TestCase
from django.test.client import Client

from djangonews import models

class NewsTest(TestCase):
    
    fixtures = ['djangonews/test_fixtures.json', 'test_fixtures', 'test_fixtures.json']

    def setUp(self):
        self.client = Client()

    def test_featured_article(self):
        response = self.client.get(
            '/news/articles/2009/oct/30/featured-article/'
        )
        self.assertEqual(response.status_code, 200)

    def test_normal_article(self):
        response = self.client.get(
            '/news/articles/2009/oct/30/not-featured-article/'
        )
        self.assertEqual(response.status_code, 200)

    def test_article_listing(self):
        response = self.client.get('/news/articles/')
        self.assertEqual(response.status_code, 200)

    def test_category_listing(self):
        response = self.client.get('/news/categories/more-news/')
        self.assertEqual(response.status_code, 200)

    def test_main(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
