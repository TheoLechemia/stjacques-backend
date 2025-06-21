Installation
=============

Copier le fichier `config.toml.sample` en `config.toml` et le remplir
```

pip install -e .
```

Mode developpement
=================


    cd app
    flask run 

Exploitation (production)
=========================

Le service systemd `saintjacques.service` contrôle le procesus de l'application.



    # Lancer le service
    systemclt start saintjacques
    # Arreter le service
    systemclt stop saintjacques
    # Vérifier que le service fonctionne bien
    systemclt status saintjacques


Les logs de l'application se situent dans le fichier `/var/log/saintjacques/errors.log`