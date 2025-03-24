# GetAround

La société de location de voitures se demande :
1-Quel est le meilleur seuil de temps pour éviter qu’il y ait des retards entre une location et une autre ? 

2-Quel est le meilleur prix pour louer des véhicules?

La réponse à la première question se trouve sur un tableau de bord streamlit à l’adresse suivante : https://getaround-i7yrhod9paojch7ohucv8x.streamlit.app/

En ce qui concerne le prix, j’ai créé un modèle de ml (XGboost) capable de prédire le prix en fonction d’un certain nombre de variables.
À l’adresse suivante vous trouverez la documentation de l’api qui permet de faire la prédiction : https://getaround-52758a126f17.herokuapp.com/docs


## En téléchargeant le repo, vous trouverez à l’intérieur un fichier test_api.py qui vous permettra de tester l’API avec les données de votre choix et d’avoir des prédictions instantanées avec python
