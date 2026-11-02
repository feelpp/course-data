#import "paper.typ": *
#show: doc => paper("Fiche de TP · Covariance, Pearson et première validation", doc)
= Des couples à la covariance
*Fiche étudiant · 20 octobre 2026 · travail en binôme*

Poursuivre le notebook #link("https://feelpp.github.io/course-data/course-data/foundations/statistical-exploration.html")[Statistical Exploration]. Conserver ses imports et la table `air`. Échanger la personne au clavier au milieu de chaque TP. Les notations sont celles des diapositives ; les noms de colonnes et l’API Python restent inchangés.

== A. Préparer, calculer, expliquer — 25 min
1. Choisir PM2.5 et PM10. Une paire doit provenir de la même station et de la même heure. Retenir les couples complets, puis annoncer leur nombre $n$.
2. Prévoir le signe du lien, puis tracer le nuage. Décrire sa forme ; ne pas commencer par le coefficient.
3. Calculer les moyennes des deux colonnes retenues, les écarts centrés et leurs produits. Construire explicitement la covariance avant de comparer avec pandas sur *les mêmes lignes*.

$ s_(x y) = 1/(n-1) sum_(i=1)^n (x_i-overline(x))(y_i-overline(y)) $

#callout[*Jalons* : à 5 min, montrer la table appariée et son effectif ; à 10 min, montrer le nuage et votre prédiction du signe. Finir en expliquant une contribution négative.]

== Au tableau : compléter les quatre couples inventés
$x$ est mesuré en heures, $y$ en points. Calculer les deux moyennes, puis compléter :

#tab((0.4fr,0.6fr,0.6fr,1fr,1fr,1fr), th[$i$],th[$x_i$],th[$y_i$],th[$x_i-overline(x)$],th[$y_i-overline(y)$],th[Produit],
[1],[1],[1],[…],[…],[…], [2],[2],[3],[…],[…],[…], [3],[3],[2],[…],[…],[…], [4],[4],[4],[…],[…],[…])

== Configuration graphique fournie
```python
paired = None  # À construire : deux colonnes, couples complets.
# Remplacer les ... par vos colonnes préparées, puis décommenter.
# fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
# ax.scatter(..., ..., s=12, alpha=0.3, edgecolors="none")
# ax.set(xlabel="PM2.5 (µg/m³)", ylabel="PM10 (µg/m³)",
#        title=f"Couples station-heure : n={len(paired)}")
# ax.grid(alpha=0.2)
```

*Restitution* : un nuage légendé, $n$, une covariance avec son unité et deux phrases reliant le signe au nuage. Une valeur inhabituelle doit être examinée, pas supprimée automatiquement.

#pagebreak()
= De la covariance à Pearson
== A2. Une matrice sur un sous-ensemble commun — 16 min
Choisir PM2.5, PM10 et WSPM. Retenir les lignes où les trois mesures sont disponibles. Noter $X$ le tableau numérique à $n$ lignes et 3 colonnes.

$ m_j = 1/n sum_(i=1)^n X_(i j) quad C_(i j)=X_(i j)-m_j quad S=(C^T C)/(n-1) $

```python
columns = ["PM2.5", "PM10", "WSPM"]
common = None  # Sélectionner les colonnes et les lignes complètes.
X = None       # Construire le tableau NumPy à n lignes et 3 colonnes.
m = None       # Une moyenne par colonne : axis=0.
C = None       # Centrer les colonnes.
S = None       # Calculer la matrice, avant common.cov().
# .T : transposée ; @ : produit matriciel.
```

Vérifier les dimensions, la symétrie et les variances de la diagonale sur *ce même sous-ensemble*. Donner les unités de $S_(1 1)$, $S_(1 2)$ et $S_(1 3)$.

#callout[Les indices mathématiques commencent à 1 ; ceux de NumPy commencent à 0. Ainsi $S_(1 3)$ s’écrit #box[`S[0, 2]`]. Pourquoi la variance WSPM calculée sur toutes les lignes disponibles ne constitue-t-elle pas le bon contrôle ici ?]

== B. Enlever les échelles, puis interpréter — 20 min
1. Reprendre *exactement les couples du TP A*. Calculer leurs deux écarts-types avec `ddof=1`, puis construire Pearson à partir de votre covariance.
2. Comparer avec pandas sur les mêmes lignes. Convertir une variable par un facteur positif : prédire et vérifier les effets sur la covariance, l’écart-type et Pearson.
3. Refaire l’analyse pour le couple attribué : TEMP/PRES ou PM2.5/WSPM. Lire le nuage avant de commenter le coefficient.

$ r_(x y) = s_(x y)/(s_x s_y) $

#tab((1.2fr,0.6fr,1.4fr,0.6fr), th[Couple],th[$n$],th[Covariance et unité],th[Pearson],
[PM2.5 / PM10],[…],[…],[…], [Couple attribué],[…],[…],[…])

*Restitution* : la matrice $S$ avec ses étiquettes, un contrôle de sa diagonale, le tableau de couples, une explication de l’invariance d’unité et une limite de Pearson.

*Lecture de matrice* : sur les mêmes lignes, construire $Z_(i j)=C_(i j)/s_j$ avec $s_j=sqrt(S_(j j))$, puis $R=(Z^T Z)/(n-1)$. Une carte de couleurs doit fixer l’échelle de −1 à 1 et être accompagnée des effectifs ; elle ne remplace pas les nuages.

#pagebreak()
= Première séparation et validation
== C. Une règle constante apprise sur le passé — 20 min
À la fin du 10 mars 2013, on doit annoncer PM2.5 pour les 11–12 mars aux mêmes stations. Commencer par une règle constante, apprise uniquement sur le passé.

#tab((0.7fr,1.1fr,1.8fr),th[Mars 2013],th[Rôle],th[Lignes / cibles valides / manquantes],
[1–10],[Apprentissage],[… / … / …], [11–12],[Validation],[… / … / …], [13–14],[Réserve],[Ne pas utiliser ici])

Les périodes sont fixées ; les calculs restent à faire :
```python
t = pd.to_datetime(air[["year", "month", "day", "hour"]])
train = air.loc[t < "2013-03-11"]
validation = air.loc[(t >= "2013-03-11") & (t < "2013-03-13")]
# 1. Contrôler les bornes temporelles et compter les cibles disponibles.
b = None           # Médiane de PM2.5 sur l'apprentissage uniquement.
actual = None      # Cibles disponibles de validation.
predictions = None # Même constante, avec le même index que actual.
mae = None         # Erreurs absolues, puis moyenne.
```

$ b=op("médiane")(y_"apprentissage") quad hat(y)_i=b quad "MAE"_"validation"=1/(n_"val") sum_(i=1)^(n_"val") abs(y_i-hat(y)_i) $

Ici $n_"val"$ est le nombre de cibles disponibles en validation. Il est distinct de l’effectif $n$ utilisé pour les couples descriptifs.

#tab((1.2fr,1fr),th[Résultat],th[Votre valeur], [Constante apprise et unité],[…],
[Effectif $n_"val"$ et erreur avec son unité],[…], [Sens du résultat et une limite],[…])

== Questions de restitution
- Quelle question l’erreur de validation traite-t-elle que Pearson ne traite pas ?
- Que se passerait-il si la médiane utilisait les quatorze jours ?
- Le PM10 du 11 mars à midi est-il connu à l’instant de décision fixé ici ?

#callout[*Portée de l’exercice* : cet extrait a déjà été exploré. La séparation illustre des rôles ; elle ne recrée pas un test final indépendant. Pour une évaluation finale, réserver les données avant l’exploration et la sélection.]

#context [#metadata(counter(page).get().first()) <handout-page-count>]
