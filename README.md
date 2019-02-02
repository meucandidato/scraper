# Meu Candidato Scraper

Projeto voltado para raspagem de várias fontes de dados dos candidatos registrados no TSE

## Instalação

1. Faça o checkout do projeto:

```shell
$ git clone https://github.com/meucandidato/scraper.git meucandidato-scraper
```

2. Crie o ambiente virtual e instale as dependências:

```shell
$ cd meucandidato-scraper
$ python3 -m venv .venv
```

```shell
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

3. Rode o spider desejado. Nesse exemplo irei buscar notícias do _Michel Temer_ no portal do G1.

```shell
$ scrapy crawl g1_news -a keywords="Michel Temer"
```

Ele irá captura o título da notícia, link para o conteúdo da notícia, entre outros. Segue um exemplo de como é salvo no MongoDB:

```json
{
  "_id": ObjectId("59e7e862d5cb43c2b970eafe"),
  "url": "http://g1.globo.com/globo-news/jornal-globo-news/videos/v/rodrigo-maia-cancela-viagem-para-evitar-novo-atrito-com-michel-temer/6227466/",
  "posted_at": ISODate("2017-10-18T21:20:50.748Z"),
  "title": "Rodrigo Maia cancela viagem para evitar novo atrito com Michel Temer",
  "image": "http://s03.video.glbimg.com/160x100/6227466.jpg",
  "summary": "...Com a proximidade da votação, no plenário da Câmara, da segunda denúncia contra    , o presidente da Ca...",
  "portal_name": "Jornal GloboNews edição das 18h",
  "search_origin": "G1"
}
```
