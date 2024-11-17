import subprocess

def run_API_news():
    try:
        subprocess.run(['python', 'C:/Users/33672/OneDrive/Documents/GitHub/Projet_EDD/script/getAPI.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")

def run_API_fin():
    try:
        subprocess.run(['python', 'C:/Users/33672/OneDrive/Documents/GitHub/Projet_EDD/script/getAPI_fin.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script : {e}")

# Test des fonctions
run_API_news()
run_API_fin()
