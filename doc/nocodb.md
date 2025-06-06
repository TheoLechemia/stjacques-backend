Changer le mdp "owner" de nocodb
================================

- Se rendre dans le répertoire `/home/stjacq/nocodb_data`

- ouvrir la bdd : `sqlite3 noco.db`

- executer la requete SQL (en remplaçant le mail souhaité):

::

    UPDATE nc_users_v2
    SET email='new_admin@mail.com'  --new mail
    WHERE email='old_admin@mail.com'; -- old admin mail