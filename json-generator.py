import requests
import json


def json_iter(url):
    '''Returns an iterator the yields jsons from the provided url.'''
    # the second parameter being "stream=True" is important
    r = requests.get(url, stream=True)
    # needs to have the right encoding
    if r.encoding is None:
        r.encoding = 'utf-8'
    for line in r.iter_lines(decode_unicode=True):
        # This is essentially going line by line in the response object's
        # content. This is why the return values need to be strings with a
        # newline "\n" at the end for the generator on the API side.
        if line:
            yield json.loads(line)






if __name__ == "__main__":
    for index, data in enumerate(json_iter("http://34.217.174.15:5000/api/data/pubmed_central/?mesh=D009202&docs=10")):
        if index < 4:
            print(data)

        else:
            break
