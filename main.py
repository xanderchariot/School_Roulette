import json
import random
nazwa_klasy = input('podaj nazwę klasy:(n.p.: 1A, 2B) ')
klasa = ''+nazwa_klasy+'.json'
with open(klasa, 'r', encoding='utf-8') as f:
    uczniowie = json.load(f)
obecni = []
do_odpowiedzi = []
def czy_obecny():
    while len(uczniowie) != 0:
        losowany = random.choice(list(uczniowie.keys()))
        uczen = uczniowie[losowany]
        tak_nie = input(f"Czy {uczen['imie']} {uczen['nazwisko']} jest obecny? (y/n) ")
        if tak_nie.lower() == 'y':
            obecni.append(uczen)
            uczniowie.pop(losowany)
        elif tak_nie.lower() == 'n':
            uczniowie.pop(losowany)
        else:
            print('Podaj poprawną odpowiedź!')
            continue
    print("Lista obecnych:")
    for uczen in obecni:
        print(f"{uczen['imie']} {uczen['nazwisko']}")
def losuj():
    if len(obecni) <= 0:
        print('Niema osób do odpowiedzi!')
    else:
        while True:
            print(f"Ilość obecnych = {len(obecni)}")
            ile_losowac = int(input("ile uczniów pójdzie do odpowiedzi? "))
            if ile_losowac <= 0:
                print("Podałeś zamałą liczbę!")
                continue
            elif ile_losowac > len(obecni):
                print("Podałeś zadużą liczbę!")
                continue
            else:
                while len(do_odpowiedzi) != ile_losowac:
                    odpowiada  = random.choice(obecni)
                    do_odpowiedzi.append(odpowiada)
                print("Odpowiada:")
                for uczen in do_odpowiedzi:
                    print(f"{uczen['imie']} {uczen['nazwisko']}")
            break
czy_obecny()
losuj()