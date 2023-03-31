# Brief 8

## Chapitre 1 : Déployer un cluster AKS
    
### Créer un cluster AKS avec 1 node

Connexion azure CLI
``az login``

Création d'un groupe de ressource
``az group create --name B8Celia --location francecentral``

Création du cluster AKS avec 1 nodes et la clé SSH de l'utilisateur dans le groupe de ressource
``az aks create -g B8Celia -n AKSCluster --node-count 1 --ssh-key-value ./.ssh/id_rsa.pub --enable-managed-identity -a ingress-appgw --appgw-name B8Gateway --appgw-subnet-cidr "10.225.0.0/16"``

Téléchargement des informations d’identification et configuration de l’interface de ligne de commande Kubernetes
``az aks get-credentials --resource-group B8Celia --name AKSCluster``

Créer 2 namespaces
``kubectl create namespace qal``
``kubectl create namespace prod``

## Chapitre 2 : Installation sur la VM Jenkins

Connexion à la VM
```consol=
ssh celia@vmjenkins.francecentral.cloudapp.azure.com
```

Installation de Java (nécessaire pour Jenkins)
```consol
sudo apt update
sudo apt install openjdk-17-jdk openjdk-17-jre
java -version
```
Ajout de la clé Jenkins
```consol
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
```
Utilisation du repository Jenkins
```consol
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
```
Mise à jour : ATTENTION TAILLE VM + 2vCPU pour que Jenkins fonctionne
```consol
sudo apt-get update
sudo apt-get install jenkins
```

Mot de passe administrateur pour se connecter à Jenkins
```consol
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Installation de azure CLI
```consol
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login
```

Installation de kubectl
```consol
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
Test de connexion et merge au cluster en tant que client jenkins
```consol
kubectl version --client
sudo -iu jenkins
az login
az aks get-credentials --resource-group B8Celia --name AKSCluster
exit
```

Installation de git
```consol
sudo apt update
sudo apt install git
git --version
```

Installation de jq
```consol
sudo apt update
sudo apt install jq
jq --version
```

Installation de Docker : https://docs.docker.com/engine/install/debian/

Jenkins en sudo
```consol
sudo su    
visudo -f /etc/sudoers
jenkins ALL= NOPASSWD: ALL
```

Installation kubectx/kubens
```consol
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
```

Installation pip

``sudo apt install -y python3-pip``

Installation requests-toolbelt
``pip install requests-toolbelt``

Installation de parallel
``sudo apt install parallel``

## Chapitre 3 : Configuration de Jenkins

Installation de plugins : 
*pipeline, workspace cleanup, github, docker, docker pipeline*

Ajout de credentials : 
- docker pour docker hub

## Chapitre 4 : Création de DNS pour chaque environnement

Création d’un enregistrement DNS pointant vers l’adresse IP de l’application sur Gandi : http://vote.simplon-celia.space

![](https://i.imgur.com/eXNRs5q.png)

## Chapitre 5 : Pipeline

```code
pipeline {
    agent any 
    environment {
        DOCKERHUB_CREDENTIALS=credentials('dockerhubaccount')
    }
    stages {
        stage('Cloning the git') {
            steps {
                sh('''
                git clone https://github.com/Simplon-CeliaOuedraogo/Brief8-celia.git
                ''')
            }
        }
        stage('Build image') {
            steps {
                sh('''
                    cd Brief8-celia
                    sudo docker build -t vote-app .
                ''')
            }
        }
        stage('Login and Push image on DockerHub') {
            steps {
                sh('''
                    echo $DOCKERHUB_CREDENTIALS_PSW | sudo docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                    cd Brief8-celia
                    PATCH=\044(cat azure-vote/main.py | grep -E "^ver = \\"[0-9.]+\\"\\$"|awk -F\\" {'print $2'})
                    sudo docker tag vote-app celiaoued/vote-app:\044PATCH
                    sudo docker push celiaoued/vote-app:\044PATCH
                ''')
            }
        }
        stage('Change tag yaml and launch vote site') {
            steps {
                    sh('''
                    git clone https://github.com/Simplon-CeliaOuedraogo/brief7-yaml.git app
                    TAG=\044(curl -sSf https://registry.hub.docker.com/v2/repositories/celiaoued/vote-app/tags |jq '."results"[0]["name"]'| tr -d '"')
                    sed -i "s/TAG/\044{TAG}/" ./app/vote.yaml
                    kubectl apply -f ./app
                    ''')
            }
        }
        stage('Test de charge') {
            steps {
                sh('''seq 250 | parallel --max-args 0  --jobs 20 "curl -k -iF 'vote=Jenkins' http://vote.simplon-celia.space."
                ''')
            }
        }
    }
    post {
        always {
            // Nettoyage de l'espace de travail Jenkins
            step([$class: 'WsCleanup'])
            // Deconnexion Docker
            sh 'docker logout'
        }
    }
}
```
