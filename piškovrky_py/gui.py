# ----------------
# IMPORT KNIHOVEN
# ----------------
import tkinter as tk
from tkinter import messagebox

# ------------------------
# INICIALIZACE PROMĚNNÝCH
# ------------------------
from hra import (
    vytvor_pole,
    kontrola_vyhry,
    konec_remizou,
    ziskej_ai_tah,
    HRAC,
    AI,
    PRAZDNE_POLE,
    VELIKOST
)

# ------------------
# GRAFICKÉ ROZHRANÍ
# ------------------
class PiskvorkyGUI:

    def __init__(self):
        # Vytvoří hlavní okno a inicializuje herní pole a tlačítka
        self.root = tk.Tk()
        self.root.title("Piškvorky 5x5")

        self.pole = vytvor_pole()
        self.obtiznost = "3"  # default těžká

        self.tlacitka = []

        self.vytvor_menu()
        self.vytvor_mrizku()

    # -------------------
    # MENU OBTÍŽNOSTI
    # -------------------

    def vytvor_menu(self):
        # Vytvoří menu pro výběr obtížnosti
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Label(frame, text="Obtížnost:").pack(side=tk.LEFT)

        self.obt_var = tk.StringVar(value="3")

        obtiznosti = [
            ("Jednoduchá", "1"),
            ("Střední", "2"),
            ("Těžká", "3")
        ]

        for text, value in obtiznosti:
            # Vytvoří radiobutton pro každou obtížnost a při změně volby aktualizuje proměnnou obtiznost
            tk.Radiobutton(
                frame,
                text=text,
                variable=self.obt_var,
                value=value,
                command=self.zmen_obtiznost
            ).pack(side=tk.LEFT)

    def zmen_obtiznost(self):
        # Aktualizuje proměnnou obtiznost na základě zvolené radiobutton
        self.obtiznost = self.obt_var.get()

    # -----------
    # MŘÍŽKA 5x5
    # -----------

    def vytvor_mrizku(self):
        # Vytvoří mřížku 5x5 pomocí tlačítek a uloží je do seznamu tlacitka pro pozdější aktualizaci
        frame = tk.Frame(self.root)
        frame.pack()

        for r in range(VELIKOST):
            # Pro každý řádek vytvoří seznam tlačítek a uloží je do self.tlacitka pro pozdější aktualizaci textu tlačítek
            row = []
            for c in range(VELIKOST):
                # Vytvoří tlačítko pro každou buňku, které při kliknutí zavolá funkci tah_hrace s příslušnými souřadnicemi
                btn = tk.Button(
                    frame,
                    text=" ",
                    width=4,
                    height=2,
                    font=("Arial", 20),
                    command=lambda r=r, c=c: self.tah_hrace(r, c)
                )
                btn.grid(row=r, column=c)
                row.append(btn)
            self.tlacitka.append(row)

    # ----------
    # TAH HRÁČE
    # ----------

    def tah_hrace(self, r, c):
        # Pokud je buňka již obsazena, neumožní hráči provést tah
        if self.pole[r][c] != PRAZDNE_POLE:
            return

        self.pole[r][c] = HRAC
        self.tlacitka[r][c]["text"] = HRAC

        if kontrola_vyhry(self.pole, HRAC):
            # Pokud hráč vyhrál, zobrazí zprávu a restartuje hru
            messagebox.showinfo("Konec hry", "Vyhrál jsi!")
            self.restart()
            return

        if konec_remizou(self.pole):
            # Pokud je remíza, zobrazí zprávu a restartuje hru
            messagebox.showinfo("Konec hry", "Remíza!")
            self.restart()
            return

        self.root.after(200, self.tah_ai)

    # -------
    # TAH AI
    # -------

    def tah_ai(self):
        # Získá tah AI na základě zvolené obtížnosti a aktualizuje pole a tlačítka podle tahu AI
        r, c = ziskej_ai_tah(self.pole, self.obtiznost)

        self.pole[r][c] = AI
        self.tlacitka[r][c]["text"] = AI

        if kontrola_vyhry(self.pole, AI):
            # Pokud AI vyhrála, zobrazí zprávu a restartuje hru
            messagebox.showinfo("Konec hry", "AI vyhrála!")
            self.restart()
            return

        if konec_remizou(self.pole):
            # Pokud je remíza, zobrazí zprávu a restartuje hru
            messagebox.showinfo("Konec hry", "Remíza!")
            self.restart()

    # --------
    # RESTART
    # --------

    def restart(self):
        self.pole = vytvor_pole()
        for r in range(VELIKOST):
            # Pro každý řádek a sloupec nastaví text tlačítka zpět na prázdný, aby se vizuálně resetovala mřížka
            for c in range(VELIKOST):
                # Nastaví text tlačítka zpět na prázdný, aby se vizuálně resetovala mřížka
                self.tlacitka[r][c]["text"] = " "

    def spust(self):
        # Spustí hlavní smyčku GUI, která umožní interakci s uživatelem a aktualizaci zobrazení
        self.root.mainloop()


if __name__ == "__main__":
    # Vytvoří instanci třídy PiskvorkyGUI a spustí hlavní smyčku GUI
    app = PiskvorkyGUI()
    app.spust()