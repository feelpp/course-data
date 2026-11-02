#import "theme.typ": *
#let session = json("lesson.json").sessions.at(1)

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
#let direction = ```python
t = np.linspace(-2,2,19)
toy = np.column_stack([t, .7*t+.2*np.sin(5*t)])
_,ss,vv = np.linalg.svd(toy-toy.mean(0),full_matrices=False)
v1=vv[0]; projected=(toy@v1)[:,None]*v1
fig,ax=plt.subplots(figsize=(7.5,3.4),constrained_layout=True)
ax.scatter(*toy.T,label='Observations centrées')
ax.plot([-3*v1[0],3*v1[0]],[-3*v1[1],3*v1[1]],'k--',label='Direction principale')
for a,b in zip(toy,projected,strict=True): ax.plot([a[0],b[0]],[a[1],b[1]],color='grey',alpha=.5)
ax.scatter(*projected.T,marker='x',label='Projections')
ax.set(xlabel='Variable 1 centrée',ylabel='Variable 2 centrée',aspect='equal')
ax.legend(fontsize=10)
save(fig)
```
#let pca = ```python
U,s,Vt = np.linalg.svd(Az,full_matrices=False)
ratio=s*s/np.sum(s*s)
scores=Az@Vt.T
raw=np.linalg.svd(Ac,compute_uv=False)**2
fig,axes=plt.subplots(1,2,figsize=(10,3.4),constrained_layout=True)
axes[0].plot(range(1,p+1),np.cumsum(raw/raw.sum()),'o--',label='Échelles originales')
axes[0].plot(range(1,p+1),np.cumsum(ratio),'s-',label='Centrage-réduction')
axes[0].set(xlabel='Composantes retenues',ylabel='Part cumulée de variance',ylim=(0,1.05))
axes[0].legend(fontsize=10)
for station,marker in zip(sorted(complete.station.unique()),['o','s','^'],strict=True):
    mask=complete.station.to_numpy()==station
    axes[1].scatter(scores[mask,0],scores[mask,1],marker=marker,s=9,alpha=.3,label=station)
axes[1].set(xlabel='Score CP1',ylabel='Score CP2',title='ACP sur variables centrées-réduites')
axes[1].legend(fontsize=8)
save(fig)
```
#let validation = ```python
predictors=['PM10','TEMP','PRES','DEWP','WSPM']
needed=predictors+['PM2.5']
train=air.loc[air.day<=10].dropna(subset=needed)
valid=air.loc[air.day>10].dropna(subset=needed)
mu=train[predictors].mean(); scale=train[predictors].std(ddof=1)
Atr=((train[predictors]-mu)/scale).to_numpy()
Ava=((valid[predictors]-mu)/scale).to_numpy()
Xtr=np.column_stack([np.ones(len(train)),Atr])
Xva=np.column_stack([np.ones(len(valid)),Ava])
ytr=train['PM2.5'].to_numpy(); yva=valid['PM2.5'].to_numpy()
beta=np.linalg.lstsq(Xtr,ytr,rcond=None)[0]
pred=Xva@beta
rmse=np.sqrt(np.mean((yva-pred)**2)); baseline=np.sqrt(np.mean((yva-ytr.mean())**2))
record(regression_n=[len(train),len(valid)],rmse=float(rmse),baseline_rmse=float(baseline),
       pca_ratios=ratio.tolist())
fig,ax=plt.subplots(figsize=(7.5,3.2),constrained_layout=True)
ax.scatter(yva,pred,s=12,alpha=.3)
lim=[min(yva.min(),pred.min()),max(yva.max(),pred.max())]
ax.plot(lim,lim,'k--')
ax.set(xlabel='PM2.5 observé (µg/m³)',ylabel='PM2.5 estimé (µg/m³)',
       title=f'Validation ultérieure · n={len(valid)} · RMSE={rmse:.1f} µg/m³')
save(fig)
```

#setup(session)[
#frame[2 novembre : ACP, directions et reconstruction][
  #text(size: 23pt)[Le 20 octobre, nous sommes arrivés à la matrice de Pearson. Aujourd’hui : que faire de cette information ?]
  #v(12pt)
  #point[*Question.* Résumer plusieurs mesures par quelques nouvelles directions de grande variance.]
  #point[*Théorie.* Projection, contrainte de longueur, valeurs propres, scores et SVD.]
  #point[*TP.* Calculer et interpréter des composantes sur les observations de Beijing.]
  #note[2 heures, dont 45 minutes de TP. La régression sera étudiée le 9 novembre ; aujourd’hui, nous en poserons la question.]
  #notebook("matrix-geometry", "séance du 2 novembre")
]
#frame[Rappel du 20 octobre : partir de S ou de R][
  #text(size: 18pt)[A : table observée ; $A_c$ : colonnes centrées ; S : covariance. $s_j$ : écart-type de la colonne j ; D : diagonale des variances ; $A_z$ : table centrée-réduite.]
  $ S=(A_c^T A_c)/(n-1), quad D=op("diag")(s_1^2,dots,s_p^2) $
  $ A_z=A_c D^(-1/2), quad R=(A_z^T A_z)/(n-1) $
  #point[Les mêmes lignes complètes sont utilisées pour toutes les variables. R est la matrice de Pearson, déjà introduite le 20 octobre.]
  #point[Sur S, les échelles originales comptent. Sur R, chaque variable a variance un. Le choix définit ce qu’on veut préserver.]
  #note[A et ses matrices sont des nombres observés. Les preuves et l’exemple de matrice sont dans le support du 20 octobre.]
]
#frame[La nouvelle question : combiner les variables][
  #point[*La matrice décrit des paires.* Une case de R résume une relation linéaire entre deux mesures.]
  #point[*L’ACP cherche des axes.* Peut-on représenter chaque station-heure par deux ou trois coordonnées, plutôt que six ?]
  #point[*Critère.* Conserver le plus possible de dispersion du nuage, mesurée par la variance des coordonnées projetées.]
  #point[*Choix.* Covariance : préserver les échelles choisies. Corrélation : comparer des variations mesurées en écarts-types.]
  #note[L’ACP est descriptive : aucune variable à prédire n’est désignée. Un axe de grande variance n’est pas automatiquement utile pour une future réponse.]
]
#frame[Des axes qui combinent les mesures physiques][
  #text(size: 18pt)[La direction $v=(w_1,…,w_p)^T$ possède un coefficient $w_j$ par variable. Sur la table centrée-réduite, le score $z_i$ de la ligne i est :]
  $ z_i=sum_(j=1)^p (A_z)_(i j) w_j $
  #point[Chaque coefficient indique comment sa variable entre dans cette nouvelle coordonnée. Un score appartient à une observation ; la direction contient p coefficients.]
  #point[La composante ne correspond pas nécessairement à un capteur physique. Elle peut résumer un motif commun ou un contraste entre plusieurs mesures.]
  #point[Après centrage-réduction, les scores sont sans unité physique ; leur interprétation demande de lire les coefficients avec les variables originales.]
  #note[Nommer prudemment un axe après inspection. Son signe peut être inversé sans changer le sous-espace ni la reconstruction ; ce n’est pas une preuve de causalité.]
]
#frame[Deux variables : une somme et un contraste][
  #text(size: 18pt)[Reprenons les quatre couples déjà calculés : leurs variables centrées-réduites ont une corrélation de 0,8. Leur matrice est :]
  $ R=mat(1,0.8;0.8,1), quad v_1=1/sqrt(2) vec(1,1), quad v_2=1/sqrt(2) vec(1,-1) $
  #text(size: 18pt)[Si $x_(z,i),y_(z,i)$ sont les deux valeurs centrées-réduites de la ligne i :]
  $ z_(i,1)=(x_(z,i)+y_(z,i))/sqrt(2), quad z_(i,2)=(x_(z,i)-y_(z,i))/sqrt(2) $
  #point[Première coordonnée : variation commune ; variance 1,8, soit 90 % du total 2. Seconde : contraste ; variance 0,2.]
  #note[Ces axes combinent les deux variables. Le choix des directions de variance maximale sera justifié par le problème d’optimisation.]
]
#frame[Choisir une direction de grande dispersion][
  #text(size: 18pt)[Une direction principale est un axe sur lequel le nuage projeté conserve le plus de variance. La projection orthogonale tombe perpendiculairement sur cet axe.]
  #fig("direction", height: 220pt)
  #ask[Pourquoi imposer une longueur unitaire à la direction ?]
]
#frame[L’ACP est un problème d’optimisation][
  #text(size: 18pt)[v : direction de p coefficients, de longueur un ; z : n coordonnées projetées, appelées scores. $s_z^2$ : variance corrigée de ces scores ; leur moyenne est nulle.]
  $ v^T v=1, quad z=A_c v in RR^n $
  $ s_z^2=(z^T z)/(n-1)=v^T S v, quad max_(v^T v=1) v^T S v $
  #point[Ici, variance signifie variance d’échantillon des scores observés. Les valeurs propres calculées décrivent cette table ; sans contrainte, multiplier v augmenterait cette variance arbitrairement.]
  #note[Pour v = (1,0), les scores sont la première colonne centrée, de variance $S_(1 1)$. Dans le TP, remplacer $A_c$, S par $A_z$, R : même raisonnement après centrage-réduction.]
]
#frame[Le Lagrangien : objectif et contrainte][
  #text(size: 18pt)[L’objectif est $f(v)=v^T S v$ ; la contrainte est $g(v)=v^T v-1=0$. Le scalaire $lambda$ est un multiplicateur inconnu.]
  $ L(v,lambda)=v^T S v-lambda(v^T v-1) $
  #text(size: 18pt)[$nabla_v$ regroupe les dérivées suivant les coordonnées de v. Comme S est symétrique :]
  $ nabla_v L=2S v-2lambda v=0 quad arrow.r quad S v=lambda v $
  $ (∂ L)/(∂ lambda)=-(v^T v-1)=0 $
  #point[Un vecteur propre non nul vérifie $S v=lambda v$ ; $lambda$ est sa valeur propre. Pour une direction unitaire, $v^T S v=lambda$ est la variance projetée.]
  #note[Ces équations donnent des candidats. Il reste à choisir celui qui réalise le maximum ; on ne maximise pas L conjointement en v et $lambda$.]
]
#frame[La plus grande valeur propre donne le maximum][
  #text(size: 18pt)[Le théorème spectral donne, pour S symétrique, une base orthonormée $(v_j)$ de vecteurs propres : longueurs un, produits scalaires nuls entre directions distinctes.]
  #text(size: 18pt)[Ordonnons $lambda_1>=dots>=lambda_p$. Les coordonnées de v dans cette base sont $alpha_j=v_j^T v$. Si v est unitaire :]
  $ v=sum_j alpha_j v_j, quad sum_j alpha_j^2=1, quad v^T S v=sum_j lambda_j alpha_j^2<=lambda_1 $
  #point[La borne est atteinte pour $v=v_1$. La variance sur ce premier axe est donc $lambda_1$.]
  #point[Pour le deuxième axe, imposer en plus l’orthogonalité au premier ; poursuivre pour les axes suivants.]
  #note[Dans l’exemple somme / contraste : 1,8 est la plus grande variance projetée ; 0,2 est celle de la direction orthogonale.]
]
#frame[Directions et scores : ne pas les confondre][
  #text(size: 18pt)[j,k indexent les directions, de 1 à p. La part de variance compare une variance projetée à la somme des p variances, supposée positive.]
  $ v_j in RR^p, quad z_j=A_c v_j in RR^n $
  $ s_(z_j)^2=lambda_j, quad (z_j^T z_k)/(n-1)=0 quad (j != k) $
  $ op("part de variance")_j=lambda_j/(sum_(ell=1)^p lambda_(ell)) $
  #point[Directions orthogonales ; scores non corrélés, pas forcément indépendants.]
  #note[Changer le signe d’un axe change le signe des scores, pas la reconstruction. Si plusieurs valeurs propres sont égales, leurs axes peuvent tourner dans le même sous-espace.]
]
#frame[Le TP : reconstruire les valeurs centrées-réduites][
  #text(size: 18pt)[Choisir k directions parmi p. $V_k$ les regroupe en colonnes ; $Z_k$ regroupe les scores. $hat(A)_z$ est la table centrée-réduite reconstruite.]
  $ V_k=(v_1,dots,v_k), quad Z_k=A_z V_k, quad hat(A)_z=Z_k V_k^T $
  #point[La reconstruction revient aux p variables : elle possède n lignes et p colonnes, même avec k = 2.]
  #point[L’erreur de Frobenius au carré additionne les carrés des erreurs de toutes les cellules. La mesurer ici sur les valeurs centrées-réduites.]
  #text(size: 18pt)[Retour facultatif aux mesures physiques : $overline(a)_j$ est la moyenne d’origine et $s_j$ son écart-type.]
  $ hat(A)_(i j)=overline(a)_j+s_j (hat(A)_z)_(i j) $
  #note[La reconstruction n’utilise aucune réponse à prédire. Les premières directions minimisent cette erreur pour un nombre k de coordonnées fixé.]
]
#frame[SVD économique : définir les facteurs et dimensions][
  #text(size: 18pt)[La décomposition en valeurs singulières sépare directions, échelles et scores. $q=min(n,p)$ ; $Sigma=op("diag")(sigma_1,…,sigma_q)$ avec $sigma_1>=dots>=sigma_q>=0$.]
  $ A_c=U Sigma V^T $
  $ U in RR^(n times q), quad Sigma in RR^(q times q), quad V in RR^(p times q) $
  $ U^T U=I_q, quad V^T V=I_q $
  #text(size: 18pt)[Les colonnes $u_j$ de U et $v_j$ de V sont orthonormées ; $I_q$ est l’identité de taille q. $sigma_j$ est une valeur singulière, distincte de l’écart-type $s_j$.]
  #ask[Quelle est la dimension du score $A_c v_j=sigma_j u_j$ ?]
]
#frame[La SVD calcule directement l’ACP][
  $ S=1/(n-1) V Sigma^T U^T U Sigma V^T $
  $ S=V (Sigma^T Sigma)/(n-1) V^T $
  $ lambda_j=sigma_j^2/(n-1), quad j=1,dots,q $
   #point[Les scores sont les colonnes de $U Sigma$. Les directions sont celles de V. Si q < p, les p−q autres valeurs propres de S sont nulles.]
  #point[Même calcul sur $A_z$ pour l’ACP centrée-réduite.]
  #note[Tronquer la SVD signifie conserver les k plus grandes valeurs singulières et leurs directions : on retrouve la reconstruction précédente.]
]
#frame[Trois contrôles pour construire le calcul][
  #point[*Table.* Après centrage-réduction : mêmes n lignes et p colonnes ; moyennes proches de zéro, variances proches de un.]
  #point[*Projection.* Une direction contient p coefficients ; une composante donne n scores. Vérifier les dimensions avant le produit.]
  #point[*Reconstruction.* Retrouver n lignes et p colonnes ; comparer l’erreur avec le retour aux moyennes.]
  #note[NumPy renvoie les directions en lignes dans `Vt`. Les calculs restent à construire dans le TP ; les indices repliables aident à vérifier les étapes.]
  #notebook("pca-practical", "trois points de contrôle du TP")
]
#frame[Beijing : l’échelle modifie les composantes][
  #text(size: 18pt)[CP1 et CP2 : première et deuxième composantes principales. Leurs scores sont les coordonnées de chaque station-heure sur les deux axes retenus.]
  #fig("pca", height: 225pt)
  #ask[Que préserve le graphique de gauche ? Que ne prouve pas celui de droite ?]
]
#frame[TP ACP : calculer, interpréter, comparer][
  #point[*Préparer.* Garder les mêmes observations complètes ; justifier covariance ou corrélation avant le calcul.]
  #point[*Calculer.* Directions, scores et parts de variance ; comparer directions de p coefficients et scores de n observations.]
  #point[*Lire.* Identifier les variables qui contribuent à un axe ; expliquer ce que signifie un score élevé pour une station-heure.]
  #point[*Comparer.* Reconstruire avec deux puis trois composantes sur les mêmes données centrées-réduites. Mesurer le gain de variance et la baisse d’erreur.]
  #note[45 minutes, de la minute 60 à 105. Calculs à construire ; trois contrôles et des indices facultatifs. Garder cinq minutes pour conclure.]
  #notebook("pca-practical", "TP guidé du 2 novembre")
]
#frame[Bilan : ce que votre ACP permet de dire][
  #point[*Choix.* Expliquer pourquoi le TP utilise la matrice R plutôt que S. Les unités et la fiabilité des mesures comptent dans cette décision.]
  #point[*Résultat.* Interpréter un axe avec ses coefficients et une station-heure ; comparer variance et erreur pour deux puis trois composantes.]
  #point[*Limite.* Une variance bien reconstruite décrit les entrées ; elle ne garantit pas qu’une quantité particulière soit bien estimée.]
  #ask[Quelle information perd-on en gardant seulement deux composantes ?]
  #note[Donner les dimensions d’une direction, de ses scores et de la table reconstruite. Relier l’erreur à la variance écartée.]
]#frame[Semaine suivante : régression et apprentissage][
  #point[*Nouvelle question.* Peut-on estimer PM2.5 avec PM10 et les mesures météorologiques disponibles à la même heure ? PM2.5 devient la réponse.]
  #point[*Régression, le 9 novembre.* Introduire une droite, ses coefficients et ses résidus, puis plusieurs variables explicatives.]
  #text(size: 18pt)[L’apprentissage supervisé utilise des exemples avec une réponse connue pour ajuster une règle ; on l’évalue ensuite sur d’autres observations.]
  #point[*Validation.* Ajuster transformations et coefficients sur l’apprentissage seulement ; comparer à une référence simple.]
  #note[Aucun ajustement de régression n’est requis aujourd’hui. Les preuves et l’expérience chronologique de Beijing sont disponibles comme préparation du 9 novembre.]
]

]
