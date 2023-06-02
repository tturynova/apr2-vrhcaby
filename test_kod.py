import random 

class Hra:
    def __init__(self, hrac1, hrac2):
        self.hrac1 = hrac1
        self.hrac2 = hrac2
        self.herni_pole = HerniPole()
        self.dvojkostka = Dvojkostka()
        self.bar = Bar()
        self.konec_hry = False
        self.vitez = None
        self.na_tahu = hrac1

    def hraj(self):
        while not self.konec_hry:
            hody_kostkou = self.dvojkostka.hod()
            while hody_kostkou != []:
                self.herni_pole.vypis_pole()
                print(self.bar)
                print("")
                print("kostky :" + str(hody_kostkou))
                tah_hrace = self.na_tahu.tahni(self.herni_pole, hody_kostkou, self.bar)
                self.herni_pole.proved_tah(tah_hrace, self.na_tahu)
                if self.herni_pole.je_konec_hry():
                    self.konec_hry = True
                    self.vitez = self.na_tahu
                    break

            if self.na_tahu is self.hrac1:
                self.na_tahu = self.hrac2
            else:
                self.na_tahu = self.hrac1

        self.zobraz_vysledky()
    
    def zobraz_vysledky(self):
        print("Vítěz: ", self.vitez.jmeno)
        print("Stav herního pole: ", self.herni_pole.stav())

class HerniPole:
    def __init__(self):
        self.pole = [0] * 24
        self.pole[0] = 2
        self.pole[5] = -5
        self.pole[7] = -3
        self.pole[11] = 5
        self.pole[12] = -5
        self.pole[16] = 3
        self.pole[18] = 5
        self.pole[23] = -2
        self.bar = Bar()
     
    def vypis_pole(self):
        vertical_space = max(map(abs, self.pole))
        start = 11
        end = -1
        step = 1
        start2 = 0
        end2 = vertical_space
        border = 5
        print(" 12 11 10  9  8  7     6  5  4  3  2  1")
        print("╔═══════════════════╤════════════════════╗")
        for j in range(2):
            for i in range(start2, end2, step):
                print("║ ", end="")
                for index in range(start, end, -step):
                    if index == border:
                        print("│", end="  ")
                    if abs(self.pole[index]) > i:
                        if self.pole[index] > 0:
                            print("X", end="  ")
                        elif self.pole[index] < 0:
                            print("O", end="  ")
                    else:
                        print("∙", end="  ")
                else:
                    print("║")
            if j == 0:
                print("║                   │                    ║")
            start = 12
            end = 24
            step = -1
            start2 = vertical_space - 1
            end2 = -1
            border = 18
        print("╚═══════════════════╧════════════════════╝")
        print(" 13 14 15 16 17 18    19 20 21 22 23 24")

    def vypis_pole2(self):
        for i, pole in enumerate(self.pole):
            print(i, pole)

    def proved_tah(self, tah, hrac):
        if not self.je_povoleny_tah(tah):
            raise ValueError("Neplatný tah")
        if self.bar.vrat_pocet_kamenu() > 0:
            pozice = tah[1] - 1
            self.pole[pozice] += 1
            self.bar.odeber_kamen(hrac.barva)
        else:
            pozice_od = tah[0]
            pozice_do = tah[1]
            if self.pole[pozice_od] <= 0 or self.pole[pozice_do] < -1:
                raise ValueError("Neplatný tah")
            self.pole[pozice_od] -= 1
            if self.pole[pozice_do] == -1:
                self.pole[pozice_do] = 1
                self.bar.pridej_kamen(hrac.barva)
            else:
                self.pole[pozice_do] += 1

        #self.na_tahu = (self.na_tahu + 1) % 2
                      
    def mozne_tahy(self, bar, kostky):
        tahy = set()
        for hod in kostky:
            if bar.vrat_pocet_kamenu() > 0:
                if self.pole[hod - 1] >= -1:
                    tahy.add((0, hod))
            for pozice in range(24):
                if self.pole[pozice] > 0:
                    nova_pozice = pozice + hod
                    if nova_pozice < 24 and self.pole[nova_pozice] >= -1:
                        tahy.add((pozice + 1, nova_pozice + 1))
        return list(tahy)

    def je_povoleny_tah(self, tah):
        if len(tah) == 0:
            return False
        if self.bar.vrat_pocet_kamenu() > 0:
            return tah[0] == 0 or tah[0] == 1
        for pozice in range(24):
            if self.pole[pozice] > 0:
                nova_pozice = pozice + tah[0]
                if nova_pozice < 24 and self.pole[nova_pozice] >= -1:
                    return True
        return False

    def je_konec_hry(self):
        pocet_kamenu_v_cili = sum(self.pole[18:])
        if pocet_kamenu_v_cili == 15:
            return True
        return all(kamen <= 0 for kamen in self.pole[:18])
    
class Dvojkostka:
    def __init__(self):
        self.mozne_hody = [0, 1, 2, 3, 4, 5, 6]

    def hod(self):
        hod1 = random.randint(1, 6)
        hod2 = random.randint(1, 6)
        if hod1 == hod2:
            return [hod1, hod1, hod1, hod1]
        else: 
            return [hod1, hod2]
        
class Bar:
    def __init__(self):
        self.kameny = []
    
    def pridej_kamen(self, barva):
        self.kameny.append(barva)
    
    def odeber_kamen(self, barva):
        if barva in self.kameny:
            self.kameny.remove(barva)
    
    def vrat_pocet_kamenu(self):
        return len(self.kameny)
    
    def je_prazdny(self):
        return len(self.kameny) == 0
    
    def __str__(self) -> str:
        return str(self.kameny)

class HerniKamen:
    def __init__(self, pozice=-1, barva=''):
        self.pozice = pozice
        self.barva = barva
        
    def nastav_pozici(self, pozice):
        self.pozice = pozice

    def nastav_barvu(self, barva):
        self.barva = barva

class KonzolovyHrac:
    def __init__(self, jmeno, barva):
        self.jmeno = jmeno
        self.barva = barva

    def tahni(self, herni_pole, hody_kostka, bar):
        mozne_tahy = herni_pole.mozne_tahy(bar, hody_kostka)
        print("mozne tahy: " + str(mozne_tahy))
        while True:
            try:
                hod = input(f"{self.jmeno}, zadej svůj tah (oddělený mezerou): ")
                hod1, hod2 = map(int, hod.split())
                if (hod1, hod2) not in mozne_tahy:
                    raise ValueError
                #if hod1 not in dvojkostka.mozne_hody or hod2 not in dvojkostka.mozne_hody:
                #    raise ValueError
                hody_kostka.remove(abs(hod2 - hod1))
                tah = (hod1 - 1, hod2 - 1)
                # if bar.vrat_pocet_kamenu() > 0 and not herni_pole.je_povoleny_tah(tah, bar):
                #     raise ValueError
                # elif bar.vrat_pocet_kamenu() == 0 and not herni_pole.je_povoleny_tah(tah):
                #     raise ValueError
                # else:
                return tah
            except ValueError:
                print("Neplatný tah, zkus to znovu.")

class AiHrac:
    def __init__(self, jmeno, barva):
        self.jmeno = jmeno
        self.barva = barva

    def tahni(self, herni_pole, dvojkostka, bar):
        mozne_tahy = herni_pole.mozne_tahy(dvojkostka, bar)
        if not mozne_tahy:
            return None
        else:
            return self.zvol_tah(mozne_tahy)

    def zvol_tah(self, mozne_tahy):
        return mozne_tahy[0]

hrac1 = KonzolovyHrac("Hráč 1", "X")
#hrac2 = AiHrac("Ai", "X")
hrac2 = KonzolovyHrac("Hráč 2", "O")

hra = Hra(hrac1, hrac2)
hra.hraj()
