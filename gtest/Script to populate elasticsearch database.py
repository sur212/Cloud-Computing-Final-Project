import elasticsearch
import requests
from requests_aws4auth import AWS4Auth
from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = ''
Placename="bangalore"
attractions=[]
google_places = GooglePlaces(YOUR_API_KEY)
query_result = google_places.nearby_search(
        location=Placename,keyword='tourist attractions',types=[types.TYPE_POINT_OF_INTEREST],
        radius=200000)

if query_result.has_attributions:
    print query_result.html_attributions
    



for place in query_result.places:
    print place.name
    attractions.append(place.name)
host = ''
awsauth = AWS4Auth('', '', '', 'es')
print attractions
es = elasticsearch.Elasticsearch(
    hosts=[{'host': host, 'port': 44}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=elasticsearch.connection.RequestsHttpConnection
)
doc = {
    'country': 'India',
    'place': Placename,
    'attractionslist': attractions,
}
res = es.index(index="test-index", doc_type='test-index', body=doc)
print(res['created'])
print(es.cluster.health()['status'])