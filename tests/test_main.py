import pytest
import os
import json
import subprocess
import shutil

# ==============================================================================
# 🎛️ PARTIE 1 : CONFIGURATION ET SCÉNARIOS (À modifier selon l'application)
# ==============================================================================

DATASET_TEST = "eeg" 


CONFIG_DE_BASE = {
    "eog": "None",
    "ecg": "None",
    "bads": "None",
    "include": "None",
    "misc": "None",
    "rm_flat": True,
    "events_as_annotations": True
}

# LES SCÉNARIOS : Ecrire les parametres que l'on souhaite modifier
# Format : ("Nom du scénario", {dictionnaire_des_modifications}, Doit_reussir_bool)
SCENARIOS = [
    (
        "1. Exécution Vanilla (Tout par défaut)", 
        {},  # Dictionnaire vide : on garde 100% de la CONFIG_DE_BASE
        True
    ),
    (
        "2. Exclusion de canaux (Bads)", 
        {"bads": "D101,D102"}, # Écrase uniquement la clé "bads"
        True
    ),
    (
        "3. Combinaison complexe (Include + Rm_flat désactivé)", 
        {
            "include": "DIN1,DIN2", 
            "rm_flat": False
        }, 
        True
    ),
    (
        "4. Test de sécurité (Negative testing sur canal inexistant)", 
        {"include": "CANAL_INVALIDE"}, 
        False # MNE doit planter, le test est donc réussi si le code d'erreur n'est pas 0
    )
]

# ==============================================================================
# ⚙️ PARTIE 2 : LE MOTEUR UNIVERSEL BRAINLIFE (Ne change jamais)
# ==============================================================================

@pytest.fixture
def dataset():
    """Vérifie la présence du fichier source avant de lancer la batterie de tests."""
    if not os.path.exists(DATASET_TEST):
        pytest.skip(f"Fichier '{DATASET_TEST}' manquant. Test ignoré.")
    return DATASET_TEST

def nettoyer():
    """Nettoie l'espace de travail pour éviter la pollution entre les scénarios."""
    for element in ['config.json', 'out_dir', 'product.json']:
        if os.path.exists(element):
            shutil.rmtree(element) if os.path.isdir(element) else os.remove(element)

@pytest.mark.parametrize("nom_test, modifs_scenario, doit_reussir", SCENARIOS)
def test_application_dynamique(dataset, nom_test, modifs_scenario, doit_reussir):
    """Moteur de test qui fusionne la base et le scénario, puis simule BrainLife."""
    # 1. Préparation d'un terrain propre
    nettoyer()

    # 2. Fusion (Base + Surcharge du scénario)
    config_finale = {"egi": dataset}
    config_finale.update(CONFIG_DE_BASE)   # Ajout de toutes les valeurs par défaut
    config_finale.update(modifs_scenario)  # Écrasement avec les valeurs du scénario
    
    # 3. Génération du fichier de configuration attendu par BrainLife
    with open('config.json', 'w') as f:
        json.dump(config_finale, f)

    # Simulation de BrainLife : création du dossier de sortie attendu
    os.makedirs('out_dir', exist_ok=True)

    # 4. Exécution de l'application en boîte noire
    resultat = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    
    # 5. Assertions selon les standards de la plateforme
    if doit_reussir:
        assert resultat.returncode == 0, f"Plantage inattendu ({nom_test}):\n{resultat.stderr}"
        assert os.path.exists(os.path.join('out_dir', 'raw.fif')), "Fichier raw.fif manquant."
        assert os.path.exists('product.json'), "Fichier product.json manquant."
    else:
        assert resultat.returncode != 0, f"L'application aurait dû planter ({nom_test})."

    # 6. Nettoyage final
    nettoyer()