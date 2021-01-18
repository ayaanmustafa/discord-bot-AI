import requests
def get_quote():
    response = requests.get("https://twinword-word-graph-dictionary.p.rapidapi.com/association/")
    print(response)

get_quote()
