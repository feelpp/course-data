#import "theme.typ": *
#let session = json("lesson.json").sessions.at(0)

// These named Python blocks are executed by build.py before Typst compilation.
#let clouds = ```python
fig, axes = plt.subplots(1, 2, figsize=(10, 3.2), constrained_layout=True)
for ax, names in zip(axes, [('TEMP','DEWP'), ('TEMP','PRES')], strict=True):
    pair = air[list(names)].dropna()
    ax.scatter(pair.iloc[:,0], pair.iloc[:,1], s=9, alpha=.25, edgecolors='none')
    ax.set(xlabel=f'{names[0]} (°C)', ylabel=f'{names[1]} ({"°C" if names[1] == "DEWP" else "hPa"})',
           title=f'1–14 mars 2013 · n={len(pair)}')
save(fig)
```
#let pairing = ```python
x, y = np.array([1.,2.,3.,4.]), np.array([1.,3.,2.,4.])
fig, axes = plt.subplots(1, 2, figsize=(10,3.1), constrained_layout=True)
for ax, yy, title in zip(axes, [y,5-y], ['Couples A', 'Couples B'], strict=True):
    ax.scatter(x, yy, s=90)
    ax.axvline(2.5, color='grey', ls='--'); ax.axhline(2.5, color='grey', ls='--')
    ax.set(xlabel='x (heures)', ylabel='y (points)', title=title,
           xticks=[1,2,3,4], yticks=[1,2,3,4])
save(fig)
```
#let bias = ```python
rng = np.random.default_rng(20261020)
draws = rng.multivariate_normal([0.,0.], [[1.,.7],[.7,1.]], size=(20000,5))
c = draws-draws.mean(axis=1, keepdims=True)
q_values = (c[:,:,0]*c[:,:,1]).sum(axis=1)
fig, ax = plt.subplots(figsize=(8.5,3.1), constrained_layout=True)
ax.hist(q_values/5, bins=60, density=True, histtype='step', ls='--', label='Diviseur n : moyenne attendue 0,560')
ax.hist(q_values/4, bins=60, density=True, histtype='step', label='Diviseur n−1 : moyenne attendue 0,7')
ax.axvline(.7, color='black', label='Covariance de population')
ax.set(xlabel='Covariance estimée', ylabel='Densité', title='20 000 échantillons i.i.d., n = 5')
ax.legend(fontsize=10)
save(fig)
```
#let projection = ```python
u, v = np.array([3.,0.]), np.array([2.,2.])
fig, ax = plt.subplots(figsize=(7,3.3), constrained_layout=True)
for end, label in [(u,'U'), (v,'V'), (np.array([2.,0.]),'a* U')]:
    ax.annotate('', xy=end, xytext=(0,0), arrowprops=dict(arrowstyle='->', lw=2))
    ax.text(end[0]+.07,end[1]+.07,label,fontsize=14)
ax.plot([2,2],[0,2], '--', color='#bc6734', label='Résidu orthogonal')
ax.plot([1.85,1.85,2],[0,.15,.15],color='grey')
ax.set(xlim=(-.4,3.6),ylim=(-.5,2.7),aspect='equal',title='Schéma dans le plan engendré par U et V')
ax.axis('off'); ax.legend(loc='lower left')
save(fig)
```
#let curve = ```python
u = np.linspace(-1,1,401)
fig, ax = plt.subplots(figsize=(7.5,3.1), constrained_layout=True)
ax.plot(u,u*u)
ax.set(xlabel='x',ylabel='y = x²', title='Relation déterministe, Pearson nul par symétrie')
save(fig)
```
#let influence = ```python
u, v = np.arange(6.), np.array([1.,3.,0.,4.,2.,1.])
fig, axes = plt.subplots(1,2,figsize=(10,3.1),constrained_layout=True)
for ax, extra in zip(axes,[False,True],strict=True):
    xx, yy = (np.r_[u,30],np.r_[v,30]) if extra else (u,v)
    ax.scatter(u,v,label='Couples initiaux')
    if extra: ax.scatter([30],[30],marker='x',s=90,label='Point ajouté')
    ax.set(xlim=(-2,33),ylim=(-2,33),xlabel='x',ylabel='y',title=f'n={len(xx)}, r={np.corrcoef(xx,yy)[0,1]:.2f}')
    ax.legend(fontsize=10)
save(fig)
```

#let matrix = ```python
features = ['PM2.5','PM10','TEMP','PRES','DEWP','WSPM']
complete = air.dropna(subset=features)
A = complete[features].to_numpy()
Ac = A-A.mean(axis=0)
n,p = A.shape
S = Ac.T@Ac/(n-1)
sd = np.sqrt(np.diag(S))
Az = Ac/sd
R = Az.T@Az/(n-1)
assert np.allclose(R, complete[features].corr())
fig, ax = plt.subplots(figsize=(7,4),constrained_layout=True)
im=ax.imshow(R,vmin=-1,vmax=1,cmap='RdBu_r')
ax.set(xticks=range(p),yticks=range(p),xticklabels=features,yticklabels=features,
       title=f'Mêmes lignes complètes · n={n}')
for j in range(p):
    for k in range(p):
        ax.text(k,j,f'{R[j,k]:.2f}',ha='center',va='center',color='white' if abs(R[j,k])>.6 else 'black')
fig.colorbar(im,ax=ax,label='Pearson (sans unité)')
save(fig)
```

#setup(session)[
#frame[20 octobre : covariance et matrice de Pearson][
  #text(size: 29pt)[Comment deux variables varient-elles ensemble ?]
  #v(18pt)
  #point[Partir du nuage, construire une mesure, comprendre sa géométrie.]
  #point[Distinguer description, estimation et approximation linéaire.]
  #point[Calculer puis défendre une interprétation sur les données de Beijing.]
  #note[Bilan de la séance de 4 heures : jusqu’à la matrice de Pearson. TP du 5 octobre à finaliser.]
  #notebook("joint-variation", "parcours et objectifs")
]
#frame[Variables aléatoires et valeurs observées][
  #text(size: 18pt)[Le modèle est défini sur $(Omega,cal(F),bb(P))$ : issues possibles, événements et probabilités. E désigne l’espérance dans ce modèle ; aucune théorie de la mesure supplémentaire n’est nécessaire ici.]
  #point[$(X,Y)$ est un couple aléatoire générique, de loi jointe $P_(X Y)$.]
  #point[Pour n ≥ 2 fixé, $(X_i,Y_i)$ désigne le i-ème couple aléatoire, i = 1,…,n. Les hypothèses sur ces couples seront précisées avant la preuve.]
  #text(size: 18pt)[Une réalisation $omega_0$ de l’expérience fournit les nombres observés :]
  $ x_i=X_i thin lr((omega_0)), quad y_i=Y_i thin lr((omega_0)) $
  #note[Le fichier contient les valeurs minuscules. Répéter l’expérience pourrait produire d’autres valeurs ; les variables aléatoires décrivent cette variabilité.]
]
#frame[La covariance de population : le paramètre visé][
  #text(size: 18pt)[On suppose $E[X^2]<infinity$ et $E[Y^2]<infinity$. Les moyennes $mu_X,mu_Y$ et la covariance $sigma_(X Y)$ sont des paramètres déterministes, généralement inconnus.]
  $ mu_X=E[X], quad mu_Y=E[Y] $
  $ op("Var")(X)=E[(X-mu_X)^2] $
  $ sigma_(X Y)=op("Cov")(X,Y)=E[(X-mu_X)(Y-mu_Y)] $
  #point[Les écarts de même signe donnent un produit positif ; les signes opposés, un produit négatif. Pour Y = X, on retrouve la variance.]
  #ask[La moyenne de population $mu_X$ varie-t-elle quand on tire un autre échantillon ?]
]
#frame[Rappels : les règles utilisées dans la preuve][
  #text(size: 18pt)[U,V,W sont ici des variables aléatoires de moments d’ordre deux finis ; a,b sont des constantes.]
  #point[*Linéarité de l’espérance* :]
  $ E[a U+b V]=a E[U]+b E[V] $
  #point[*Bilinéarité de la covariance* (aussi dans le second argument) :]
  $ op("Cov")(a U+b V,W)=a op("Cov")(U,W)+b op("Cov")(V,W) $
  #point[*Indépendance* de U,V : $E[U V]=E[U]E[V]$, donc covariance nulle.]
  #note[La réciproque est fausse. Pour les moyennes d’échantillon, nous appliquerons les deux premières règles aux sommes des $X_i$ et des $Y_j$.]
]
#frame[Indépendance : factoriser l’espérance du produit][
  #show math.equation: set text(size: 22pt)
  #text(size: 18pt)[Cas fini : U et V sont indépendantes ; u et v désignent leurs valeurs possibles.]
  #v(5pt)
  #text(size: 18pt)[*1. Factoriser les probabilités.* L’indépendance signifie :]
  $ bb(P)(U=u,V=v)=bb(P)(U=u) bb(P)(V=v) $
  #text(size: 18pt)[*2. Calculer l’espérance du produit et séparer les sommes.*]
  $ E[U V] &= sum_u sum_v u v bb(P)(U=u,V=v) \
           &= sum_u sum_v u bb(P)(U=u) thin v bb(P)(V=v) \
           &= lr((sum_u u bb(P)(U=u))) lr((sum_v v bb(P)(V=v))) \
           &= E[U] E[V] $
  #note[Chaque facteur ne dépend que d’un indice de somme. Cette factorisation vaut aussi pour des variables indépendantes de moments d’ordre deux finis.]
]
#frame[Indépendance : annuler la covariance][
  #text(size: 18pt)[*3. Développer les produits centrés.* Posons $mu_U=E[U]$ et $mu_V=E[V]$ : ce sont des constantes.]
  $ op("Cov")(U,V) &= E[(U-mu_U)(V-mu_V)] \
                   &= E lr([U V-mu_V U-mu_U V+mu_U mu_V]) \
                   &= E[U V]-mu_V E[U]-mu_U E[V]+mu_U mu_V \
                   &= E[U V]-mu_U mu_V $
  #text(size: 18pt)[Sous indépendance, l’étape 2 donne $E[U V]=mu_U mu_V$, donc :]
  $ op("Cov")(U,V)=mu_U mu_V-mu_U mu_V=0 $
  #note[Les produits centrés peuvent être positifs ou négatifs ; leur espérance s’annule. L’identité $op("Cov")(U,V)=E[U V]-E[U]E[V]$ reste vraie sans indépendance. La covariance nulle, à elle seule, ne prouve pas l’indépendance.]
]
#frame[I.i.d. : indépendance des couples, pas dans le couple][
  #text(size: 18pt)[Les n couples sont indépendants et de même loi jointe $P_(X Y)$, avec moments d’ordre deux finis. À indice égal : $op("Cov")(X_i,Y_i)=sigma_(X Y)$.]
  #two([
    #text(size: 18pt)[Si i ≠ j, l’indépendance des couples donne :]
    $ E[X_i Y_j]=E[X_i]E[Y_j] $
    $ op("Cov")(X_i,Y_j)=0 $
    #text(size: 18pt)[Cette hypothèse n’impose pas l’indépendance de $X_i$ et $Y_i$.]
  ], [
    #text(size: 17pt)[$C_n$ regroupe les covariances entre indices i,j :]
    $ C_n=mat(sigma_(X Y),0,dots,0;0,sigma_(X Y),dots,0;⋮,⋮,⋱,⋮;0,0,dots,sigma_(X Y)) $
    #text(size: 17pt)[n termes diagonaux ; les autres sont nuls. Ici les axes indexent les observations.]
  ])
  #ask[Température et point de rosée mesurés ensemble doivent-ils être indépendants ?]
]
#frame[Du dernier TP à une nouvelle question][
  #text(size: 17pt)[Une station-heure = une station observée à une heure ; n = nombre de paires complètes. TEMP : température ; DEWP : température du point de rosée (condensation), en °C ; PRES : pression, en hPa.]
  #fig("clouds", height: 210pt)
  #ask[Que voit-on que deux histogrammes ne montrent pas ?]
  #text(size: 17pt)[Même station-heure pour les deux coordonnées ; valeurs manquantes retirées par paire.]
]
#frame[Mêmes distributions, associations opposées][
  #fig("pairing")
  #ask[Chaque distribution décrit les valeurs d’une variable seule. Ici, leurs valeurs restent les mêmes, mais leur appariement change : les grandes valeurs vont-elles ensemble ?]
]
#frame[Définir la somme centrée avant de la calculer][
  #text(size: 18pt)[Les moyennes d’échantillon sont aléatoires ; leurs réalisations sont les moyennes numériques :]
  $ overline(X)=(sum_(i=1)^n X_i)/n, quad overline(Y)=(sum_(i=1)^n Y_i)/n $
  $ overline(x)=overline(X) thin lr((omega_0)), quad overline(y)=overline(Y) thin lr((omega_0)) $
  #text(size: 18pt)[Nous appelons $Q_(X Y)$ la somme aléatoire des produits centrés, et $q_(x y)$ sa valeur observée :]
  $ Q_(X Y)=sum_(i=1)^n (X_i-overline(X))(Y_i-overline(Y)) $
  $ q_(x y)=Q_(X Y) thin lr((omega_0))=sum_(i=1)^n (x_i-overline(x))(y_i-overline(y)) $
  #note[$overline(X)$ est une statistique ; $mu_X$ est un paramètre. Même si $E[overline(X)]=mu_X$ sous le modèle de même loi, ces objets ne sont pas identiques.]
]
#frame[Quatre couples : une réalisation numérique][
  #text(size: 18pt)[n = 4 ; $x_i$ en heures, $y_i$ en points. Les vecteurs x,y contiennent les observations ; $bold(1)$ contient n uns ; $x_c,y_c$ désignent les vecteurs centrés.]
  $ x=(1,2,3,4), quad y=(1,3,2,4), quad overline(x)=overline(y)=2.5 $
  $ x_c=x-overline(x)bold(1)=(-1.5,-0.5,0.5,1.5) $
  $ y_c=y-overline(y)bold(1)=(-1.5,0.5,-0.5,1.5) $
  $ q_(x y)=2.25-0.25-0.25+2.25=4 $
  #text(size: 18pt)[Deux valeurs à distinguer : $c_n=q_(x y)/n=1$ et $s_(x y)=q_(x y)/(n-1)=4/3$. Nous allons expliquer les deux diviseurs.]
  #notebook("joint-variation", "§ 2 · calculer avant de vérifier")
]
#frame[Paramètre, covariance empirique, estimateur][
  #point[*Population* : $sigma_(X Y)$ est la covariance de la loi $P_(X Y)$.]
  #point[*Loi empirique* : chaque couple observé reçoit le poids 1/n. Sa covariance exacte est $c_n=q_(x y)/n$.]
  #text(size: 18pt)[Un *estimateur* est une règle appliquée à l’échantillon aléatoire. Une *estimation* est sa valeur après observation :]
  $ S_(X Y)=Q_(X Y)/(n-1), quad s_(x y)=S_(X Y) thin lr((omega_0))=q_(x y)/(n-1) $
  #note[« Sans biais » signifiera $E[S_(X Y)]=sigma_(X Y)$ sous des hypothèses précises. Cela n’affirme jamais $s_(x y)=sigma_(X Y)$ pour le fichier observé.]
]
#frame[Pourquoi n−1 ? Une identité algébrique][
  #text(size: 18pt)[On manipule les variables aléatoires. Le centrage par une moyenne d’échantillon s’écrit :]
  $ X_i-overline(X)=(X_i-mu_X)-(overline(X)-mu_X) $
  $ sum_(i=1)^n (X_i-mu_X)=n(overline(X)-mu_X) $
  #text(size: 18pt)[Même égalité pour Y. Dans le produit développé, chacun des deux termes croisés retire $n(overline(X)-mu_X)(overline(Y)-mu_Y)$ ; le terme constant en remet une copie. D’où :]
  $ Q_(X Y)=sum_(i=1)^n (X_i-mu_X)(Y_i-mu_Y)-n(overline(X)-mu_X)(overline(Y)-mu_Y) $
  #note[Cette identité ne requiert aucune indépendance. Le notebook développe explicitement les quatre termes.]
]
#frame[Les n termes diagonaux donnent la correction][
  #text(size: 18pt)[Par bilinéarité, la covariance des moyennes est la somme des covariances croisées, divisée par n² :]
  $ op("Cov")(overline(X),overline(Y))=1/n^2 sum_(i=1)^n sum_(j=1)^n op("Cov")(X_i,Y_j)=(n sigma_(X Y))/n^2=sigma_(X Y)/n $
  #text(size: 18pt)[On prend ensuite l’espérance de l’identité précédente :]
  $ E[Q_(X Y)]=n sigma_(X Y)-n sigma_(X Y)/n=(n-1)sigma_(X Y) $
  $ E[S_(X Y)]=sigma_(X Y), quad E[Q_(X Y)/n]=(n-1)/n sigma_(X Y) $
  #note[Pour Y = X : $S_(X X)=sum_i (X_i-overline(X))^2/(n-1)$ et $E[S_(X X)]=op("Var")(X)$. C’est la variance corrigée, avec la même preuve.]
]
#frame[Sans biais ne veut pas dire exact][
  #fig("bias")
  #text(size: 18pt)[Chaque tirage donne une estimation différente. La moyenne simulée approche une espérance ; elle ne constitue pas une preuve. Le notebook compare n = 5, 20, 100 pour covariance et variance.]
  #note[Le diviseur n contracte l’espérance vers zéro : pour une covariance négative, le biais est positif.]
  #notebook("joint-variation", "§ 3 · simulation reproductible et dépendance des heures de Beijing")
]
#frame[Les unités empêchent une comparaison directe][
  #text(size: 18pt)[Transformation affine : multiplier par une constante puis ajouter un décalage. a,c : facteurs d’échelle ; b,d : décalages. Exemple : °F = 1,8 × °C + 32.]
  $ op("Cov")(a X+b,c Y+d)=a c op("Cov")(X,Y) $
  $ op("Cov")(60X,Y)=60 op("Cov")(X,Y) $
  #point[Le nuage décrit le même phénomène après conversion des unités.]
  #point[La covariance numérique change pourtant d’un facteur 60.]
  #ask[Par quelle quantité de même unité peut-on diviser ?]
]
#frame[Centrer et réduire : fixer une moyenne et une variance][
  #text(size: 18pt)[L’écart-type d’échantillon $s_x$ (et de même $s_y$) est la racine de la variance corrigée :]
  $ s_x=sqrt((sum_(i=1)^n (x_i-overline(x))^2)/(n-1)) $
  #point[Centrer : $x_c=x-overline(x) bold(1)$ ; la moyenne devient zéro.]
  #point[Réduire : $x_c/s_x$ ; la variance corrigée devient un, si $s_x>0$.]
  #note[Pour les quatre couples : $s_x=s_y=sqrt(5/3)$. Diviser par une échelle n’efface pas une relation courbe.]
]
#frame[Longueur, produit scalaire et autres normalisations][
  #text(size: 18pt)[L’espace $RR^n$ contient les vecteurs de n nombres. Pour x,y dans cet espace, T désigne la transposition.]
  $ x^T y=sum_(i=1)^n x_i y_i, quad norm(x)=sqrt(x^T x) $
  #point[Produit scalaire nul : vecteurs orthogonaux, donc à angle droit.]
  #point[Normalisation euclidienne : $x/norm(x)$ a longueur un si $x != 0$.]
  #point[Min-max : $(x-min(x))/(max(x)-min(x))$ place les valeurs entre 0 et 1, si l’étendue est positive.]
  #note[Centrage-réduction, longueur unitaire et min-max répondent à des objectifs différents.]
]
#frame[Pearson : retirer les unités de la covariance][
  #text(size: 18pt)[Nous notons $rho_(X Y)$ la corrélation de population. $sigma_X=sqrt(op("Var")(X))>0$ et $sigma_Y=sqrt(op("Var")(Y))>0$ : écarts-types de population.]
  $ rho_(X Y)=(op("Cov")(X,Y))/(sigma_X sigma_Y) $
  #text(size: 18pt)[Les variables centrées-réduites, notées $Z_X,Z_Y$, sont :]
  $ Z_X=(X-mu_X)/sigma_X, quad Z_Y=(Y-mu_Y)/sigma_Y $
  $ op("Cov")(Z_X,Z_Y)=rho_(X Y) $
  #point[Population : $rho$. Échantillon : $r_(x y)=s_(x y)/(s_x s_y)$.]
  #note[Écarts-types strictement positifs et même diviseur. Le résultat sans biais démontré pour la covariance ne se transmet pas automatiquement au coefficient de Pearson.]
]
#frame[Dans l’échantillon, Pearson est un cosinus][
  #text(size: 18pt)[$theta$ est l’angle entre les deux vecteurs centrés non nuls.]
  $ x_c=x-overline(x) bold(1), quad y_c=y-overline(y) bold(1) $
  $ r_(x y) = ((x_c^T y_c)/(n-1)) / (sqrt((x_c^T x_c)/(n-1)) sqrt((y_c^T y_c)/(n-1))) $
  $ r_(x y) = (x_c^T y_c)/(norm(x_c) norm(y_c)) = cos(theta) $
  #point[Angle entre deux colonnes centrées de $RR^n$, pas entre deux points du nuage.]
  #ask[Pourquoi faut-il centrer avant de normaliser la longueur ?]
]
#frame[Le centrage enlève une dimension][
  #text(size: 18pt)[Pour les vecteurs observés x,y, $I_n$ est l’identité et $bold(1)$ le vecteur de n uns. H retire la moyenne de chaque colonne :]
  $ H=I_n-1/n bold(1)bold(1)^T, quad x_c=H x, quad y_c=H y $
  $ H^T=H, quad H^2=H, quad H bold(1)=0 $
  #text(size: 18pt)[$bold(1)^perp$ est l’espace des vecteurs de somme nulle. Il a dimension n−1 : la dernière coordonnée est imposée par les précédentes. H est sa projection orthogonale.]
  $ op("rang")(H)=op("tr")(H)=n-1 $
  #note[La trace tr est la somme des coefficients diagonaux. Cette géométrie explique la contrainte ; l’égalité d’espérances exige encore les hypothèses sur les couples. Preuve détaillée en lecture complémentaire.]
]
#frame[Bornes et cas d’égalité : Cauchy–Schwarz][
  $ abs(x_c^T y_c) <= norm(x_c) norm(y_c) arrow.r -1 <= r_(x y) <= 1 $
  #point[Égalité si et seulement si les deux vecteurs non nuls sont proportionnels.]
  $ y_c=a x_c quad arrow.r quad y_i=a x_i+b $
  #point[Orthogonalité : $r_(x y)=0$. Alignement : $r_(x y)=1$ ou $r_(x y)=-1$.]
  #note[Échelle positive : même corrélation. Une seule échelle négative : signe inversé.]
]
#frame[Pourquoi la covariance parle-t-elle de linéarité ?][
  #text(size: 17pt)[$U,V$ désignent les variables aléatoires centrées ci-dessous. $L^2$ est l’espace des variables W telles que $E[W^2]<infinity$ ; ici, la longueur vient de l’espérance du carré.]
  $ op("Cov")(X,a X+b)=a op("Var")(X) $
  $ U=X-E[X], quad V=Y-E[Y] $
  $ lr(⟨U,V⟩) = E[U V], quad norm(U)^2=op("Var")(X) $
  #text(size: 18pt)[$lr(⟨U,V⟩)$ est leur produit scalaire. On identifie les variables égales presque sûrement, c’est-à-dire avec probabilité un : une longueur nulle signifie alors le même élément.]
]
#frame[La meilleure approximation par une droite][
  #text(size: 17pt)[a : pente candidate ; J(a) : erreur quadratique moyenne ; $a^star$ : pente qui minimise J. Le résidu est l’écart $V-a^star U$.]
  $ J(a)=E[(V-a U)^2]=E[V^2]-2a E[U V]+a^2 E[U^2] $
  $ J'(a)=0 quad arrow.r quad a^star=(op("Cov")(X,Y))/(op("Var")(X)) $
  $ E[U(V-a^star U)] = 0 $
  #point[Variance de X positive : minimum unique ; résidu orthogonal à U.]
  #note[Prédicteur affine : $mu_Y+a^star(X-mu_X)$. La meilleure droite ne suit pas nécessairement la moyenne de Y à chaque valeur de X, si celle-ci est courbe.]
]
#frame[La projection explique la formule][
  #fig("projection")
  #point[Covariance nulle : aucune composante de V dans la direction U.]
  #ask[Peut-il rester une dépendance dans une direction non linéaire ?]
]
#frame[Une dépendance parfaite avec Pearson nul][
  #text(size: 17pt)[$cal(U)(-1,1)$ désigne la loi uniforme : dans cet intervalle, deux sous-intervalles de même longueur ont la même probabilité.]
  #two([
    $ X tilde.op cal(U)(-1,1), quad Y=X^2 $
    $ E[X]=E[X^3]=0 $
    $ op("Cov")(X,Y)=0 $
    #text(size: 18pt)[Variances : 1/3 et 4/45. Les événements $abs(X)<=1/2$ et $Y<=1/4$ coïncident. Leur probabilité et celle de leur intersection valent 1/2 ; l’indépendance donnerait 1/4.]
  ], [#fig("curve", height: 240pt)])
]
#frame[Un point peut dominer le coefficient][
  #fig("influence")
  #point[Vérifier l’origine du point et comparer le coefficient avec et sans lui avant de justifier une exclusion.]
  #note[Corrélation : association linéaire descriptive ; aucune preuve de causalité.]
]
#frame[Du produit d’écarts à la projection][
  #text(size: 25pt)[Centrage → produit scalaire → covariance → angle de Pearson → projection linéaire]
  #v(20pt)
  #point[Une preuve : pourquoi $E[S_(X Y)]=sigma_(X Y)$ sous les hypothèses i.i.d. ?]
  #point[Une limite : pourquoi une courbe peut-elle avoir Pearson nul ?]
  #point[Une trace écrite : paire, station, période, n, unités, nuage, conclusion bornée.]
  #note[Ces outils permettent maintenant de terminer la covariance et Pearson dans votre TP du 5 octobre. Garder une paire, son effectif et ses unités dans votre conclusion.]
]
#frame[Une table, deux espaces géométriques][
  #text(size: 18pt)[n observations, p variables numériques ; $A_(i j)$ est la valeur observée de la variable j à la ligne i. A est une matrice de nombres fixés : sa majuscule désigne ici une matrice, pas une variable aléatoire.]
  $ A in RR^(n times p), quad A=mat(1,2;3,4;5,6), quad n=3, quad p=2 $
  #two([
    #point[Chaque ligne est un point de $RR^p$ : ici (1,2), (3,4), (5,6).]
  ], [
    #point[Chaque colonne est un vecteur de $RR^n$ : ici (1,3,5) et (2,4,6).]
  ])
  #note[Chaque ligne complète contient toutes les variables choisies. Comme en séance 1, on retire les lignes incomplètes sans remplacer leurs valeurs manquantes.]
]
#frame[Centrer est une projection orthogonale][
  #text(size: 17pt)[$I_n$ : identité ; $bold(1)$ : n uns ; T : transposition ; $overline(a)$ : vecteur des p moyennes. P garde la partie constante ; H la retire.]
  $ P=(bold(1)bold(1)^T)/n, quad H=I_n-P, quad A_c=H A=A-bold(1)overline(a)^T $
  $ P^T=P, quad P^2=P quad arrow.r quad H^T=H, quad H^2=H $
  #text(size: 18pt)[Dans notre table : $overline(a)=(3,4)^T$ ; lignes centrées (−2,−2), (0,0), (2,2).]
  #note[Projection orthogonale : on retire une partie perpendiculaire au résultat. Ici, chaque colonne centrée a une somme nulle ; elle est orthogonale au vecteur constant. En code : `Ac = A - A.mean(axis=0)`.]
]
#frame[La covariance : un produit entre colonnes][
  #text(size: 18pt)[j et k indexent les variables (1,…,p) ; i les lignes (1,…,n), avec n > 1. $S_(j k)$ est leur covariance ; $s_j$ est l’écart-type corrigé de la colonne j.]
  $ S=1/(n-1) A_c^T A_c=1/(n-1) A^T H A in RR^(p times p) $
  $ S_(j k)=1/(n-1) sum_(i=1)^n (A_(i j)-overline(a)_j)(A_(i k)-overline(a)_k) $
  #point[Diagonale : variances $S_(j j)=s_j^2$. Hors diagonale : covariances.]
  #note[Dans notre exemple, $S=mat(4,4;4,4)$. Les deux colonnes centrées sont identiques.]
]
#frame[La matrice observée et le paramètre de population][
  #text(size: 18pt)[$bold(W)=(W_1,…,W_p)^T$ est un vecteur aléatoire générique ; $bold(W)_i$ est le i-ème vecteur d’un échantillon i.i.d. Sa réalisation fournit la ligne i de A. $mu=E[bold(W)]$ est le vecteur des moyennes de population.]
  #text(size: 18pt)[La matrice de population $Gamma$ contient $Gamma_(j k)=op("Cov")(W_j,W_k)$. La moyenne aléatoire et l’estimateur matriciel sont :]
  $ overline(bold(W))=(sum_(i=1)^n bold(W)_i)/n $
  $ hat(Gamma)_n=1/(n-1)sum_(i=1)^n (bold(W)_i-overline(bold(W)))(bold(W)_i-overline(bold(W)))^T $
  $ S=hat(Gamma)_n thin lr((omega_0)), quad E[hat(Gamma)_n]=Gamma $
  #note[La dernière égalité utilise l’hypothèse i.i.d. et les moments d’ordre deux. Les identités de centrage, de Gram et d’ACP sur A restent des identités sur la table observée, sans cette hypothèse.]
]
#frame[Gram, rang et noyau : trois rappels utiles][
  #point[*Gram* : matrice des produits scalaires entre des vecteurs ; ici les colonnes centrées de A, divisées par n−1.]
  #point[*Rang* : nombre de colonnes linéairement indépendantes. Notre exemple a deux colonnes identiques après centrage, donc un rang égal à 1.]
  #point[*Noyau* : ensemble des vecteurs envoyés sur zéro ; noté $ker$. Ici $A_c vec(1,-1)=0$.]
  #note[Une matrice carrée de rang incomplet est dite singulière : elle n’est pas inversible. Des colonnes colinéaires (proportionnelles) peuvent produire cette situation.]
]
#frame[Pourquoi symétrique et semi-définie positive ?][
  #text(size: 18pt)[Pour tout vecteur v de p coefficients, $norm(A_c v)^2$ est la somme des carrés de ses n coordonnées. « Semi-définie positive » signifie $v^T S v>=0$ pour tout v.]
  $ S^T=S, quad v^T S v=norm(A_c v)^2/(n-1)>=0 $
  $ ker(S)=ker(A_c), quad op("rang")(S)=op("rang")(A_c)<=min(p,n-1) $
  #point[La norme nulle équivaut à $A_c v=0$ : mêmes noyaux, donc mêmes rangs. Le centrage impose une contrainte de somme nulle.]
  #note[Retirer des lignes différentes pour chaque paire peut détruire la structure de Gram : cette preuve exige une seule table complète.]
]
#frame[La corrélation choisit l’échelle de chaque axe][
  #text(size: 17pt)[$op("diag")$ construit une matrice diagonale. D contient les variances ; $D^(-1/2)$ a pour diagonale $1/s_1,…,1/s_p$. On suppose chaque $s_j>0$.]
  $ D=op("diag")(s_1^2,dots,s_p^2), quad A_z=A_c D^(-1/2) $
  $ R=D^(-1/2) S D^(-1/2)=1/(n-1) A_z^T A_z $
  #point[R est la matrice de Pearson : chaque colonne de $A_z$ a variance un.]
  #point[Sur S : unités originales. Sur R : distances entre observations mesurées en écarts-types. C’est un changement de métrique, c’est-à-dire de règle de mesure des distances.]
  #ask[Une mesure peu fiable doit-elle recevoir le même poids après réduction ?]
]
#frame[Beijing : lire la matrice avec ses nuages][
  #text(size: 17pt)[Une carte de couleurs (heatmap) associe une couleur à chaque coefficient. PM2.5 et PM10 : particules (µg/m³) ; TEMP et DEWP : température et point de rosée (°C) ; PRES : pression (hPa) ; WSPM : vent (m/s).]
  #fig("matrix", height: 245pt)
  #text(size: 16pt)[1–14 mars 2013 ; 1 002 station-heures complètes. Lire une case avec son nuage : la couleur ne montre ni courbure ni causalité.]
]
#frame[Travail à finaliser : le TP du 5 octobre][
  #text(size: 21pt)[Reprendre votre notebook Statistical Exploration déjà commencé. Garder vos calculs, votre audit et vos graphiques.]
  #v(12pt)
  #point[*Parties 5–7.* Nuages appariés, covariance explicite et Pearson sur les mêmes paires ; vérifier avec pandas.]
  #point[*Matrice et effectifs.* Terminer la carte des coefficients et le tableau des effectifs. Comparer suppression par paire et mêmes lignes complètes.]
  #point[*Interpréter.* Donner unités, signe, n et une limite ; vérifier l’effet d’un changement d’unité positif.]
  #note[Compléter la sélection de la partie 9 et le Results existant. Ce travail était à finaliser ; la séance ne garantit pas que chaque étudiant l’ait terminé.]
  #text(size: 17pt, fill: green)[#link("https://feelpp.github.io/course-data/course-data/foundations/statistical-exploration.html#exploration-paired-work")[Reprendre le TP du 5 octobre ↗]]
]
#frame[Prochaine étape : le 2 novembre][
  #point[*Acquis introduits.* Les matrices S et R décrivent les relations entre toutes les variables sur une table commune.]
  #point[*Nouvelle question.* Peut-on résumer ces variables par quelques nouvelles coordonnées qui conservent beaucoup de variance ?]
  #point[*ACP et SVD.* L’analyse en composantes principales choisit les directions ; la décomposition en valeurs singulières les calcule.]
  #point[*Le 9 novembre : régression.* Désigner une réponse à estimer ; distinguer cet objectif de la reconstruction des entrées.]
  #note[Le 2 novembre : théorie et TP ACP, puis la question d’une réponse à estimer. La régression et les premiers pas en apprentissage supervisé sont prévus le 9 novembre.]
]

]
