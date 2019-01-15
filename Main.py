import requests
import collections
from nltk.corpus import stopwords

class Request:
    def __init__(self, nome):
        self.url = 'https://api.vagalume.com.br/'+nome+'/index.js'
        self.api = requests.get(self.url)
        self.art = self.api.json()

class Req_musicas:
    def __init__(self,id):
        self.key = 'db9ae52c02ff42f16c5e2ab5c1479108'
        self.url2 = 'https://api.vagalume.com.br/search.php?musid='+id+'&apikey={'+self.key+'}'
        self.api2 = requests.get(self.url2)
        self.musica_api = self.api2.json()

class Get_artista:
    def __init__(self, api):
        self.artista_id = api.art['artist']['id']
        self.nome_art = api.art['artist']['desc']
        self.url = api.art['artist']['url']
        self.pic_small = api.art['artist']['pic_small']
        self.pic_medium = api.art['artist']['pic_medium']

class Get_ranking:
    def __init__(self, api):
        self.rank = api.art['artist']['rank']
        #print(self.rank)

    def get_rank(self):
        return self.rank['pos']

class Get_genre:
    def __init__(self, api):
        self.list_genres = api.art['artist']['genre']

    def get_genre_names(self):
        self.genres = []

        for genre in self.list_genres:
            self.genres.append(genre['name'])

        return self.genres

class Get_toplyrics:
    def __init__(self, api):
        self.list_toplyrics = api.art['artist']['toplyrics']['item']

    def get_n_toplyrics(self, n):
        self.toplyrics = []

        for toplyric in self.list_toplyrics:
            self.toplyrics.append(toplyric['desc'])

        if n <= len(self.toplyrics):
            return self.toplyrics[0:n]
        else:
            return self.toplyrics

    def mais_frequentes(self, n):

        #obtem os ids das musicas
        self.ids = []

        self.copia = self.list_toplyrics[0:n]
        for toplyric in self.copia:
            self.ids.append(toplyric['id'])

        #gera a api a partir dos ids
        self.api_musicas = []

        for id in self.ids:
            self.api_musicas.append(Req_musicas(id))

        #gera uma lista com as letras
        self.letras = []
        for so_letras in self.api_musicas:
            self.letras.append(so_letras.musica_api["mus"][0]["text"])

        #separa as letras em palavras
        self.palavras = []
        for uma_musica in self.letras:
            self.palavras.append(uma_musica.lower().replace('(', '').replace(')', '').replace('!', '').replace('?', '').split())

        #junta as palavras das musicas em uma lista só
        self.lista_palavras = []
        for temp in self.palavras:
            for cada_palavra in temp:
                self.lista_palavras.append(cada_palavra)

        #filtra as palavras
        stop_words_eng = set(stopwords.words('english'))
        stop_words_pt = set(stopwords.words('portuguese'))

        filtered_sentence = [w for w in self.lista_palavras if not w in stop_words_eng]
        filtered_sentence = []
        for w in self.lista_palavras:
            if w not in stop_words_eng:
                filtered_sentence.append(w)

        filtered_sentence1 = [w for w in filtered_sentence if not w in stop_words_pt]
        filtered_sentence1 = []
        for w in filtered_sentence:
            if w not in stop_words_pt:
                filtered_sentence1.append(w)

        colecao = collections.Counter(filtered_sentence1)

        return colecao.most_common(10)

class Get_albuns:
    def __init__(self, api):
        self.list_albuns = api.art['artist']['albums']['item']

    def get_albuns(self):
        self.albuns = []

        for album in self.list_albuns:
            self.albuns.append(album['desc'])

        return self.albuns

    def last_album(self):
        self.get_albuns()
        return self.albuns[0]

nome = input("Nome do artista: ")
n=5

try:
    artista = Request(nome)

    print("Ranking: ")
    rank = Get_ranking(artista)
    print(rank.get_rank())

    print("Genero(s): ")
    genero = Get_genre(artista)
    print(genero.get_genre_names())

    print("Albuns: ")
    albuns = Get_albuns(artista)
    print(albuns.get_albuns())

    print("Ultimo Album:")
    print(albuns.last_album())

    print(str(n)+" mais ouvidas: ")
    toplyric = Get_toplyrics(artista)
    print(toplyric.get_n_toplyrics(n))

    print("10 Palavras mais frequentes das "+str(n)+" musicas mais populares")
    print(toplyric.mais_frequentes(n))

except:
   print("Erro no nome do artista")
