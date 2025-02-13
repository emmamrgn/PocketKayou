# Pocket-Kayoo

## Description

Ce bot met automatiquement à jour les rôles sur votre serveur Discord en fonction des subs Twitch. Il attribue des rôles en fonction de si un utilisateur est sub à une ou deux chaînes Twitch spécifiques. Il renvoie également le rank valorant de l'utilisateur.

- **les_subs**: Attribué si un utilisateur est abonné à l'une des chaînes Twitch spécifiées.
- **super_subs**: Attribué si un utilisateur est abonné aux deux chaînes Twitch spécifiées.

## Fonctionnalités

- Réponse à une commande qui renvoie le rang du joueur.
- Attribution et retrait automatiques des rôles en fonction des abonnements Twitch.
- Journalisation des changements de rôles, du statut du bot et de la vérification des membres.
- Commande de vérification manuelle des rôles.
- Commande ping simple pour vérifier la latence du bot.

## Commandes

- `k!rank [tagvlr#id]` : Renvoie le rank du joueur
- `k!verifier_roles [membre]`: Vérifier et mettre à jour manuellement les rôles pour un membre spécifique ou pour l'émetteur de la commande si aucun membre n'est spécifié.
- `k!ping`: Vérifier la latence du bot.

## Journalisation

Le bot journalise les événements importants tels que les appels aux commandes, les changements de rôles, le statut du bot et la vérification des membres dans un canal Discord spécifié.


## Développeur
Ce projet a été développé par [emmamrgn](https://github.com/emmamrgn).

