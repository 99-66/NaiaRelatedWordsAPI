import re
import pandas as pd
from elasticsearch import Elasticsearch
from app.env import ELASTICSEARCH


class ElasticsearchConnector:
    elasticsearch = ELASTICSEARCH

    def __init__(self):
        self.host = None
        self.client = self._client()
        self.text_index = self._index('TEXT_INDEX')

    @classmethod
    def _client(cls) -> Elasticsearch:
        """
        Elasticsearch client를 생성하여 반환한다

        :return:
        """
        username = cls.elasticsearch['USER']
        password = cls.elasticsearch['PASSWORD']
        if username and password:
            es = Elasticsearch(hosts=cls.elasticsearch['HOST'], http_auth=(username, password))
        else:
            es = Elasticsearch(hosts=cls.elasticsearch['HOST'])

        return es

    @classmethod
    def _index(cls, key) -> str:
        """
        Index 이름을 반환한다

        :param key:
        :return:
        """
        return cls.elasticsearch[key]

    @staticmethod
    def cleaning_text(text: str) -> str:
        """
        한글과 영문으로만 된 문장으로 변환한다

        :param text:
        :return:
        """
        cleaning_rule = re.compile('[^가-힣a-zA-Z\s]')
        return cleaning_rule.sub('', text)

    def get_related_words(self, word: str, size: int = 10000):
        """
        특정 단어와 연관된 단어가 포함된 목록을 가져온다

        :param word: '테스트'
        :param size: default 10000
        :return:
        """

        # 검색 쿼리 설정
        body = {
            "_source": [
                "words",
                "text"
            ],
            "size": size,
            "sort": [
                {
                    "createdAt": {"order": "desc"}
                }
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "words"
                            }
                        },
                        {
                            "match": {
                                "words": word
                            }
                        }
                    ]
                }
            }
        }

        # 단어가 포함된 모든 문서를 Scroll API로 읽어온다
        resp = self.client.search(index=self.text_index, body=body, scroll='1m', request_timeout=30)
        scroll_id = resp['_scroll_id']
        scroll_size = len(resp['hits']['hits'])

        result = []
        while scroll_size > 0:
            for doc in resp['hits']['hits']:
                result.append(doc['_source'])

            resp = self.client.scroll(scroll_id=scroll_id, scroll='1m', request_timeout=30)
            scroll_id = resp['_scroll_id']
            scroll_size = len(resp['hits']['hits'])

        # Scroll API를 닫는다
        self.client.clear_scroll(body={'scroll_id': scroll_id})

        # 검색 결과를 DataFrame으로 변환하여 반환한다
        return pd.DataFrame(result)

    def get_related_tweets(self, word: str, size: int = 100):
        """
        특정 단어와 연관된 단어가 트윗 목록을 가져온다

        :param word: '테스트'
        :param size: default 100
        :return:
        """

        # 검색 쿼리 설정
        body = {
            "_source": [
                "text",
                "createdAt"
            ],
            "size": size,
            "sort": [
                {
                    "createdAt": {
                        "order": "desc"
                    }
                }
            ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "exists": {
                                "field": "words"
                            }
                        },
                        {
                            "match": {
                                "words": word
                            }
                        },
                        {
                            "match": {
                                "origin": "twitter"
                            }
                        }
                    ]
                }
            }
        }

        # 단어가 포함된 문서를 읽어온다
        resp = self.client.search(index=self.text_index, body=body, request_timeout=30)
        result = [doc['_source'] for doc in resp['hits']['hits']]

        # 검색 결과를 DataFrame으로 변환하여 반환한다
        return pd.DataFrame(result)
