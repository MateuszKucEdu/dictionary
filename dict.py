import csv
import os
import difflib


# Zakładam, że każde słowo w danym języku może mieć kilka znaczeń
# Stąd pewne założenia przy konstrukcji tej funkcji.
def populate_dict(file):
    tmp_list = []
    with open(file,'r',encoding="utf-8") as data:
        for line in csv.reader(data): #csv.reader tworzy tablicę wyrazów na podstawie słów oddzielonych przecinkami
            key = line.pop(0) # zakładam, że pierwsze słowo jest z języka bazowego, dlatego używam funckji pop() która zwraca mi dany element i usuwa go z listy
            dict_from_line = {key:line} # tworzę słownik gdzie kluczem jest słowo np pl a value lista pozostałych z pliku csv słów ang
            tmp_list.append(dict_from_line)
    return tmp_list # ostatecznie funkcja zwraca listę słowników


def find_pl_word(dict_list):
    word = str(input("Wprowadź poszukiwnay wyraz: "))
    con = False # potrzebna jest dodatkowa zmienna która pozwoli wyjść z podwójnej pętli, w pythonie nie da się tego aż tak łatwo zrobić
    list_of_similar_words = [] # Nie zakładam z góry przy przetwarzaniu o jakie słowo mogło chodzić użytkownikowi tylko tworzę listę prawdopodobnych trafień która jest zwracana na koniec
    for element in dict_list: #
        for k,v in element.items():
            if word.lower() == k: # szukam polskich słów, więc przeszukuję elementy pod kątem key ze słownika
                print(word,"po angielsku: ")
                print("\t".join([str(value) for value in v])) # valeu zawsze jest listą więc przy zwracaniu wyniku iteruje jeszcze po tej liście
                con = True
                break
            elif difflib.SequenceMatcher(None,word.lower(),k).ratio() > 0.7:
                list_of_similar_words.append(k)

            if word.lower() in v: #dodatkowy warunek, jeżeli user wprowadził słowo ang (które znajduje się w słowniku) a korzysta z translatora pl -> ang to podpowiadamy, żeby skorzystał z odwrotnej wersji
                print("Wprowadziłeś ang słowo, skorzystaj z wersji tłumacza ang -> pl")
                con = True
                break
            # Moduł difflib pozwala porównywać dwa stringi i oszacować ich podobieństwo, fucnkja ratio() zwraca wartość pomiędzy 0 a 1
            # zakładamy, że przy podobieństwie 0.7 mogło userowi chodzić o podobne słowo z naszego słownika


        if con:
            break
    else:
        print("Przepraszmay, nie zanelźliśmy takiego słowa.")
    if list_of_similar_words:
        print("Za to udało nam się znaleźć podobne. Czy chodziło Ci o:")
        for i in list_of_similar_words:
            print(i)

def find_eng_word(dict_list):
    word = str(input("Wprowadź poszukiwnay wyraz: "))
    list_of_similar_words = []
    con = False
    for element in dict_list:
        for k,v in element.items():
            if word.lower() == k:
                print(word, "po angielsku: ")
                print("\t".join([str(value) for value in v]))
                con = True
                break
            elif difflib.SequenceMatcher(None, word.lower(), k).ratio() > 0.7:
                list_of_similar_words.append(k)

            if word.lower() in v:
                print("Wprowadziłeś słowo pl, skorzystaj z wersji tłumacza pl -> ang")
                con = True
                break
        if con:
            break
    else:
        print("Przepraszmay, nie zanelźliśmy takiego słowa.")

    if list_of_similar_words:
        print("Za to udało nam się znaleźć podobne. Czy chodziło Ci o:")
        for i in list_of_similar_words:
            print(i)

def main():
    dict_pl_file = os.path.abspath("C:/Users\mat\dict\pl.csv")
    dict_eng_file = os.path.abspath("C:/Users\mat\dict\eng.csv")
    dict_pl_list = populate_dict(dict_pl_file)
    dict_eng_list = populate_dict(dict_eng_file)
    while(True):
        print("\n----------------------------------------------------------------------------------\n")
        print("Witaj w programie translator\n Program umożliwia tłumaczenie wyrażeń technichnicnzych z języka ang na pl i odwrotnie")
        print("1. Tłumacz z języka ang -> pol")
        print("2. Tłumacz z języka pol -> ang")
        print("3. Zakończ działanie programu")
        wybor = input("Dokonaj wyboru: ")

        if wybor == "1":
            find_eng_word(dict_eng_list)
        if wybor == "2":
            find_pl_word(dict_pl_list)
        if wybor == "3":
            exit()


if __name__ == "__main__":
    main()
