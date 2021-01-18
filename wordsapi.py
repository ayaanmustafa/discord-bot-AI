import requests, json
with open("api-key.txt") as f:
    api_key = f.read()
def get_word_data(word):
    url = f"https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"

    response = requests.get(url)
    json_data = json.loads(response.text)
    data1 = []
    data1.append(json_data[0]['shortdef'])
    data1.append(json_data[0]['meta']['stems'])
    data1.append(json_data[0]['meta']['syns'][0])
    return data1

