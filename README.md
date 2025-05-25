Installation
=============

Copier le fichier `config.toml.sample` en `config.toml` et le remplir
```

pip install -e .
```

Lancement
=========

```
cd app
flask run 

# ou

gunicorn app.wsgi -b 127.0.0.1:5000
```