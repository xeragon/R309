# SAE_R309

## Guide d'utilisation

### Serveur

tous les fichiers sont contenu dans le dossier /serveur

#### Configuration

le fichier config.json (/serveur/config.json)
contient les configurations des serveurs esclaves, vous pouvez editer les config existente ou ajouter des entrées.

Cette config sera utilisée par le serveur principal et le script de lancement
des serveur esclaves

#### Serveurs esclaves

Il y a deux façons de lancer les serveurs esclaves

- soit un par un avec la commande ```python3 WorkerServer.py -h <addrese> -p <port> -n <nom> ```
- ou bien a partir du fichier de config avec le script workersStarter.py qui lis le contenu du fichier *config.json* et lance les serveurs esclaves correspondant.
<br>
Utiliser la commande ```python3 workersStarter.py``` 
<br>
<br>
<strong> /!\ Attention /!\ </strong> Selon la version de python que vous utilisez il vous sera peut etre nécessaire d'utiliser ```python``` au lieu de ```python3``` et de modifier la commande ligne 7 dans workersStarter.py et la ligne 74 dans WorkerServer.py pour utiliser votre commande python (python, python3, py.exe , etc...)    
<br>
workersStarter.py : ligne 7 ```os.system(f"<votre commande python> WorkerServer.py -h {host} -p {port} -n {name}")```
<br> WorkerServer.py : ligne 74 ```s = subprocess.run(["python",filename],capture_output=True,encoding="locale")```

#### Serveur principal
pour lancer le serveur principal utiliser la commande ```python3 MainServ.py -h <addresse> -p <port> ```

le serveur utilisera le fichier *config.json* afin de se connecter au serveurs esclaves contenu dans la config, dès qu'une connexion a été établie avec au moins un esclave le serveur est prêt a recevoir les connexion des client

si une tentatives de connexion à un esclaves à échoué alors le serveur principal retenteras une connexion toute les 3 secondes jusqu'au succès.

### Client
Tous les fichiers sont contenu dans le dossiers /client 

si vous n'avez pas encore la librairie PyQT5 d'installer alors installer la avec la commande ``` pip install pyqt5 ``` 
lancer simplement le client avec ``` python3 client.py ```

une fois le client lancer vous pouvez entrer l'addresse et le port du serveur principale et vous y connecter, vous pourrez ensuite uploader un fichier en python, java ou C.
<br>
En cliquant sur un élément dans la liste des fichiers uploadés, un dialog avec les informations sur l'execution s'ouvre


### Démo

[lien démo](https://www.youtube.com/watch?v=Su0BZYSm3tA)