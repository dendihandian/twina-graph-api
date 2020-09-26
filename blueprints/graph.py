import networkx as nx
from flask import Blueprint, jsonify, request
from components.http_client import http_client
from config.firebase import fb_db_base_url


graphApi = Blueprint('graph', __name__)


@graphApi.route('/graph/analysis', methods=['POST'])
def graphAnalysis():

    body = request.get_json()

    graph = http_client.get(fb_db_base_url + body['graph_path'] + ".json")

    graph = graph.json()

    G = nx.Graph()

    G.add_nodes_from([(screen_name, graph['nodes'][screen_name])
                      for screen_name in graph['nodes']])

    G.add_edges_from([
        (
            graph['edges'][source_target]['source'],
            graph['edges'][source_target]['target'],
            graph['edges'][source_target]
        )
        for source_target in graph['edges']
    ])

    return jsonify({
        'message': 'Analyzing graph',
        'analysis': {
            'clustering': nx.clustering(G),
        }
        # 'graph': graph.json()['nodes']
    })
