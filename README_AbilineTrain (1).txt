
==============================
AbilineTrain – Console & GUI
==============================

Deux versions incluses :
1) **Console** : `abilinetrain_console.py`
2) **GUI Streamlit** : `abilinetrain_streamlit.py` (bonus)

Prérequis
---------
- Python 3.10+ recommandé
- (GUI) Streamlit : `pip install streamlit`

Lancer la version console
-------------------------
```bash
python abilinetrain_console.py
```

Lancer la version Streamlit (GUI rose)
--------------------------------------
```bash
streamlit run abilinetrain_streamlit.py
```
Le thème rose est configuré par CSS dans l'app et par un fichier `config.toml`.

Fonctionnalités couvertes
-------------------------
- Afficher les trains & places restantes
- Réserver une place (avec **ticket** tuple et export JSON)
- Annuler une réservation
- Afficher les passagers triés
- Lister les trains complets

Branding
--------
- Nom d'agence : **AbilineTrain**
- Accent couleur : **rose**

Fichiers
--------
- `abilinetrain_console.py`
- `abilinetrain_streamlit.py`
- `.streamlit/config.toml`
- `README_AbilineTrain.txt`
