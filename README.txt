🧪 Injection Lab - Laboratoire de Vulnérabilités Web Conteneurisé

Bienvenue dans l'**Injection Lab** ! Ce dépôt contient un environnement de formation complet composé de **55 applications web vulnérables** (Python, PHP, Node.js) conteneurisées via Docker. Il est conçu pour vous permettre de vous entraîner à identifier et exploiter un large éventail de failles de sécurité, de l'OWASP Top 10 aux techniques avancées.

---

## 🛠️ Prérequis : Installation des Outils

Avant de commencer, vous devez installer deux outils essentiels : **Git** et **Docker**.

### 1. Installation de Git
Git est nécessaire pour télécharger le code source du projet.

```bash
# Pour les systèmes basés sur Debian/Ubuntu
sudo apt update
sudo apt install git -y

# Pour les systèmes basés sur Red Hat/Fedora
sudo dnf install git -y
2. Installation de Docker et Docker ComposeDocker est le moteur qui va faire tourner toutes les applications, et Docker Compose est l'outil qui les orchestre. Suivez les instructions officielles sur le site de Docker pour l'installation complète.
Correction des Permissions (Important !)Après l'installation de Docker, vous devez ajouter votre utilisateur au groupe docker pour éviter d'utiliser sudo à chaque commande. Vous devez vous déconnecter et vous reconnecter après cette étape.
Bash sudo usermod -aG docker $USER
(Si vous ne voulez pas vous reconnecter, vous devrez utiliser sudo devant toutes les commandes docker compose.)


🚀 Guide de DéploiementSuivez ces étapes pour lancer l'intégralité du laboratoire en quelques minutes.

Étape 1 : Cloner le DépôtOuvrez votre terminal et téléchargez le projet :
git clone [https://github.com/Geraldo568/injection_lab.git](https://github.com/Geraldo568/injection_lab.git)
cd injection_lab
Étape 2 : Construction des Images DockerCette étape lit le fichier docker-compose.yml et construit les 55 images d'application. Cela peut prendre plusieurs minutes la première fois.
docker compose build
Étape 3 : Lancer le LaboratoireDémarrez tous les services en mode détaché (-d). Si la commande échoue, essayez d'ajouter sudo devant (sudo docker compose up -d).
docker compose up -d
Étape 4 : Vérification du Statut
Vérifiez que tous les conteneurs sont en cours d'exécution 
(State: running) :
docker compose ps
🌐 Accès aux LaboratoiresLe laboratoire est accessible localement sur votre machine (via localhost ou 127.0.0.1).

Chaque labo est mappé sur un port unique.

Labo N° Description 

(Exemple )Port d'Accès

1. Advanced SQL Injection http://localhost:8080

2. NoSQL Injection http://localhost:8081

7. Server-Side Request Forgery http://localhost:8086 

 Insecure Deserialization http://localhost:8126.........

Consultez le fichier docker-compose.yml pour la liste complète et les ports associés (de 8080 à 8134).

🛑 Arrêt et NettoyageLorsque vous avez terminé votre session, vous pouvez utiliser ces commandes depuis le répertoire injection_lab/ :

CommandeAction 
docker compose stop, Arrête tous les conteneurs (ils peuvent être redémarrés avec up -d).

docker compose down, Arrête et supprime les conteneurs et réseaux.

docker compose down --volumes Arrête, supprime les conteneurs, les réseaux ET les volumes (suppression définitive des données de MongoDB/MySQL).


📜 Contribution Si vous trouvez un bug ou souhaitez ajouter un nouveau labo, n'hésitez pas à créer une Issue ou à soumettre une Pull Request !Hackez de manière responsable ! 🛡️
