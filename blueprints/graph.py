import networkx as nx
import logging
import json
from flask import Blueprint, jsonify, request, current_app
from components.http_client import http_client
from config.firebase import fb_db_base_url
from config.twina_graph_api import tga_key

graphApi = Blueprint('graph', __name__)


@graphApi.route('/graph/analysis', methods=['POST'])
def graphAnalysis():

    if not request.headers['tga-key'] or request.headers['tga-key'] != tga_key:
        return jsonify({
            'message': 'Not authorized for twina graph api.'
        })

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
        # Single-Result
        'number_of_nodes': G.number_of_nodes(),
        'number_of_edges': G.number_of_edges(),
        'average_clustering': nx.average_clustering(G),

        # Nodes Analysis
        'clustering': nx.clustering(G),
        'square_clustering': nx.square_clustering(G),
        'degree_centrality': nx.degree_centrality(G),
        'closeness_centrality': nx.closeness_centrality(G),
        'betweenness_centrality': nx.betweenness_centrality(G),
    }

    for nodes_analysis in [
        'clustering',
        'square_clustering',
        'degree_centrality',
        'closeness_centrality',
        'betweenness_centrality'
    ]:
        print(analysis[nodes_analysis].keys())
        for node in analysis[nodes_analysis].keys():
            if 'analysis' not in graph['nodes'][node].keys():
                graph['nodes'][node]['analysis'] = {}

            graph['nodes'][node]['analysis'][nodes_analysis] = analysis[nodes_analysis][node]

    try:
        # post analysis
        http_client.put(fb_db_base_url +
                        body['analysis_path'] + ".json", data=json.dumps(analysis))

        # modify graph with analysis
        http_client.put(fb_db_base_url +
                        body['graph_path'] + ".json", data=json.dumps({
                            'nodes': graph['nodes'],
                            'edges': graph['edges']
                        }))

    except Exception as e:
        current_app.logger.error('Failed to post analysis: ' + str(e))

    return jsonify({
        'message': 'Graph analyzed',
        # 'data': analysis,
    })
