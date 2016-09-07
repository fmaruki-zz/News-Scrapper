import yaml
from pyquery import PyQuery as pq
import os

def extract_text(filename, selector):
    with open(filename) as f:
        text = f.read()
        if not text:
            return ""
        html = pq(text, parser="html")
        html.remove("script,style,link,head")
        text = ". ".join([el.text_content() or "" for el in html(selector)])
        text = text.replace(". . ", ". ")
    return text

configs = yaml.load(open("config.yaml").read())
for config in configs:
    nome = config['nome']
    print nome
    files = os.listdir(config['abrev'])
    for filename in files:
        text = extract_text(config['abrev'] + "/" + filename, config['text'])
        if text:
            with open("text/" + config['abrev'] + "/" + filename, "w") as f:
                f.write(text.encode("utf-8"))
                f.close()
