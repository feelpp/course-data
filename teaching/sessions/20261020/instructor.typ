#import "paper.typ": *
#let lesson = json("lesson.json")
#let refs = json("teacher.json")
#show: doc => paper("Conducteur enseignant · Covariance, Pearson et validation", doc)
= Conduire les quatre heures
*20 octobre 2026 · M1 CSMI · support de classe en français*

Point de départ confirmé : pandas, audit et description univariée ont été abordés. L’analyse conjointe et les matrices restent nouvelles. La présence d’une notion dans le site ne prouve pas qu’elle a déjà été comprise.

#table(columns: (0.8fr, 3.5fr, 0.6fr), inset: 6pt, stroke: 0.4pt + green,
 th[Minutes], th[Contenu], th[Durée],
 ..lesson.schedule.map(row => (row.at(0), row.at(1), str(row.at(2)) + " min")).flatten())

== Une question, un calcul, une interprétation
Faire prévoir un résultat avant d’afficher le calcul ou le graphique. Sur les quatre couples inventés, demander successivement : quels écarts ? quels signes ? quel bilan ? quelle unité ? La formule vient après ces contributions.

La reprise reste limitée à 25 min. Le nouveau créneau Pearson dure 65 min, avec 20 min de TP. Le dernier bloc ouvre la validation à l’aide d’une constante ; il ne lance pas tout le chapitre de modélisation.

== Décisions si le temps manque
Préserver les couples complets, la lecture de la matrice et l’effet des unités. Réduire la mise en forme de la carte de couleurs et le nombre de couples secondaires. Les deux dernières diapositives, sur Gram et le cosinus, sont facultatives et hors des 220 minutes d’activité. Les pauses comptent 20 minutes.

#callout[Les diapositives et les fiches de cette séance sont en français à la demande de l’enseignant. Les références du site restent en anglais. La fiche étudiant ne contient aucun résultat Beijing calculé ; ce conducteur n’est pas publié avec elle.]

#pagebreak()
= Du rappel à la covariance
== Diagnostic et rappel
Une ligne Beijing représente une station à une heure donnée. Zéro est une mesure, pas une absence de mesure. Une moyenne ne décrit ni une asymétrie, ni tous les extrêmes, ni les groupes. Changer les classes ne change pas une proportion calculée sur les mêmes observations et au même seuil.

Sur $(1,2,2,3,12)$ µg/m³ : moyenne $4$, médiane $2$, variance d’échantillon $20.5$ (µg/m³)² et écart-type $sqrt(20.5) approx 4.53$ µg/m³. Avec interpolation linéaire : $Q_1=2$, $Q_3=3$, écart interquartile $1$. La proportion ne dépassant pas $3$ vaut $4/5$.

== Construire le bilan avec les quatre couples
Dessiner le nuage A et ses deux droites moyennes : $overline(x)=overline(y)=2.5$. Les lignes ne sont jamais triées séparément.

#tab((0.4fr,0.7fr,0.7fr,1fr,1fr,1fr), th[$i$],th[$x_i$ (h)],th[$y_i$ (pts)],th[$x_i-overline(x)$],th[$y_i-overline(y)$],th[Produit],
[1],[1],[1],[$-1.5$],[$-1.5$],[$2.25$],
[2],[2],[3],[$-0.5$],[$0.5$],[$-0.25$],
[3],[3],[2],[$0.5$],[$-0.5$],[$-0.25$],
[4],[4],[4],[$1.5$],[$1.5$],[$2.25$])

$ s_(x y) = 1/(n-1) sum_(i=1)^n (x_i-overline(x))(y_i-overline(y)) = 4/3 space "h·point" $

Les contributions de signes opposés diminuent la somme. Une covariance positive ne signifie pas que chaque augmentation de $x$ provoque ou accompagne une augmentation de $y$. Dans le nuage B, remplacer $y$ par $5-y$ conserve ses valeurs marginales et donne $s_(x y)=-4/3$ h·point.

== Relier le code au calcul
```python
paired = air[["PM2.5", "PM10"]].dropna()
x = paired["PM2.5"].to_numpy(dtype=float)
y = paired["PM10"].to_numpy(dtype=float)
n = len(paired)
dx, dy = x - x.mean(), y - y.mean()
s_xy = (dx * dy).sum() / (n - 1)
```
Le dénominateur $n-1$ est notre convention `ddof=1`. Les lectures horaires sont dépendantes : ce choix ne suffit pas à justifier automatiquement une estimation sans biais pour une population.

#pagebreak()
= Matrices, unités et standardisation
== Distinguer les objets sans changer de convention
$X$ contient les observations, à $n$ lignes et $p$ colonnes. La moyenne de la colonne $j$ est $m_j$. La matrice $C$ contient les écarts centrés ; $S$ contient les covariances.

$ m_j=1/n sum_(i=1)^n X_(i j) quad C_(i j)=X_(i j)-m_j quad S=(C^T C)/(n-1) $

Dans le tableau à deux colonnes, $m_1=overline(x)$ et $m_2=overline(y)$. La diagonale de $S$ contient $s_x^2$ et $s_y^2$ ; les cases croisées contiennent $s_(x y)$.

#tab((1fr,1fr,1fr),th[Unité de $x$],th[Matrice de covariance],th[Pearson],
[Heures],[$S=mat(5/3,4/3;4/3,5/3)$],[$r_(x y)=0.8$],
[Minutes],[$S'=mat(6000,80;80,5/3)$],[$r_(x' y)=0.8$])

Les unités des cases sont respectivement h², h·point et point² avant conversion. La conversion multiplie la variance de $x$ par $60^2$, sa covariance avec $y$ par $60$ et son écart-type par $60$. Elle ne renforce pas la relation.

== Expliquer la solution au problème d’échelle
$ z_(x i)=(x_i-overline(x))/s_x quad z_(y i)=(y_i-overline(y))/s_y $
$ r_(x y)=s_(x y)/(s_x s_y)=1/(n-1) sum_(i=1)^n z_(x i) z_(y i) $

Chaque valeur standardisée est sans unité. Moyenne nulle, variance d’échantillon un ; une variable constante rend cette division impossible. Pour les quatre couples : $s_x^2=s_y^2=5/3$ et $r_(x y)=(4/3)/(5/3)=0.8$.

Pour plusieurs colonnes, définir $s_j=sqrt(S_(j j))$, puis $Z_(i j)=C_(i j)/s_j$ et $R=(Z^T Z)/(n-1)$. La diagonale de $R$ vaut un pour les colonnes non constantes.

== Limites à faire formuler
Pearson retire les unités, pas les points influents, les mélanges de groupes, les tendances ou les biais de sélection. Sur $x=(-2,-1,0,1,2)$ et $y_i=x_i^2$, la corrélation est nulle malgré une relation déterministe. Une association ne prouve pas une cause. Les effectifs par paire ne prouvent pas que les mêmes lignes sont utilisées.

#pagebreak()
= Corrigés des TP A, A2 et B
Les repères sont calculés sur l’extrait canonique `datasets/teaching/air-quality/observations.csv`. Les valeurs non arrondies sont vérifiées indépendamment avec NumPy et `statistics` lors de la compilation.

#table(columns: (1.5fr,0.5fr,1fr,0.8fr), inset: 7pt, stroke: 0.4pt + green,
 th[Couple],th[$n$],th[$s_(x y)$],th[$r_(x y)$],
 ..refs.pairs.map(row => (row.pair, str(row.n), str(calc.round(row.covariance,digits:3)), str(calc.round(row.r,digits:4)))).flatten())

Unités des covariances : (µg/m³)² pour PM2.5/PM10 ; °C² pour TEMP/DEWP ; °C·hPa pour TEMP/PRES ; (µg/m³)·(m/s) pour PM2.5/WSPM. Tous les coefficients de Pearson sont sans unité.

== A2 : les mêmes lignes dans chaque produit
```python
columns = ["PM2.5", "PM10", "WSPM"]
common = air[columns].dropna()
X = common.to_numpy(dtype=float)
m = X.mean(axis=0)
C = X - m
S = C.T @ C / (len(X) - 1)
assert np.allclose(S, common.cov().to_numpy())
assert np.allclose(np.diag(S), common.var(ddof=1))
assert np.allclose(S, S.T)
s = np.sqrt(np.diag(S))
Z = C / s
R = Z.T @ Z / (len(X) - 1)
assert np.allclose(R, common.corr().to_numpy())
```
Effectif commun : #refs.common_n. WSPM est complet, mais sa variance dans cette matrice doit utiliser ces lignes communes, pas ses 1008 valeurs disponibles. Mathématiquement, $S_(1 3)$ correspond à #box[`S[0, 2]`] dans NumPy.

== B : deux implémentations sur les mêmes couples
```python
s_x, s_y = x.std(ddof=1), y.std(ddof=1)
r_xy = s_xy / (s_x * s_y)
assert np.isclose(r_xy, paired.corr().iloc[0, 1])
```
Faire reprendre les deux colonnes du TP A pour conserver l’appariement. La suppression de toutes les lignes manquantes du fichier ne serait pas justifiée pour chaque couple.

#callout[Pendant la circulation : demander le sens d’une ligne, les dimensions du tableau, une unité de case et une contribution négative. Une cellule exécutée sans erreur ne suffit pas à prouver la compréhension.]

#pagebreak()
= Premier résultat de validation et bilan
== TP C : apprendre une constante sur le passé
```python
t = pd.to_datetime(air[["year", "month", "day", "hour"]])
train = air.loc[t < "2013-03-11"]
validation = air.loc[(t >= "2013-03-11") & (t < "2013-03-13")]
b = train["PM2.5"].dropna().median()
actual = validation["PM2.5"].dropna()
predictions = pd.Series(b, index=actual.index)
mae = (actual - predictions).abs().mean()
assert t.loc[train.index].max() < t.loc[validation.index].min()
assert set(train.index).isdisjoint(validation.index)
```
$ "MAE"_"validation"=1/(n_"val") sum_(i=1)^(n_"val") abs(y_i-hat(y)_i) quad hat(y)_i=b $

#tab((1.2fr,1fr),th[Repère],th[Valeur canonique],
[Apprentissage / validation / réserve],[#refs.train_rows / #refs.validation_rows / #refs.reserved_rows lignes],
[Médiane apprise],[#refs.baseline µg/m³],
[Erreur absolue moyenne],[#calc.round(refs.validation_mae,digits:6) µg/m³])

PM2.5 est complet dans ces partitions, donc $n_"val"=144$. Dans le petit exemple au tableau, la médiane de $(1,2,3)$ vaut $2$ ; les erreurs sur $(4,6)$ valent $2$ et $4$, soit une moyenne $3$.

== Limites de cette illustration
Le jeu entier a déjà servi à l’exploration. On illustre les rôles temporels ; on ne dispose pas d’un test final indépendant. Les 13–14 mars restent inutilisés ici. Une dépendance horaire empêche aussi d’interpréter 144 lignes comme 144 informations indépendantes.

Le PM10 mesuré au même futur instant que la cible n’est pas connu au moment de décision annoncé. Une corrélation élevée ne répare pas cette frontière. Apprendre une médiane sur tout le fichier ferait entrer le futur dans la règle, même si le score obtenu semblait meilleur.

== Bilan individuel : ce que l’on doit entendre
- Un changement positif d’unité modifie variances et covariances, mais laisse Pearson inchangé.
- La matrice $S$ réunit les variances et covariances sur les lignes déclarées ; chaque case a sa propre unité.
- Pearson peut manquer une relation courbe ; il ne prouve pas une causalité.
- L’apprentissage détermine la constante ; la validation calcule son erreur, dans l’unité de la cible.

Suite du cours : prétraitements ajustés sur apprentissage, pipelines et modèles simples. Conserver les difficultés repérées pour une reprise ciblée.

#context [#metadata(counter(page).get().first()) <handout-page-count>]
