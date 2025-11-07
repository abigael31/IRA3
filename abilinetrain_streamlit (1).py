# abilinetrain_streamlit.py
# Streamlit GUI "AbilineTrain" (bonus)
# Pour lancer: streamlit run abilinetrain_streamlit.py

import streamlit as st
from typing import Dict, Set, Tuple
import uuid
import json

st.set_page_config(
    page_title="AbilineTrain",
    page_icon="logo.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

#  Thème rose via CSS additionnel
PINK = "#ff2e88"
CSS = f"""
<style>
:root {{
  --abiline-pink: {PINK};
}}
/* Titres & accents */
h1, h2, h3, .st-emotion-cache-10trblm, .st-emotion-cache-15hul6a {{
  color: var(--abiline-pink) !important;
}}
/* Boutons */
.stButton > button {{
  border-radius: 999px;
  border: 2px solid var(--abiline-pink);
  background: white;
  color: var(--abiline-pink);
  font-weight: 700;
}}
.stButton > button:hover {{
  background: var(--abiline-pink);
  color: white;
}}
/* Badges style "ticket" */
.badge {{
  display:inline-block;
  padding: .25rem .6rem;
  border-radius: 999px;
  border: 1px solid var(--abiline-pink);
  color: var(--abiline-pink);
  font-weight:600;
  font-size:.85rem;
}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

#  Données en mémoire (session) 
if "trains" not in st.session_state:
    st.session_state.trains: Dict[str, Dict[str, object]] = {
    'ANGERS-PARIS': {'places_total': 80, 'places_restantes': 80, 'passagers': set()},
    'TURIN-ROME': {'places_total': 65, 'places_restantes': 65, 'passagers': set()},
    'BARCELONE-MADRID': {'places_total': 55, 'places_restantes': 55, 'passagers': set()},
    'LYON-SAINT TROPEZ' :{'places_total': 55, 'places_restantes': 55, 'passagers': set()},
    }

trains = st.session_state.trains

def reserver_place(nom: str, code: str):
    code = code.strip().upper()
    if code not in trains:
        return False, "Trajet introuvable."
    info = trains[code]
    if info['places_restantes'] <= 0:
        return False, "Train complet."
    if nom in info['passagers']:
        return False, "Ce passager a déjà une réservation sur ce trajet."
    numero_place = info['places_total'] - info['places_restantes'] + 1
    info['passagers'].add(nom)
    info['places_restantes'] -= 1
    ticket = (nom, code, numero_place)
    st.session_state["last_ticket"] = ticket
    return True, f"Réservation confirmée pour {nom} place n°{numero_place}."

def annuler_reservation(nom: str, code: str):
    code = code.strip().upper()
    if code not in trains:
        return False, "Trajet introuvable."
    info = trains[code]
    if nom not in info['passagers']:
        return False, "Réservation introuvable pour ce passager sur ce trajet."
    info['passagers'].remove(nom)
    info['places_restantes'] += 1
    return True, f"Réservation annulée pour {nom} sur {code}."

def header():
    col1, col2 = st.columns([1, 3])  # Créez deux colonnes pour l'image et le titre
    with col1:
        st.image("logo.png", width=100)  # Affichez l'image avec une largeur de 100 pixels
    with col2:
        st.markdown(f"## **AbilineTrain**")
     
def vue_trajets():
    st.subheader("Trajets disponibles")
    for code, info in trains.items():
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            st.markdown(f"**{code}**")
        with col2:
            st.markdown(f"<span class='badge'>{info['places_restantes']} / {info['places_total']}</span>", unsafe_allow_html=True)
        with col3:
            if info['places_restantes'] == 0:
                st.markdown("<span class='badge'>Complet</span>", unsafe_allow_html=True)

def vue_reserver():
    st.subheader("Réserver une place")
    with st.form("form_resa"):
        nom = st.text_input("Nom du passager", "")
        code = st.selectbox("Choisir un trajet", list(trains.keys()))
        ok = st.form_submit_button("Réserver")
    if ok:
        if not nom.strip():
            st.error("Veuillez saisir un nom.")
        else:
            success, msg = reserver_place(nom.strip(), code)
            (st.success if success else st.error)(msg)
            if success and "last_ticket" in st.session_state:
                nom_t, code_t, place_t = st.session_state["last_ticket"]
                st.info(f"🎫 Ticket: ({nom_t}, {code_t}, {place_t})")
                # Export JSON
                ticket_json = json.dumps({"nom": nom_t, "trajet": code_t, "place": place_t}, ensure_ascii=False, indent=2)
                st.download_button("Télécharger le ticket", data=ticket_json, file_name=f"ticket_{nom_t}_{code_t}_{place_t}.json")

def vue_annuler():
    st.subheader("Annuler une réservation")
    with st.form("form_cancel"):
        code = st.selectbox("Trajet", list(trains.keys()))
        candidats = sorted(list(trains[code]["passagers"]))
        nom = st.selectbox("Passager", [""] + candidats, index=0)
        ok = st.form_submit_button("Annuler")
    if ok:
        if not nom:
            st.error("Sélectionnez un passager.")
        else:
            success, msg = annuler_reservation(nom, code)
            (st.success if success else st.error)(msg)

def vue_passagers():
    st.subheader("Passagers par train")
    code = st.selectbox("Trajet", list(trains.keys()))
    passagers = sorted(trains[code]['passagers'])
    if passagers:
        st.markdown("**Liste triée** :")
        for p in passagers:
            st.markdown(f"- {p}")
    else:
        st.info("Aucun passager pour ce trajet.")

def vue_complets():
    st.subheader("Trains complets")
    complets = [c for c, i in trains.items() if i['places_restantes'] == 0]
    if complets:
        for c in complets:
            st.markdown(f"- **{c}**")
    else:
        st.info("Aucun train complet.")

# pour le menu déroulant
header()
action = st.sidebar.selectbox("Menu", ["Afficher les trajets", "Réserver", "Annuler", "Passagers", "Trains complets"])
# st.sidebar.markdown(f"**Thème** : rose {PINK}")

if action == "Afficher les trajets":
    vue_trajets()
elif action == "Réserver":
    vue_reserver()
elif action == "Annuler":
    vue_annuler()
elif action == "Passagers":
    vue_passagers()
elif action == "Trains complets":
    vue_complets()
