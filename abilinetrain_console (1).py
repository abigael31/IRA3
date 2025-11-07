# abilinetrain_console.py
# Programme console "AbilineTrain" — gestion simple de réservations de trains
# Couverture des fonctionnalités demandées dans le TP:
# 1) Afficher les trains
# 2) Réserver une place
# 3) Annuler une réservation
# 4) Afficher les passagers d’un train
# 5) Afficher les trains complets
# 6) (Bonus) Générer un ticket (tuple)

from typing import Dict, Set, Tuple

Train = Dict[str, object]

trains: Dict[str, Train] = {
    'ANGERS-PARIS': {'places_total': 80, 'places_restantes': 80, 'passagers': set()},
    'TURIN-ROME': {'places_total': 65, 'places_restantes': 65, 'passagers': set()},
    'BARCELONE-MADRID': {'places_total': 55, 'places_restantes': 55, 'passagers': set()},
    'LYON-SAINT TROPEZ' :{'places_total': 55, 'places_restantes': 55, 'passagers': set()},
}

def afficher_trains() -> None:
    print("=== TRAJETS DISPONIBLES ===")
    for code, info in trains.items():
        print(f"{code} → {info['places_restantes']} / {info['places_total']} places restantes")

def reserver_place(nom: str, code: str) -> Tuple[str, str, int] | None:
    code = code.strip().upper()
    if code not in trains:
        print("Trajet introuvable.")
        return None
    info = trains[code]
    if info['places_restantes'] <= 0:
        print("Train complet.")
        return None
    if nom in info['passagers']:
        print("Ce passager a déjà une réservation sur ce trajet.")
        return None
    # Numéro de place = places_total - places_restantes + 1 (simple)
    numero_place = info['places_total'] - info['places_restantes'] + 1
    info['passagers'].add(nom)
    info['places_restantes'] -= 1
    ticket = (nom, code, numero_place)
    print(f" Réservation confirmée pour {nom} sur {code}, place n°{numero_place}.")
    return ticket

def annuler_reservation(nom: str, code: str) -> bool:
    code = code.strip().upper()
    if code not in trains:
        print("Trajet introuvable.")
        return False
    info = trains[code]
    if nom not in info['passagers']:
        print("Réservation introuvable pour ce passager sur ce trajet.")
        return False
    info['passagers'].remove(nom)
    info['places_restantes'] += 1
    print(f"Réservation annulée pour {nom} sur {code}.")
    return True

def afficher_passagers(code: str) -> None:
    code = code.strip().upper()
    if code not in trains:
        print(" Trajet introuvable.")
        return
    passagers = sorted(trains[code]['passagers'])
    print(f"=== PASSAGERS {code} ===")
    if not passagers:
        print("(aucun passager)")
    else:
        for p in passagers:
            print(f"- {p}")

def trains_complets() -> None:
    print("=== TRAINS COMPLETS ===")
    found = False
    for code, info in trains.items():
        if info['places_restantes'] == 0:
            print(f"- {code}")
            found = True
    if not found:
        print("(aucun)")

def menu():
    while True:
        print("\n=== MENU RÉSERVATION TRAIN – AbilineTrain ===")
        print("1) Afficher les trains")
        print("2) Réserver une place")
        print("3) Annuler une réservation")
        print("4) Afficher les passagers d’un train")
        print("5) Voir les trains complets")
        print("0) Quitter")
        choix = input("Votre choix: ").strip()
        if choix == "1":
            afficher_trains()
        elif choix == "2":
            nom = input("Nom du passager: ").strip()
            code = input("Code du trajet (ex: TUN-PAR): ").strip().upper()
            reserver_place(nom, code)
        elif choix == "3":
            nom = input("Nom du passager: ").strip()
            code = input("Code du trajet: ").strip().upper()
            annuler_reservation(nom, code)
        elif choix == "4":
            code = input("Code du trajet: ").strip().upper()
            afficher_passagers(code)
        elif choix == "5":
            trains_complets()
        elif choix == "0":
            print("Au revoir")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()
