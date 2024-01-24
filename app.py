from flask import Flask, request, jsonify
import weaviate

app = Flask(__name__)

# Initialize Weaviate client
weaviate_url = "https://vinci3-863qlivv.weaviate.network"
api_key = "OWND9kyZDCVZG9MOa31Z7rZ8FA2v0PPIJe4T"

client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=weaviate.AuthApiKey(api_key=api_key),
    additional_headers={
        "X-HuggingFace-Api-Key": "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"  # Replace with your inference API key
    }
)

@app.route('/')
def query_handler():
    # Retrieve query parameters from the request
    query_word = request.args.get('query')
    limit = int(request.args.get('limit', 1))  # Default limit is 1 if not provided
    # Perform a text-based similarity search with the query word
    query_result = (
        client.query
        .get("ImageStroke", ["nameOfImage", "strokeOfImage"])
        .with_near_text({
            "concepts": [query_word]
        })
        .with_limit(limit)
        .do()
    )

    # Extract relevant information from the query result
    response_data = []
    for result_object in query_result.get('data', {}).get('Get', {}).get('ImageStroke', []):
        # Append the entire imageStroke array to the response
        response_data.append(result_object)
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
