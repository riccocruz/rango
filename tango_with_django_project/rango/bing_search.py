import json
import requests


# Add your Microsoft Key to a file called bing.key
def read_bing_key():
    """
    Reads the Bing API key from a file called bing.key

    :return: string which is either None, ie no key found, or key
        remember to put bing.key in your .gitignore file to avoid committing it.

    See Python Anti-Patterns - it is an awesome resource to improve your python code
    Here we using "with" when opening documents
    http://bit.ly/twd-antipattern-open-files
    """
    bing_api_key = None

    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline().strip()
    except:
        try:
            with open('../bing.key') as f:
                bing_api_key = f.readline().strip()
        except:
            raise IOError('bing.key file not found')

    if not bing_api_key:
        raise KeyError('Bing key not found')

    return bing_api_key


def run_query(search_terms):
    """
    See the Microsoft's documentation on other parameters that you can set.
    http://bit.ly/twd-bing-api

    1.  Prepares the URL we're requesting.
    2.  Prepare authentication, making use of API key.
    3.  Response is parsed into dict using json package.
    4.  Loop through each of the results, populating the results dict.
    5.  List of dict is returned.

    :param search_terms: query of type string
    :return: results of type list
    """

    bing_key = read_bing_key()
    search_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'
    headers = {'Ocp-Apim-Subscription-Key': bing_key}
    params = {'q': search_terms, 'textDecorations': True, 'textFormat': 'HTML'}

    # Issue the request, given the details above.
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # With the response now in play, build up a Python list.
    results = []
    for result in search_results['webPages']['value']:
        results.append({'title': result['name'], 'link': result['url'], 'summary': result['snippet']})

    return results


def main():
    # Alternative solution for terminal-based interaction. DM.
    search_terms = input("Enter your query terms: ")
    results = run_query(search_terms)

    for result in results:
        print(result['title'])
        print(result['link'])
        print(result['summary'])
        print('===============')


if __name__ == '__main__':
    main()