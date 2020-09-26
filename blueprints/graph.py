import networkx as nx
import logging
from flask import Blueprint, jsonify, request, current_app
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

    analysis = {
        'number_of_nodes': G.number_of_nodes(),
        'number_of_edges': G.number_of_edges(),
        # 'clustering': nx.clustering(G),
        # 'average_clustering': nx.average_clustering(G),
        # 'square_clustering': nx.square_clustering(G),
        # 'degree_centrality': nx.degree_centrality(G),
        # 'closeness_centrality': nx.closeness_centrality(G),
        # 'betweenness_centrality': nx.betweenness_centrality(G),
    }

    try:
        # NOTE: not stored, try to debug this...
        http_client.post(fb_db_base_url +
                         body['analysis_path'] + ".json", analysis)
    except Exception as e:
        current_app.logger.error('Failed to post analysis: ' + str(e))

    return jsonify({
        'message': 'Graph analyzed',
        # 'data': analysis,
    })
