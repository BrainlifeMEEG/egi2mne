import pytest
import os
import json
import subprocess

@pytest.fixture
def chemin_mini_dataset():
    """
    Vérifie que le mini dataset de Max est bien là.
    """
    chemin = "C:\\Ecole Lucaïna\\ENSC\\ICM Stage\\eeg" # On suppose qu'il sera à la racine pour l'instant
    if not os.path.exists(chemin):
        pytest.skip(f"Fichier '{chemin}' introuvable. En attente du dataset de Max.")
    return chemin

def preparer_config(chemin_egi, include_val):
    """Fonction utilitaire pour créer le config.json avant de lancer l'app"""
    config_data = {
        "egi": chemin_egi,
        "include": include_val
    }
    with open('config.json', 'w') as f:
        json.dump(config_data, f)
        
    # S'assurer que le dossier de sortie existe (comme sur BrainLife)
    os.makedirs('out_dir', exist_ok=True)

def test_conversion_complete(chemin_mini_dataset):
    """
    TEST 1 : Vérifie que le script tourne avec l'option 'include' par défaut ('None')
    """
    preparer_config(chemin_mini_dataset, "None")
    
    # On lance main.py comme si on était dans le terminal
    resultat = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    
    # Assertions : Le script n'a pas planté et les fichiers sont là
    assert resultat.returncode == 0, f"Le script a planté avec l'erreur : {resultat.stderr}"
    assert os.path.exists(os.path.join('out_dir', 'raw.fif')), "Le fichier raw.fif n'a pas été créé"
    assert os.path.exists(os.path.join('out_dir', 'report.html')), "Le rapport HTML n'a pas été créé"
    assert os.path.exists('product.json'), "Le product.json n'a pas été créé"

def test_option_include_specifique(chemin_mini_dataset):
    """
    TEST 2 : Le fameux "Code coverage" demandé par Max !
    On vérifie le comportement si on demande de n'inclure que certains canaux.
    """
    # Attention: Remplacer E1, E2 par des noms de canaux qui existent vraiment dans le mini dataset de Max
    preparer_config(chemin_mini_dataset, "E1,E2")
    
    resultat = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    
    assert resultat.returncode == 0, f"Le script a planté avec l'option include : {resultat.stderr}"
    # Si on voulait aller plus loin, on pourrait ouvrir out_dir/raw.fif avec mne et compter les canaux !