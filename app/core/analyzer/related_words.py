import math
from typing import Dict
import pandas as pd
import networkx as nx
from apyori import apriori
from networkx.readwrite import json_graph
from app.env import SUPPORT


def word_network(df: pd.DataFrame) -> Dict:
    """
    단어와 연관된 단어들의 노드 정보를 생성하여 반환한다

    :param df:
    :return:
    """
    results = (list(apriori(df['words'], min_support=SUPPORT, max_length=2)))

    columns = ['nodes', 'support']
    ndf = pd.DataFrame(columns=columns)

    for result in results:
        if len(result.items) == 2:
            row = [result.items, result.support]
            series = pd.Series(row, index=ndf.columns)
            ndf = ndf.append(series, ignore_index=True)

    ndf.sort_values(by='support', ascending=False, inplace=True)

    return _network_data(ndf)


def _network_data(df: pd.DataFrame) -> Dict:
    """
    DataFrame을 그래프 노드, 링크로 변환하여 반환한다

    :param df:
    :return:
    """
    G = nx.Graph()
    ar = df['nodes']
    G.add_edges_from(ar)

    pr = nx.pagerank(G)
    node_size = {k: math.log(1000 * v) * 8 for k, v in pr.items()}
    node_link_data = json_graph.node_link_data(G)

    node_data = node_link_data['nodes']
    for node in node_data:
        node['name'] = node['id']
        node['_size'] = get_node_size(node_size.get(node['id'], 10))

    link_data = node_link_data['links']
    for link in link_data:
        link['sid'] = link['source']
        link['tid'] = link['target']
        del link['source']
        del link['target']

    resp_node_data = {
        'nodes': node_data,
        'links': link_data,
        'rank': pr
    }

    return resp_node_data


def get_node_size(ns: float) -> float:
    if ns < 10:
        return 10.0
    elif ns > 50:
        return 50.0
    else:
        return ns
