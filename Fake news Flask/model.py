from googlesearch import search
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from torch import nn

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def predict(query):
    # Set the query you want to search
    # query = "Usa invaded Iraq"
    # Set the number of results you want to retrieve
    API_KEY = "31de7c3a989d4874bd9cf7067d890c3c"

    # Set the query you want to search
    query = query
    words=query.split()

    if(len(words)>10):
        words=words[0:11]

    query=' '.join(words)

    # Set the number of results you want to retrieve
    num_results = 10

    # Set the Google News API endpoint
    endpoint = "https://newsapi.org/v2/everything"

    # Set the API key as a header in the request
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Set the request parameters
    params = {
        "q": query,
        "pageSize": num_results,
        "sortBy": "publishedAt",
        "language": "en",
        # "domains": "bbc.co.uk,cnn.com,nytimes.com,wsj.com,reuters.com,apnews.com"
    }

    # Send a GET request to the API endpoint with the headers and parameters
    response = requests.get(endpoint, headers=headers, params=params)

    # Parse the JSON content of the response
    data = response.json()

# Print the headings of the news articles

    headings = []
    for i, article in enumerate(data["articles"]):
        # Extract the URL and heading of the article
        url = article["url"]
        heading = article["title"]
        # Print the ranking number, URL, and heading of the article
        print(f"{i+1}. {url}")
        headings.append(heading)

    sentences = list()
    sentences = headings

    embeddings = list()
    map = dict()

    for i, sentence in enumerate(sentences):
        embed = model.encode(sentence, convert_to_tensor=True)
        embeddings.append(embed)

        map[sentence] = embed

    query_vector = model.encode(query, convert_to_tensor=True)

    flag = 1

    realEvaluator = list()

    d = dict()
    for i, sentence in enumerate(embeddings):
        cos = nn.CosineSimilarity(dim=0)
        cosine_similarity = cos(query_vector, sentence)
        d[sentences[i]] = cosine_similarity

    return d
