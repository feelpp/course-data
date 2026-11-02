// Source canonique : toutes les expressions mathématiques sont composées par Typst.
// Les blocs Python nommés sont exécutés par build.py avant la composition.
#let pairing = ```python
x = np.array([1., 2., 3., 4.])
y = np.array([1., 3., 2., 4.])
fig, axes = plt.subplots(1, 2, figsize=(10, 3.1))
for ax, yy, title in zip(axes, (y, 5-y), ("Couples A", "Couples B")):
    ax.scatter(x, yy, s=90, color=GREEN)
    ax.axvline(x.mean(), color=GREY, linestyle="--")
    ax.axhline(yy.mean(), color=GREY, linestyle="--")
    ax.set(xlabel=r"$x$ (heures)", ylabel=r"$y$ (points)", title=title)
    ax.set(xticks=[1, 2, 3, 4], yticks=[1, 2, 3, 4])
save(fig)
```

#let matrix = ```python
X = np.column_stack([x, y])
m = X.mean(axis=0)
C = X - m
S = C.T @ C / (len(X) - 1)
assert np.allclose(S, [[5/3, 4/3], [4/3, 5/3]])
record(S=S.tolist())
```

#let rescaling = ```python
X_minutes = X * np.array([60., 1.])
C_minutes = X_minutes - X_minutes.mean(axis=0)
S_minutes = C_minutes.T @ C_minutes / (len(X_minutes) - 1)
s = np.sqrt(np.diag(S))
Z = C / s
R = Z.T @ Z / (len(X) - 1)
assert np.allclose(S_minutes, [[6000, 80], [80, 5/3]])
assert np.allclose(R, [[1, .8], [.8, 1]])
assert np.allclose(R, np.corrcoef(X_minutes, rowvar=False))
record(S_minutes=S_minutes.tolist(), R=R.tolist())
fig, axes = plt.subplots(1, 2, figsize=(10, 3.1))
for ax, scale, unit in zip(axes, (1, 60), ("heures", "minutes")):
    ax.scatter(scale*x, y, color=GREEN, s=90)
    ax.set(xlabel=(r"$x$ (heures)" if scale == 1 else r"$x′$ (minutes)"),
           ylabel=r"$y$ (points)")
save(fig)
```

#let limits = ```python
fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
curve_x = np.arange(-2., 3.)
examples = [(x, y), (x, 5-y), (curve_x, curve_x**2)]
for ax, (xx, yy) in zip(axes, examples):
    r = np.corrcoef(xx, yy)[0, 1]
    ax.scatter(xx, yy, s=90, color=GREEN)
    ax.set(title=rf"$r_{{xy}}={r:.1f}$", xlabel=r"$x$", ylabel=r"$y$")
    ax.axvline(xx.mean(), color=GREY, linestyle="--")
    ax.axhline(yy.mean(), color=GREY, linestyle="--")
save(fig)
```

#let influence = ```python
u = np.array([0., 1., 2., 3., 4., 5.])
v = np.array([1., 3., 0., 4., 2., 1.])
fig, axes = plt.subplots(1, 2, figsize=(10, 3.1))
for ax, extra in zip(axes, (False, True)):
    xx = np.r_[u, 30.] if extra else u
    yy = np.r_[v, 30.] if extra else v
    ax.scatter(u, v, s=70, color=GREEN)
    if extra:
        ax.scatter([30], [30], s=100, color="#bc6734", label="point ajouté")
        ax.legend(loc="upper left", fontsize=13)
    ax.set(xlim=(-2, 33), ylim=(-2, 33), xlabel=r"$x$", ylabel=r"$y$",
           title=rf"$n={len(xx)},\ r_{{xy}}={np.corrcoef(xx, yy)[0, 1]:.2f}$")
save(fig)
```

#let lesson = json("lesson.json")
#let computed = json("generated/values.json")
#let ink = rgb("142a24")
#let green = rgb("155f46")
#let muted = rgb("50675e")
#let paper = rgb("faf8f2")
#let pale = rgb("eaf0e9")
#set document(title: lesson.title, author: "CSMI M1 · Traitement de données")
#set page(width: 13.333in, height: 7.5in,
  margin: (x: 42pt, top: 28pt, bottom: 37pt), fill: paper,
  footer: context {
    set text(size: 10pt, fill: muted)
    grid(columns: (1fr, auto, 1fr), [CSMI M1 · 20 octobre 2026],
      [#counter(page).display() / #lesson.slides.len()], align(right)[Traitement de données])
  })
#set text(font: "Arial", size: 21pt, fill: ink, lang: "fr")
#set par(leading: 0.55em, spacing: 0.6em)
#show math.equation: set text(font: "New Computer Modern Math", size: 24pt)
#show raw: set text(font: "DejaVu Sans Mono", size: 13pt)

#let frame(id, body) = {
  let slide = lesson.slides.find(s => s.id == id)
  if id != lesson.slides.first().id { pagebreak() }
  [#metadata(id) <frame-id>]
  grid(columns: (1fr, auto), text(size: 11pt, fill: green, weight: "bold", upper(slide.chapter)),
    text(size: 11pt, fill: muted, if slide.minutes == 0 { "Facultatif" } else { str(slide.minutes) + " min" }))
  v(10pt)
  text(size: if id == "opening" { 37pt } else { 30pt }, weight: "bold", slide.title)
  v(18pt)
  body
  v(1fr)
  text(size: 10pt, fill: green)[#link(lesson.publicBase + slide.page)[Référence du cours (en anglais) ↗]]
}
#let point(body) = { grid(columns: (14pt, 1fr), gutter: 5pt, text(fill: green)[•], body); v(10pt) }
#let note(body) = block(width: 100%, fill: pale, inset: 11pt, radius: 5pt)[#set text(size: 18pt); #body]
#let two(left, right) = grid(columns: (1fr, 1fr), gutter: 26pt, left, right)
#let tbl(columns, ..cells) = {
  set text(size: 18pt)
  table(columns: columns, inset: 9pt, stroke: 0.5pt + rgb("cad6cd"), ..cells)
}
#let th(body) = table.cell(fill: green)[#text(fill: white, weight: "bold", body)]
#let figure(name, height: 180pt) = align(center)[#image("generated/" + name + ".svg", width: 96%, height: height, fit: "contain")]
#let codebox(body) = block(fill: pale, inset: 10pt, radius: 5pt, width: 100%)[#body]

#frame("opening")[
  #text(size: 25pt, fill: green)[Covariance, corrélation de Pearson et première validation]
  #v(24pt)
  #point[Nous avons audité les données et décrit des variables séparément.]
  #point[Nous cherchons maintenant à comprendre comment elles varient ensemble.]
  #note[Fil conducteur : une question → un calcul simple → un graphique → une interprétation à justifier.]
]
#frame("purpose")[
  #point[*Comprendre un couple* : les mesures élevées de l’une vont-elles avec les mesures élevées de l’autre ?]
  #point[*Organiser plusieurs couples* : que résume une matrice de covariance ?]
  #point[*Comparer les associations* : pourquoi les unités obligent-elles à standardiser ?]
  #point[*En pratique* : préparer les lignes, calculer explicitement, vérifier avec pandas et expliquer les limites.]
]
#frame("route")[
  #set text(size: 17pt)
  #table(columns: (1fr, 3.6fr), inset: (x: 10pt, y: 7pt), stroke: 0.4pt + muted,
    th[Minutes], th[Question et travail],
    [0–25], [Rappel actif : observation, distribution, position et dispersion],
    [25–70], [Des couples à la covariance, puis TP A],
    [70–100], [Construire et lire une matrice, puis TP A2],
    [100–110], [Pause],
    [110–175], [Unités, standardisation, Pearson, limites et TP B],
    [175–185], [Pause],
    [185–225], [Une première validation : règle constante et TP C],
    [225–240], [Restitution individuelle et vérification de la compréhension])
  #v(12pt)
  #text(size: 17pt, fill: muted)[35 diapositives pour la séance ; 2 compléments mathématiques facultatifs. Les TP sont intercalés dans la progression.]
]
#frame("diagnostic")[
  #point[Que représente une ligne de notre table Beijing ?]
  #point[Pourquoi une mesure manquante ne vaut-elle pas zéro ?]
  #point[Que peut cacher une moyenne ? Quel graphique choisir pour le voir ?]
  #point[Changer les classes de l’histogramme change-t-il la proportion au-dessus d’un seuil fixé ?]
  #note[Sans code : seul, puis à deux. Donner une justification, pas seulement le nom d’une fonction Python.]
]
#frame("recall")[
  #point[Exemple inventé : cinq concentrations, en µg/m³.]
  $ x = (1, 2, 2, 3, 12) quad overline(x) = 1/n sum_(i=1)^n x_i $
  #point[La moyenne situe les valeurs ; la médiane résiste davantage à une valeur très grande.]
  $ s_x^2 = 1/(n-1) sum_(i=1)^n (x_i - overline(x))^2 quad s_x = sqrt(s_x^2) $
  #note[La variance est en (µg/m³)² ; l’écart-type est en µg/m³. Il s’agit de la dispersion des observations retenues.]
]
#frame("plots")[
  #point[*Histogramme* : où se concentrent les valeurs ? Chercher asymétrie, creux et queues ; essayer une autre largeur de classe.]
  #point[*Fonction de répartition empirique* : quelle proportion ne dépasse pas un seuil donné ?]
  $ F_n(t) = 1/n sum_(i=1)^n bold(1)_(x_i <= t) quad F_n(3) = 4/5 $
  #text(size: 16pt, fill: muted)[L’indicatrice vaut 1 si la condition est vraie, 0 sinon.]
  #v(8pt)
  #point[*Boîte à moustaches* : situer médiane et quartiles, repérer des observations à examiner.]
  #note[Une observation inhabituelle n’est pas automatiquement une erreur. Les cinq valeurs restent les mêmes quel que soit le graphique.]
]
#frame("joint-question")[
  #point[Le profil de PM2.5 et celui de PM10 décrivent deux distributions séparées.]
  #point[Pour étudier un lien, il faut savoir quelles valeurs ont été observées *ensemble*.]
  #note[Question : une concentration de PM2.5 supérieure à sa moyenne accompagne-t-elle souvent une concentration de PM10 supérieure à la sienne ?]
  #v(15pt)
  #text(size: 19pt)[Dans Beijing, un couple correspond à *la même station et la même heure*. On prédit d’abord la forme du nuage, puis on calcule.]
]
#frame("pairing")[
  #point[Les deux nuages ont exactement les mêmes valeurs dans chaque colonne.]
  #figure("pairing", height: 210pt)
  #note[Les distributions séparées ne déterminent pas l’association. Quel signe prévoyez-vous dans chaque cas ? Les pointillés indiquent les moyennes.]
]
#frame("notation")[
  #tbl((1.1fr, 2.7fr), th[Symbole], th[Signification dans toute la séance],
    [$n$ ; $(x_i, y_i)$], [Nombre de couples complets ; valeurs de l’observation $i$.],
    [$overline(x), overline(y)$], [Moyennes calculées sur *ces mêmes couples*.],
    [$s_x^2, s_y^2$ ; $s_x, s_y$], [Variances d’échantillon ; écarts-types correspondants.],
    [$s_(x y)$ ; $r_(x y)$], [Covariance ; corrélation de Pearson du couple.])
  #v(14pt)
  #note[Convention : diviser par $n-1$ (`ddof=1`) pour les variances et covariances ; retenir au moins deux couples complets.]
]
#frame("products")[
  #set text(size: 19pt)
  #point[Sur les couples A : $overline(x) = overline(y) = 2.5$. Compléter les écarts et leurs produits.]
  #tbl((0.4fr, 0.7fr, 0.8fr, 1fr, 1fr, 1.1fr), th[$i$], th[$x_i$ (h)], th[$y_i$ (pts)], th[$x_i-overline(x)$], th[$y_i-overline(y)$], th[Produit],
    [1], [1], [1], […], […], […], [2], [2], [3], […], […], […],
    [3], [3], [2], […], […], […], [4], [4], [4], […], […], […])
  #v(12pt)
  #note[Mêmes signes des écarts : produit positif. Signes opposés : produit négatif. Le produit indique une contribution au bilan global.]
]
#frame("covariance")[
  #point[Additionner les contributions et les ramener à l’échelle de l’échantillon.]
  $ s_(x y) = 1/(n-1) sum_(i=1)^n (x_i - overline(x))(y_i - overline(y)) $
  #two([
    #text(size: 18pt)[Dans notre exemple :]
    $ (2.25, -0.25, -0.25, 2.25) $
    $ s_(x y) = 4/3 space "h·point" $
  ], [#set text(size: 19pt)
    #point[Le signe résume le bilan des produits centrés.]
    #point[L’unité est le *produit* des unités des deux variables.]
  ])
  #note[Un bilan positif n’impose pas que chaque augmentation de l’une accompagne une augmentation de l’autre.]
]
#frame("tp-a")[
  #point[*1. Préparer* : choisir PM2.5 et PM10, retenir les couples complets, annoncer l’effectif $n$.]
  #point[*2. Observer* : prévoir le signe, tracer le nuage avec unités et effectif.]
  #point[*3. Calculer* : deux moyennes, deux colonnes centrées, les produits, leur somme et la division par $n-1$.]
  #point[*4. Vérifier et interpréter* : comparer avec pandas sur les mêmes lignes ; expliquer une contribution négative.]
  #note[À rendre : un nuage, une covariance avec son unité, l’effectif et deux phrases. La fiche fournit la configuration graphique ; les quantités restent à construire.]
]
#frame("matrix-purpose")[
  #point[Avec $p$ variables, on veut retrouver toutes les variances et covariances sans refaire un raisonnement différent pour chaque couple.]
  $ X in RR^(n times p) quad X_(i j) = "valeur de la variable" space j space "à la ligne" space i $
  #two([
    $ X = mat(1,1; 2,3; 3,2; 4,4) $
    #text(size: 17pt)[Exemple : colonnes $x$ en heures et $y$ en points.]
  ], [#set text(size: 19pt)
    #point[Une ligne : une observation complète.]
    #point[Une colonne : une variable mesurée.]
    #point[Dans cet exemple, $n=4$ et $p=2$.]
  ])
]
#frame("matrix-centre")[
  #point[La moyenne de chaque colonne est calculée sur les quatre mêmes observations.]
  $ (m_1, m_2) = (2.5, 2.5) quad C_(i j) = X_(i j) - m_j $
  #two([
    $ C = mat(-1.5, -1.5; -0.5, 0.5; 0.5, -0.5; 1.5, 1.5) $
  ], [
    #codebox[```python
m = X.mean(axis=0)
C = X - m
```]
    #v(10pt)
    #text(size: 19pt)[La première ligne donne deux écarts négatifs. La deuxième donne des écarts de signes opposés.]
  ])
  #note[Centrer déplace l’origine de chaque variable vers sa moyenne. Cela conserve les couples et les unités des écarts.]
]
#frame("matrix-build")[
  #point[Noter $m_j$ la moyenne de la colonne $j$, puis centrer *chaque colonne*.]
  $ m_j = 1/n sum_(i=1)^n X_(i j) quad C_(i j) = X_(i j) - m_j $
  $ S = (C^T C)/(n-1) in RR^(p times p) quad S_(j k) = 1/(n-1) sum_(i=1)^n C_(i j) C_(i k) $
  #two([#codebox[#raw(matrix.text.split("\n").slice(0, 4).join("\n"), lang: "python")]], [#set text(size: 18pt)
    #point[`axis=0` : une moyenne par colonne.]
    #point[La transposée $C^T$ a $p$ lignes et $n$ colonnes.]
    #point[Le produit donne les mêmes sommes de produits centrés qu’avec un seul couple.]
  ])
]
#frame("matrix-read")[
  #two([
    #block(width: 100%)[
      #show math.equation: set text(size: 32pt)
      $ S = mat(5/3, 4/3; 4/3, 5/3) $
    ]
    #text(size: 18pt)[Ordre des variables : $x$ (heures), puis $y$ (points).]
    #v(12pt)
    #text(size: 18pt)[Unités des cases :]
    $ mat("h"^2, "h·point"; "h·point", "point"^2) $
  ], [#set text(size: 20pt)
    #point[*Diagonale* : variance de chaque variable.]
    #point[*Hors diagonale* : covariance de chaque couple.]
    #point[*Symétrie* : échanger les deux variables ne change pas le produit.]
  ])
  #note[Cette matrice décrit une dispersion conjointe. Les cases n’ont pas toutes la même unité ; leurs valeurs brutes ne classent pas la force des liens.]
]
#frame("tp-a2")[
  #point[*Préparer* PM2.5, PM10 et WSPM ; retenir les lignes où les trois mesures sont présentes.]
  #point[*Construire* $X$, puis le vecteur des moyennes, la matrice centrée $C$ et la matrice $S$.]
  #point[*Contrôler* les dimensions, la symétrie et les variances de la diagonale sur ce même sous-ensemble.]
  #point[*Expliquer* l’unité d’une variance et de deux covariances différentes.]
  #note[Question de contrôle : pourquoi ne peut-on pas comparer la variance WSPM de cette matrice à sa variance calculée sur toutes les lignes disponibles ?]
]
#frame("matrix-limits")[
  #point[*Unités et échelles* : changer une unité peut changer fortement la taille de certaines cases.]
  #point[*Forme du lien* : les produits centrés ne décrivent pas toute la forme du nuage.]
  #point[*Structure* : des groupes, une tendance temporelle ou un point influent peuvent peser sur le bilan.]
  #point[*Population* : la matrice décrit les lignes retenues, pas automatiquement une population plus large.]
  #note[Pour comparer l’alignement linéaire de couples d’unités différentes, il nous manque encore une échelle commune.]
]
#frame("units-plot")[
  #point[Reprendre *les mêmes couples* et convertir seulement les heures en minutes.]
  $ x'_i = 60 x_i quad y'_i = y_i $
  #figure("rescaling", height: 185pt)
  #note[La relation observée a-t-elle changé ? Prédire ce qui arrive à la variance de $x$, à la covariance et à la variance de $y$.]
]
#frame("units-matrix")[
  #two([
    #text(size: 19pt)[Avant : $x$ en heures.]
    #block(width: 100%)[
      #show math.equation: set text(size: 32pt)
      $ S = mat(5/3, 4/3; 4/3, 5/3) $
    ]
  ], [
    #text(size: 19pt)[Après : $x'$ en minutes.]
    #block(width: 100%)[
      #show math.equation: set text(size: 32pt)
      $ S' = mat(6000, 80; 80, 5/3) $
    ]
  ])
  $ s_(x' y) = 60 s_(x y) quad s_(x')^2 = 60^2 s_x^2 quad s_(x') = 60 s_x $
  #point[La covariance passe de $4/3$ h·point à $80$ min·point, sans renforcement de la relation.]
  #note[Le chiffre seul ne permet donc pas de comparer l’intensité de deux associations. Les unités font partie du résultat.]
]
#frame("normalise-purpose")[
  #point[On veut mesurer l’alignement linéaire sans que le choix des unités fasse varier le score.]
  #point[Centrer enlève l’origine des mesures ; diviser par l’écart-type enlève leur échelle.]
  $ (x_i-overline(x)) / s_x quad "est un nombre d’écarts-types, sans unité." $
  #note[Une conversion positive d’unité multiplie à la fois l’écart centré et son écart-type par le même facteur : ils se simplifient.]
]
#frame("standardise")[
  #point[Pour chaque couple retenu, construire les deux valeurs standardisées.]
  $ z_(x i) = (x_i-overline(x))/s_x quad z_(y i) = (y_i-overline(y))/s_y $
  #point[Une valeur $z_(x i)=2$ se situe deux écarts-types au-dessus de la moyenne de $x$.]
  #point[Chaque colonne standardisée a une moyenne nulle et une variance d’échantillon égale à un.]
  #note[Conditions : mêmes lignes pour les calculs ; $n >= 2$ ; $s_x > 0$ et $s_y > 0$. Une variable constante ne peut pas être standardisée ainsi.]
]
#frame("pearson")[
  #point[Calculer la covariance des valeurs standardisées donne la corrélation de Pearson.]
  $ r_(x y) = s_(x y)/(s_x s_y) = 1/(n-1) sum_(i=1)^n z_(x i) z_(y i) $
  #two([#set text(size: 19pt)
    #point[*Sans unité* : les unités du numérateur et du dénominateur s’annulent.]
    #point[*Borné* : $-1 <= r_(x y) <= 1$.]
  ], [#set text(size: 19pt)
    #point[*Signe* : direction du bilan linéaire.]
    #point[*Valeur absolue* : proximité d’un alignement linéaire ; pas un seuil universel de « force ».]
  ])
  #note[Pearson enlève le problème des unités. Il ne répare ni une sélection de lignes inadaptée, ni un lien courbe, ni un mélange de populations.]
]
#frame("pearson-example")[
  #point[Les mêmes quatre couples donnent les variances et la covariance suivantes.]
  $ s_x^2 = s_y^2 = 5/3 quad s_(x y) = 4/3 quad r_(x y) = (4/3)/(sqrt(5/3) sqrt(5/3)) = 4/5 = 0.8 $
  #point[En minutes : la covariance et l’écart-type de $x$ sont tous deux multipliés par $60$.]
  $ r_(x' y) = (60 s_(x y))/((60 s_x) s_y) = r_(x y) $
  #note[À tester dans Plotly : changer positivement l’unité conserve Pearson ; remplacer $y$ par $5-y$ inverse le signe, tout en conservant les valeurs marginales de cet exemple.]
  #text(size: 15pt, fill: green)[#link("../20261020-interactive.html")[Ouvrir l’expérience interactive ↗]]
]
#frame("curvature")[
  #figure("limits", height: 220pt)
  #point[Dans le troisième nuage, $y_i=x_i^2$ : les produits centrés se compensent et Pearson vaut zéro.]
  #note[Zéro corrélation linéaire ne signifie pas absence de relation. Une association observée, même forte, ne suffit pas à conclure à une cause.]
]
#frame("outlier")[
  #figure("influence", height: 205pt)
  #point[Un seul point éloigné des moyennes peut dominer les produits centrés et modifier fortement le coefficient.]
  #note[Ces données sont inventées. En pratique : inspecter l’observation, son contexte et la sensibilité du résultat ; ne pas supprimer un point seulement parce qu’il dérange.]
]
#frame("tp-b")[
  #point[*1. Reprendre* exactement les couples du TP A et leurs deux colonnes centrées.]
  #point[*2. Calculer* les deux écarts-types avec `ddof=1`, puis $r_(x y)$ à partir de votre covariance.]
  #point[*3. Vérifier* avec pandas sur les mêmes lignes ; convertir positivement une unité et vérifier votre prédiction.]
  #point[*4. Interpréter* un autre couple attribué : TEMP/PRES ou PM2.5/WSPM, avec son nuage et son effectif.]
  #note[À rendre : deux lignes de résultats, une explication de l’invariance d’unité et une limite que Pearson ne corrige pas.]
]
#frame("correlation-matrix")[
  #point[Sur les mêmes lignes, noter $s_j=sqrt(S_(j j))$ l’écart-type de la colonne $j$ ; toutes les colonnes doivent être non constantes.]
  $ Z_(i j) = C_(i j)/s_j quad R = (Z^T Z)/(n-1) quad R_(j k) = S_(j k)/(s_j s_k) $
  #two([
    $ R = mat(1, 0.8; 0.8, 1) $
    #text(size: 17pt)[Même matrice de corrélation avant et après conversion des heures en minutes.]
  ], [#set text(size: 19pt)
    #point[Diagonale : un.]
    #point[Toutes les cases : sans unité.]
    #point[Une case hors diagonale : Pearson pour ce couple.]
  ])
]
#frame("heatmap")[
  #point[Préparer la matrice $R$ et les effectifs ; choisir une case, puis revenir au nuage correspondant.]
  #codebox[```python
# R : matrice de corrélation préparée par vous.
fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
im = ax.imshow(R, vmin=-1, vmax=1, cmap="coolwarm")
ax.set(xticks=range(len(columns)), yticks=range(len(columns)),
       xticklabels=columns, yticklabels=columns)
fig.colorbar(im, ax=ax, label="Corrélation de Pearson")
```]
  #set text(size: 18pt)
  #point[Première analyse : un sous-ensemble commun de lignes pour toute la matrice.]
  #note[Avec une suppression des manques paire par paire, les coefficients peuvent porter sur des lignes différentes. Fournir les effectifs par couple ; la représentation comme un unique produit de Gram n’est alors plus garantie.]
]
#frame("prediction")[
  #point[*Décrire* : comment PM2.5 et PM10 varient-ils ensemble dans les observations retenues ?]
  #point[*Prévoir* : à la fin du 10 mars, quelle valeur annoncer pour les heures des 11–12 mars ?]
  #point[Une bonne association contemporaine n’est pas une preuve de qualité prédictive future.]
  #note[Question concrète : le PM10 mesuré demain à midi est-il disponible aujourd’hui au moment de la prévision ?]
]
#frame("split")[
  #tbl((1fr, 2.7fr), th[Mars 2013], th[Rôle dans cet exercice],
    [1–10], [Apprentissage : déterminer la règle de référence.],
    [11–12], [Validation : calculer l’erreur de la règle fixée.],
    [13–14], [Réserve : ne pas l’utiliser ici.])
  #v(18pt)
  #note[Illustration pédagogique : cet extrait a déjà été exploré. Il ne devient pas un test final indépendant après coup. Un vrai test est réservé avant l’exploration et la sélection.]
]
#frame("baseline")[
  #point[Dans ce bloc, $y_i$ désigne PM2.5. Apprendre une constante : la médiane des cibles disponibles en apprentissage.]
  $ b = op("médiane")(y_"apprentissage") quad hat(y)_i = b $
  #point[Sur les $n_"val"$ cibles disponibles de validation, calculer l’erreur absolue moyenne (MAE).]
  $ "MAE"_"validation" = 1/(n_"val") sum_(i=1)^(n_"val") abs(y_i - hat(y)_i) $
  #note[Petit calcul : apprentissage $(1,2,3)$, validation $(4,6)$. Déterminer $b$, puis les deux erreurs. L’erreur conserve l’unité de la cible. L’effectif $n_"val"$ compte les cibles de validation, pas les couples descriptifs.]
]
#frame("tp-c")[
  #point[*Séparer* les périodes indiquées et contrôler leur ordre ; annoncer les effectifs et les cibles manquantes.]
  #point[*Apprendre* la médiane de PM2.5 sur les lignes d’apprentissage uniquement.]
  #point[*Évaluer* cette constante sur les cibles de validation : erreurs absolues, puis moyenne.]
  #point[*Expliquer* pourquoi apprendre la constante sur tout le fichier ferait entrer le futur dans la règle.]
  #note[La fiche donne les masques temporels et un squelette. À rendre : périodes, constante et unité, effectif de validation, erreur et limite de cette illustration.]
]
#frame("return")[
  #two([
    #text(fill: green, weight: "bold")[Résultat descriptif]
    #v(10pt)
    #point[Quelles lignes ? Quelles variables ?]
    #point[Covariance et unité ; Pearson et forme du nuage.]
    #point[Que décrit ce résultat, et jusqu’où ?]
  ], [
    #text(fill: green, weight: "bold")[Résultat de validation]
    #v(10pt)
    #point[Quelles périodes et quelle règle ?]
    #point[Effectif évalué, erreur et unité.]
    #point[Quelle information était disponible pour apprendre ?]
  ])
  #note[Une corrélation et une erreur de prévision répondent à des questions différentes. Leurs valeurs numériques ne se comparent pas.]
]
#frame("exit")[
  #point[Si l’on exprime une variable en minutes plutôt qu’en heures, que deviennent sa variance, ses covariances et ses corrélations ?]
  #point[Que lit-on sur et hors de la diagonale de $S$ ? Pourquoi préciser les lignes retenues ?]
  #point[Pourquoi $r_(x y)=0$ ne suffit-il pas à conclure qu’il n’y a aucune relation ?]
  #point[Quelles lignes déterminent la règle constante ? Quelles lignes servent à calculer son erreur ?]
  #note[Répondre sans code, puis comparer les explications. Signaler un point encore incertain : ce bilan sert à préparer la suite.]
]
#frame("gram")[
  #point[Sur un même ensemble de lignes, $C$ est la matrice centrée et $S=(C^T C)/(n-1)$.]
  #point[Chaque case est un produit scalaire de deux colonnes centrées, divisé par $n-1$.]
  $ a^T S a = norm(C a)^2/(n-1) >= 0 quad "pour tout" space a in RR^p $
  #note[La matrice est symétrique et semi-définie positive. Cette géométrie dépend des unités ; le choix des échelles devra être justifié pour l’ACP. Avec des lignes différentes selon les couples, cette justification ne s’applique plus à la matrice assemblée.]
]
#frame("cosine")[
  #point[Définir les deux vecteurs centrés, sur les mêmes $n$ couples.]
  $ bold(c)_x = (x_i-overline(x))_(i=1)^n quad bold(c)_y = (y_i-overline(y))_(i=1)^n $
  $ r_(x y) = (bold(c)_x^T bold(c)_y)/(norm(bold(c)_x) norm(bold(c)_y)) = cos(theta) $
  #point[La borne $abs(r_(x y)) <= 1$ vient de Cauchy–Schwarz.]
  #note[Cette formule suppose deux vecteurs non nuls. L’alignement est une propriété des colonnes centrées, pas une preuve de causalité.]
]
#context [#metadata(counter(page).get().first()) <slide-page-count>]
