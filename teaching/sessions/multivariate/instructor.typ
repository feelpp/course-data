#let lesson = json("lesson.json")
#let computed = json("generated/values.json")
#let green=rgb("155f46")
#set document(title: "20 octobre et 2 novembre : guide enseignant", author: "M1 CSMI · Traitement de données")
#set page(paper: "a4", margin: 17mm, footer: context [#text(size: 9pt, fill: green)[M1 CSMI · Guide enseignant] #h(1fr) #counter(page).display()])
#set text(font: "Arial", size: 10.5pt, lang: "fr", fill: rgb("142a24"))
#set par(leading: .5em, spacing: .6em)
#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 21pt, fill: green)
#show heading.where(level: 2): set text(size: 13pt, fill: green)
#show math.equation: set text(font: "New Computer Modern Math", size: 12.5pt)
#show raw: set text(font: "DejaVu Sans Mono", size: 8.5pt)
#let timing(session) = {
  let elapsed=0
  table(columns: (auto, 1fr), inset: 5pt, stroke: .4pt+rgb("bfcfc2"),
    [*Minutes*], [*Activité*],
    ..session.schedule.enumerate().map(((index, item)) => {
      let start=session.schedule.slice(0,index).map(it => it.at(0)).sum(default: 0)
      let end=start+item.at(0)
      ([#start–#end], [#item.at(1)])
    }).flatten())
}
= 20 octobre : bilan et travail à finaliser
*Public :* M1 CSMI. Pandas, audit et description univariée introduits. *Bilan signalé par l’enseignant :* la séance de quatre heures est allée jusqu’à la matrice de Pearson. L’ACP, la SVD et la régression n’y ont pas été terminées. Ce bilan ne reconstitue pas un minutage qui n’a pas été relevé.

== Le contenu regroupé sous cette date
- Variables aléatoires, observations et paramètres ; covariance, centrage et correction n−1 sous ses hypothèses.
- Pearson : retrait des unités, angle entre colonnes centrées, interprétation et limites.
- Passage à une table commune : covariance matricielle, Gram, centrage, puis matrice de Pearson.

*Notations.* $Q_(X Y)$ et $S_(X Y)$ sont aléatoires ; $q_(x y)$ et $s_(x y)$ sont calculés sur les données. A, S et R majuscules relèvent de la convention matricielle pour la table observée. Cette distinction reste à faire expliciter par les étudiants.

== Le TP du 5 octobre reste le même travail
Les étudiants devaient finaliser leur notebook Statistical Exploration : nuages, covariance et Pearson sur les mêmes paires ; carte des coefficients avec effectifs ; changement d’unité et conclusion limitée. La matrice commune du cours et la matrice calculée par paires dans le TP peuvent utiliser des lignes différentes : faire verbaliser ce choix.

Conserver la partie 9 pour sélectionner les éléments de preuve, puis compléter le Results déjà commencé. Ne pas créer un second rapport. L’attribution de ce travail ne signifie pas que tous les étudiants l’ont terminé. Les comparaisons saisonnières et variantes Monte Carlo restent facultatives.

== La transition à annoncer
S et R rassemblent les relations par paires entre mesures originales. La nouvelle question n’est plus une case de la matrice : peut-on choisir quelques combinaisons de variables qui représentent bien le nuage ? L’ACP conserve de la variance ; elle ne désigne aucune réponse à prédire. Une composante n’est pas nécessairement une mesure physique directe.

Le support du 20 octobre inclut maintenant les matrices qui étaient au début de l’ancienne séance 2. Les adresses web sont conservées, mais les titres, dates et limites de contenu sont explicites. La suite est datée du 2 novembre ; elle ne fait pas partie du bilan des acquis du 20 octobre.

#pagebreak()
= 2 novembre : théorie et TP ACP en deux heures
*Objectif.* Partir des matrices S et R connues ; calculer des directions de variance maximale ; interpréter leurs poids et scores et reconstruire les mesures. L’enseignant confirme que les étudiants savent centrer et effectuer un produit matriciel, mais ont besoin de temps. La régression attend le 9 novembre.

#timing(lesson.sessions.at(1))

*Au tableau.* Projeter sur v donne n scores. Leur variance est $v^T S v$ sur les données centrées, ou $v^T R v$ après centrage-réduction. La contrainte $v^T v=1$ interdit d’augmenter artificiellement la variance en allongeant v. Lagrange donne les directions propres ; choisir la plus grande valeur propre maximise la variance. La SVD calcule ces directions sur la table sans former son Gram.

*Sens des axes.* Dans l’exemple à deux variables standardisées de corrélation 0,8, la somme et le contraste normalisés ont variances 1,8 et 0,2. Un axe combine les mesures ; il peut être interprétable sans être un nouveau capteur. Distinguer ses p coefficients des n scores. Le signe est arbitraire ; l’interprétation reste descriptive.

*TP principal, 45 minutes.* Ouvrir le TP guidé « Build and interpret principal components ». Les étudiants calculent centrage/réduction, directions et scores. Trois contrôles : table centrée-réduite ; dimensions et variances des scores ; reconstruction et erreur relative. Lire les poids d’un axe avec une station-heure extrême. Comparer deux puis trois composantes sur la même table ; unités et retrait de variable sont des prolongements. Préserver cinq minutes pour la conclusion, même si la comparaison doit être terminée après le cours.

*Ouverture, cinq minutes.* Demander ce qui change si PM2.5 devient une réponse à estimer. Aucun ajustement de droite aujourd’hui. La SVD sert au calcul de l’ACP ; le conditionnement détaillé et les comparaisons de solveurs restent en référence.

*Suite.* Régression, apprentissage et validation, comparaison à une référence simple, premiers pas en apprentissage supervisé. Les créneaux datés réutilisent les thèmes du contrat de 28 heures ; le TP est inclus dans les deux heures du 2 novembre.
#pagebreak()
= Modèle, échantillon et observations
*Cadre.* $(Omega,cal(F),bb(P))$ désigne les issues possibles, événements et probabilités. $(X,Y)$ est un couple aléatoire générique de loi jointe $P_(X Y)$. Les paramètres $mu_X=E[X]$, $mu_Y=E[Y]$ et $sigma_(X Y)=op("Cov")(X,Y)$ sont des nombres déterministes, généralement inconnus. On suppose les moments d’ordre deux finis.

*Avant et après réalisation.* Pour n ≥ 2 fixé, $(X_i,Y_i)$ est le i-ème couple aléatoire. Une issue $omega_0$ de l’expérience complète fournit $x_i=X_i thin lr((omega_0))$, $y_i=Y_i thin lr((omega_0))$. Les moyennes $overline(X),overline(Y)$ sont des variables aléatoires ; $overline(x),overline(y)$ leurs réalisations. $E[overline(X)]=mu_X$ n’en fait pas le même objet que $mu_X$.

== Définir Q avant de l’utiliser
$ Q_(X Y)=sum_(i=1)^n (X_i-overline(X))(Y_i-overline(Y)) $
$ q_(x y)=Q_(X Y) thin lr((omega_0))=sum_(i=1)^n (x_i-overline(x))(y_i-overline(y)) $
$ S_(X Y)=Q_(X Y)/(n-1), quad s_(x y)=q_(x y)/(n-1), quad c_n=q_(x y)/n $
Q et S majuscules sont des statistiques aléatoires ; q, s et c minuscules sont des valeurs calculées sur les données. « Sans biais » qualifie la règle S dans un modèle d’échantillonnage, pas l’exactitude d’un nombre s. Le diviseur n décrit exactement la loi empirique qui donne poids 1/n à chaque couple observé.

== Rappel i.i.d. avant la preuve
Les couples sont indépendants *entre indices* et de même loi jointe. Les deux composantes d’un même couple peuvent dépendre. À indice égal, la covariance vaut $sigma_(X Y)$ par identité des lois. Pour i ≠ j, indépendance des couples ⇒ indépendance de $X_i,Y_j$ ⇒ $E[X_i Y_j]=E[X_i]E[Y_j]$, donc covariance nulle. La matrice des covariances entre indices possède exactement n termes diagonaux non nuls possibles.

*Questions à poser.* $overline(X)$ est-elle un nombre déjà calculé ? $mu_X$ change-t-elle avec l’échantillon ? « Couples indépendants » impose-t-il l’indépendance température / point de rosée à la même heure ? Quelle hypothèse annule les covariances entre indices différents ?

#pagebreak()
= Covariance : la preuve sans raccourci
*1. Algèbre, sans indépendance.* Développer les deux différences :
$ X_i-overline(X)=(X_i-mu_X)-(overline(X)-mu_X) $
Dans la somme des produits apparaissent quatre termes :
$ Q_(X Y)=sum_i (X_i-mu_X)(Y_i-mu_Y) $
$ quad -(overline(Y)-mu_Y)sum_i (X_i-mu_X)-(overline(X)-mu_X)sum_i (Y_i-mu_Y) $
$ quad +n(overline(X)-mu_X)(overline(Y)-mu_Y) $
Les sommes valent $n(overline(X)-mu_X)$ et $n(overline(Y)-mu_Y)$. Les deux termes croisés retirent deux copies du produit des écarts des moyennes ; le dernier en remet une :
$ Q_(X Y)=sum_i (X_i-mu_X)(Y_i-mu_Y)-n(overline(X)-mu_X)(overline(Y)-mu_Y) $

*2. Espérance et hypothèses.* Même loi ⇒ moyennes de population communes et espérances des moyennes d’échantillon correctes. Donc :
$ E[Q_(X Y)]=n sigma_(X Y)-n op("Cov")(overline(X),overline(Y)) $
Par bilinéarité de la covariance :
$ op("Cov")(overline(X),overline(Y))=1/n^2 sum_(i=1)^n sum_(j=1)^n op("Cov")(X_i,Y_j) $
Il reste n fois $sigma_(X Y)$ sur la diagonale ; les autres termes sont nuls par indépendance entre couples, et non par simple centrage. Ainsi :
$ op("Cov")(overline(X),overline(Y))=sigma_(X Y)/n $
$ E[Q_(X Y)]=(n-1)sigma_(X Y), quad E[S_(X Y)]=sigma_(X Y) $

*3. Ce que cela signifie.* La moyenne sur des répétitions indépendantes de l’expérience approche le paramètre. Une estimation particulière ne lui est pas nécessairement égale. Avec diviseur n, l’espérance vaut $(n-1)/n sigma_(X Y)$ ; le biais vaut $-sigma_(X Y)/n$, donc son signe dépend de celui de la covariance.

*4. Variance.* Poser Y = X donne $Q_(X X)=sum_i (X_i-overline(X))^2$ et $E[Q_(X X)]=(n-1)sigma_X^2$. Ainsi $S_(X X)=Q_(X X)/(n-1)$ est sans biais pour la variance. La correction ne démontre pas le caractère sans biais de Pearson, qui est un rapport non linéaire.

#pagebreak()
= Géométrie et statut des calculs
== Centrage : une contrainte, un rang et une trace
$I_n$ est l’identité ; $bold(1)$ contient n uns. Définir :
$ P=(bold(1)bold(1)^T)/n, quad H=I_n-P $
$ P^2=P, quad P^T=P quad arrow.r quad H^T=H, quad H^2=H $
H annule $bold(1)$ et conserve les vecteurs dont la somme des coordonnées est nulle : c’est le projecteur orthogonal sur $bold(1)^perp$. Une coordonnée centrée est imposée par les n−1 autres. La trace est la somme des coefficients diagonaux :
$ op("rang")(H)=n-1, quad op("tr")(H)=n(1-1/n)=n-1 $
Cette géométrie complète la preuve probabiliste ; elle n’annule pas, à elle seule, les covariances temporelles. La preuve optionnelle du notebook relie l’espérance de Q à la trace en utilisant les hypothèses i.i.d.

== Matrices du 20 octobre ; directions et scores du 2 novembre
A, $A_c$, S et R désignent des matrices de nombres observés. Leurs majuscules relèvent de la convention matricielle. Le vecteur aléatoire $bold(W)$ représente p variables ; ses copies $bold(W)_i$ représentent les observations avant réalisation. $Gamma$ est la covariance de population ; $hat(Gamma)_n$ son estimateur aléatoire et $S=hat(Gamma)_n thin lr((omega_0))$ sa réalisation.
$ A_c=H A, quad S=(A_c^T A_c)/(n-1)=(A^T H A)/(n-1) $
Cette identité est algébrique, alors que $E[hat(Gamma)_n]=Gamma$ demande des hypothèses de moments et d’échantillonnage. $D$ contient les variances observées ; $A_z=A_c D^(-1/2)$ et R est sa covariance. $v_j$ est une direction, $z_j=A_c v_j$ ses scores observés, $lambda_j$ leur variance observée. $sigma_j$ est une valeur singulière de la table, distincte d’un écart-type scalaire. $q=min(n,p)$ est la taille de la SVD économique.

== Projection et moindres carrés : deux objectifs
Pour les variables aléatoires centrées U,V, le minimum de $E[(V-a U)^2]$ donne la meilleure approximation affine *de population*. Les moindres carrés prévus le 9 novembre minimisent au contraire une somme sur un design et une réponse *observés*. Leur résidu est orthogonal aux colonnes du design. Cela ne prouve ni absence de biais des coefficients, ni validité causale, ni précision future. L’ACP reconstruit les entrées ; la régression désigne une réponse.

*Présentation.* Rappels en ouverture ; preuve centrale au tableau ; détails algébriques, trace et variations de simulation dans le notebook. Les résultats restent visibles sur Antora et les preuves sont repliables. Le TP du 5 octobre était à finaliser après le 20 octobre ; le TP ACP occupe 45 minutes le 2 novembre.

#pagebreak()
= Repères de vérification et précautions
== Calcul exact des quatre couples
$x=(1,2,3,4)$, $y=(1,3,2,4)$ : moyennes 2,5 ; produits centrés 2,25 ; −0,25 ; −0,25 ; 2,25. Donc $q_(x y)=4$, $c_n=1$, $s_(x y)=4/3$, $s_x^2=s_y^2=5/3$, $r=0.8$. Régression : pente 0,8 point/heure et intercept 0,5 point. Passer en minutes multiplie la covariance par 60 et divise la pente par 60 ; Pearson reste égal à 0,8.

== Contre-exemple sans raccourci
La loi $cal(U)(-1,1)$ est uniforme : deux intervalles de même longueur y ont la même probabilité. Pour $X tilde.op cal(U)(-1,1)$ et $Y=X^2$, intégrer les fonctions impaires : $E[X]=E[X^3]=0$. Les deux variances sont strictement positives ($1/3$ et $4/45$). La covariance est nulle. Les événements $abs(X)<=1/2$ et $Y<=1/4$ sont identiques, de probabilité 1/2 ; leur intersection a probabilité 1/2 et non 1/4. La non-indépendance est ainsi démontrée, pas simplement affirmée.

== Repères calculés : ACP le 2 novembre ; régression en préparation
ACP centrée-réduite : six variables sur 1 002 mêmes station-heures ; part cumulée des deux premières composantes : #calc.round(100 * (computed.pca_ratios.at(0)+computed.pca_ratios.at(1)), digits: 1) %. Le signe des axes peut être inversé ; comparer projecteurs/reconstructions, et considérer un sous-espace si des valeurs propres sont répétées.

Régression fixée : PM2.5 estimé avec PM10, TEMP, PRES, DEWP, WSPM, tous mesurés à la même heure. #computed.regression_n.at(0) lignes complètes d’apprentissage (1–10 mars) ; #computed.regression_n.at(1) de validation (11–14 mars). RMSE OLS : #calc.round(computed.rmse,digits: 2) µg/m³ ; constante égale à la moyenne d’apprentissage : #calc.round(computed.baseline_rmse,digits: 2) µg/m³. Faire lire ces résultats et les résidus ; ne pas promettre une performance sur d’autres dates.

== Erreurs fréquentes
- Covariance nulle ⇒ indépendance : faux. Pearson décrit une composante linéaire.
- n−1 ⇒ observation indépendante : faux. C’est une correction sous hypothèses.
- Réduire ⇒ gaussien : faux. Cela fixe une échelle, pas une loi.
- Semi-définie positive ⇒ inversible : faux. Vérifier rang et valeurs singulières.
- Deux composantes expliquent beaucoup ⇒ bon prédicteur : faux. La cible n’entre pas dans l’objectif ACP.
- Résidus orthogonaux ⇒ modèle causal ou correct : faux. C’est une propriété du minimum sur l’apprentissage.

== Simulation et portée des résultats
La simulation est déterministe (graine fixée), avec covariance vraie 0,7 et variance vraie 1. Pour n = 5, 20, 100, les espérances avec diviseur n valent respectivement 0,56 ; 0,665 ; 0,693 pour la covariance, et 0,8 ; 0,95 ; 0,99 pour la variance. Avec n−1 : 0,7 et 1. Les moyennes Monte Carlo doivent s’en approcher ; elles ne sont pas la preuve. Les heures de Beijing peuvent conserver des covariances entre indices différents : le calcul descriptif reste valide, la conclusion i.i.d. demande justification.

== Données et reproduction
L’extrait canonique reste inchangé : Aotizhongxin, Changping, Dingling, 1–14 mars 2013. Le complément sous licence CC BY 4.0 contient les périodes du 1er au 14 mars, juin, septembre et décembre 2013. Pas d’imputation, c’est-à-dire de remplacement des valeurs manquantes par des estimations. Ces dates ne décrivent pas des saisons entières. Les heures et les stations sont dépendantes. Les données de mars ont déjà été explorées : la séparation temporelle est pédagogique, pas un test final indépendant. Tout prétraitement prédictif s’apprend sur le passé ; l’ACP descriptive préalable n’est pas utilisée dans la régression.
Reproduction : voir le README du support ; trois noyaux neufs, assertions numériques, compilation Typst, contrôle visuel de chaque page. Aucun réseau nécessaire avec environnement et données préparés.
