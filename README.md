# News-Scrapper
Baixa e extraí conteúdo de uma lista de sites de notícias

* get_pages.py - lê o arquivo de configuração e baixa o conteúdo alternadamente, criando uma pasta por site e um arquivo por artigo
* get_text.py - extrai o texto do html baseado no seletor passado, cria uma nova pasta com todos os conteúdos
* config.yaml - configurações

**lista_noticias_link** e **text** são seletores em CSS.
**lista_noticias** e **noticias** são urls com um parâmetro `{index}` que é substituído por números inteiros.

Utilizar **noticias** se a url final do artigo puder ser iterada diretamente por algum índice.
Utilizar **lista_noticias** caso a página anterior às notícias possa ser iterada e especifique o seletor para os links das notícias em **lista_noticias_link**.
