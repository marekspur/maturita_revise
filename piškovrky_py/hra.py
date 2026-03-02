# ----------------
# IMPORT KNIHOVEN
# ----------------

import random
import math

# ------------------------
# INICIALIZACE PROMĚNNÝCH
# ------------------------

VELIKOST = 5
POCET_VITEZNYCH = 3

PRAZDNE_POLE = " "
HRAC = "X"
AI = "O"

#--------------
# HERNÍ LOGIKA
#--------------

def vytvor_pole():
     # Vytorí prázdné pole o velikosti VELIKOST x VELIKOST
     return[[PRAZDNE_POLE for _ in range(VELIKOST)] for _ in range(VELIKOST)]

def zobraz_pole(pole):
     # Vypíše aktuální stav pole do konzole
     print("\n  " + " ".join(str(i) for i in range(VELIKOST)))
     for i, row in enumerate(pole):
         # Vypíše řádek s číslem a oddělí ho vodorovnou čarou
         print(str(i) + " " + " ".join(row))
         if i < VELIKOST - 1:
             print("  " + "- " * (2*VELIKOST - 1))
     print()

def zikej_prazdne_bunky(pole):
    # Vrátí seznam všech prázdných pozic na poli
    return [(r, c) for r in range(VELIKOST) for c in range(VELIKOST) if pole[r][c] == PRAZDNE_POLE]


def kontrola_vyhry(pole, symbol):
    # Zkontroluje, zda hráč s daným symbolem vyhrál
     for r in range(VELIKOST):
        # Kontrola řádků
        for c in range(VELIKOST - POCET_VITEZNYCH + 1):
            # Kontrola řádku pro symbol hráče
            if all(pole[r][c+i] == symbol for i in range(POCET_VITEZNYCH)):
                # Pokud jsou všechny buňky v řádku stejné jako symbol hráče,
                return True

     for c in range(VELIKOST):
        # Kontrola sloupců
        for r in range(VELIKOST - POCET_VITEZNYCH + 1):
            # Kontrola sloupce pro symbol hráče
            if all(pole[r+i][c] == symbol for i in range(POCET_VITEZNYCH)):
                # Pokud jsou všechny buňky ve sloupci stejné jako symbol hráče,
                return True
     for r in range(VELIKOST - POCET_VITEZNYCH + 1):
        # Kontrola diagonál
        for c in range(VELIKOST - POCET_VITEZNYCH + 1):
            # Kontrola diagonály zleva doprava (↘) a zprava doleva (↙)
            if all(pole[r+i][c+i] == symbol for i in range(POCET_VITEZNYCH)):
                # Kontrola diagonály zleva doprava (↘)
                return True
            if all(pole[r+i][c+POCET_VITEZNYCH-1-i] == symbol for i in range(POCET_VITEZNYCH)):
                # Kontrola diagonály zprava doleva (↙)
                return True

     return False


def konec_remizou(pole):
    # Zkontroluje, zda je hra remízová (žádný hráč nevyhrál a nejsou žádné volné pozice)
    return not zikej_prazdne_bunky(pole)


# ---------------------------------
# AI - JEDNODUCHÁ (BEZ STRATEGIE )
# ---------------------------------

def ai_jednoducha(pole):
    # Jednoduchá AI, která náhodně vybírá z prázdných pozic
    return random.choice(zikej_prazdne_bunky(pole))


# ---------------------------------
# AI - STŘEDNÍ (BLOKOVÁNÍ A VÝHRY)
# ---------------------------------

def ai_stredni(pole):
    # Střední AI, která nejprve zkontroluje, zda může vyhrát, a pokud ne, zkontroluje, zda musí blokovat hráče
     for r, c in zikej_prazdne_bunky(pole):
        # Zkusí umístit symbol AI na prázdné pole a zkontroluje, zda by AI vyhrála. Pokud ano, vrátí tento tah pro vítězství.
        pole[r][c] = AI
        if kontrola_vyhry(pole, AI):
            pole[r][c] = PRAZDNE_POLE
            return (r, c)
        pole[r][c] = PRAZDNE_POLE
     for r, c in zikej_prazdne_bunky(pole):
        # Zkusí umístit symbol hráče na prázdné pole a zkontroluje, zda by hráč vyhrál. Pokud ano, vrátí tento tah pro blokování.
        pole[r][c] = HRAC
        if kontrola_vyhry(pole, HRAC):
            pole[r][c] = PRAZDNE_POLE
            return (r, c)
        pole[r][c] = PRAZDNE_POLE
     return ai_jednoducha(pole)


# -------------------------------------------
# AI - TĚŽKÁ (MINIMAX S ALFA-BETA OŘEZÁVÁNÍM)
# -------------------------------------------

def posuzovani(pole):
    # Posuzovací funkce pro Minimax algoritmus, která vrací skóre pro dané pole
    if kontrola_vyhry(pole, AI):
        # Pokud AI vyhrála, vrátí kladné skóre
        return 10
    if kontrola_vyhry(pole, HRAC):
        # Pokud hráč vyhrál, vrátí záporné skóre
        return -10
    return 0


def minimax(pole, hloubka, alfa, beta, maximalizace):
    # Minimax algoritmus s alfa-beta ořezáváním pro rozhodování AI
    skore = posuzovani(pole)

    if abs(skore) == 10 or hloubka == 0 or konec_remizou(pole):
        # Pokud je dosaženo konce hry (výhra, prohra, remíza) nebo maximální hloubky, vrátí se skóre
        return skore

    if maximalizace:
        # Maximalizující hráč (AI) se snaží získat co nejvyšší skóre
        max_hodnota = -math.inf
        for r, c in zikej_prazdne_bunky(pole):
            # Pro každý možný tah AI zkusí umístit svůj symbol, zavolá minimax rekurzivně pro další tah a poté vrátí pole do původního stavu
            pole[r][c] = AI
            posud = minimax(pole, hloubka - 1, alfa, beta, False)
            pole[r][c] = PRAZDNE_POLE
            max_hodnota = max(max_hodnota, posud)
            alfa = max(alfa, posud)
            if beta <= alfa:
                break
        return max_hodnota
    else:
        min_posud = math.inf
        for r, c in zikej_prazdne_bunky(pole):
            # Pro každý možný tah hráče zkusí umístit jeho symbol, zavolá minimax rekurzivně pro další tah a poté vrátí pole do původního stavu
            pole[r][c] = HRAC
            posud = minimax(pole, hloubka - 1, alfa, beta, True)
            pole[r][c] = PRAZDNE_POLE
            min_posud = min(min_posud, posud)
            beta = min(beta, posud)
            if beta <= alfa:
                break
        return min_posud


def ai_tezka(pole):
    # Těžká AI, která používá Minimax algoritmus s alfa-beta ořezáváním pro výběr nejlepšího tahu
    nejlepsi_skore = -math.inf
    nejlepsi_tah = None

    for r, c in zikej_prazdne_bunky(pole):
        # Pro každý možný tah AI zkusí umístit svůj symbol, zavolá minimax pro získání skóre a poté vrátí pole do původního stavu
        pole[r][c] = AI
        skore = minimax(pole, 4, -math.inf, math.inf, False)
        pole[r][c] = PRAZDNE_POLE

        if skore > nejlepsi_skore:
            # Pokud získané skóre je lepší než nejlepší skóre, aktualizuje nejlepší skóre a nejlepší tah
            nejlepsi_skore = skore
            nejlepsi_tah = (r, c)

    return nejlepsi_tah


# -----------
# HLAVNÍ HRA
# -----------

def ziskej_ai_tah(pole, obtiznost):
    # Vrátí tah AI na základě zvolené obtížnosti
    if obtiznost == "1":
        # Pokud je zvolena obtížnost 1 (JEDNODUCHÁ), použije jednoduchou AI, která náhodně vybírá z prázdných pozic.
        return ai_jednoducha(pole)
    elif obtiznost == "2":
        # Pokud je zvolena obtížnost 2 (STŘEDNÍ), použije střední AI, která nejprve zkontroluje, zda může vyhrát, a pokud ne, zkontroluje, zda musí blokovat hráče.
        return ai_stredni(pole)
    else:
        # Pokud je zvolena obtížnost 3 (TĚŽKÁ), použije těžkou AI, která používá Minimax algoritmus s alfa-beta ořezáváním pro výběr nejlepšího tahu.
        return ai_tezka(pole)


def main():
    # Hlavní funkce, která řídí průběh hry
    pole = vytvor_pole()

    obtiznost = input("Zvol obtížnost (1=Jednoduchá, 2=Střední, 3=Těžká): ")

    while True:
        # Zobrazí aktuální stav pole a požádá hráče o zadání řádku a sloupce pro svůj tah.
        zobraz_pole(pole)

        r = int(input("Řádek: "))
        c = int(input("Sloupec: "))

        if pole[r][c] != PRAZDNE_POLE:
            # Pokud je zadaná pozice již obsazená, informuje hráče a požádá o zadání jiného tahu.
            print("Pole je obsazené!")
            continue

        pole[r][c] = HRAC

        if kontrola_vyhry(pole, HRAC):
            # Pokud hráč vyhrál, zobrazí pole a oznámí vítězství hráče, poté ukončí hru.
            zobraz_pole(pole)
            print("Vyhrál jsi!")
            break

        if konec_remizou(pole):
            # Pokud je hra remízová, zobrazí pole a oznámí remízu, poté ukončí hru.
            print("Remíza!")
            break

        r, c = ziskej_ai_tah(pole, obtiznost)
        pole[r][c] = AI
        print(f"AI hraje: {r}, {c}")

        if kontrola_vyhry(pole, AI):
            # Pokud AI vyhrála, zobrazí pole a oznámí vítězství AI, poté ukončí hru.
            zobraz_pole(pole)
            print("AI vyhrála!")
            break

        if konec_remizou(pole):
            # Pokud je hra remízová, zobrazí pole a oznámí remízu, poté ukončí hru.
            print("Remíza!")
            break


if __name__ == "__main__":
    # Spustí hlavní funkci, pokud je tento skript spuštěn jako hlavní program.
    main()