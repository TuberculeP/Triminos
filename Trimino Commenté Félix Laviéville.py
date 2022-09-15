import random
import turtle
import math
turtle.clear()
turtle.home()
turtle.colormode(255)
turtle.speed(0)

def creeTrou(n):
    '''Crée des coordonnées aléatoires parmi un cadrillage de taille 2**n'''
    
    return (random.randint(0,2**n-1),random.randint(0,2**n-1))


def dessineProbleme(x,y,n,a,trou=None):
    '''Trace un carré de côté 2**n*a et construit le trou (donné ou non)'''
    
    #on crée le trou si il n'est pas donné
    if trou==None: trou=creeTrou(n)
    
    turtle.pu()
    turtle.goto(x,y)
    
    #on trace le carré
    turtle.pd()
    for i in range(4):
        turtle.forward(2**n*a)
        turtle.left(90)
    
    #on se place pour tracer le trou
    turtle.pu()
    turtle.goto(x+trou[0]*a,y+trou[1]*a)
    
    #on trace le trou et on le colorie en gris
    turtle.pd()
    turtle.fillcolor("grey")
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(a)
        turtle.left(90)
    turtle.end_fill()
    turtle.pu()


def dessineTrimino(n):
    '''Dessine un trimino de taille n à l'emplacement et orientation actuels de turtle'''
    
    turtle.pd()
    
    #on définit une couleur aléatoire de remplissage parce que c'est rigolo
    turtle.fillcolor(random.randint(10,240), random.randint(10,240), random.randint(10,240))
    turtle.begin_fill()
    
    #on trace le trimino
    for i in range(2):
        turtle.forward(n)
        turtle.right(90)
    for i in range(2):
        turtle.forward(2*n)
        turtle.right(90)
    turtle.forward(n)
    turtle.right(90)
    turtle.forward(n)
    turtle.left(90)
    turtle.end_fill()
    turtle.pu()


def casBase(a,trou=None):
    '''cas initial où le carré est de type 2x2 et où il n'y a que 4 possibilités'''
    
    #on crée le trou si il n'est pas donné
    if trou==None: trou=creeTrou(1)
    
    #on dessine le grand carré et le trou
    dessineProbleme(-a, -a, 1, a, trou)
    
    if round(turtle.xcor())==-a and round(turtle.ycor())==-a:
        #trou en bas a gauche du carré
        for i in range(2):
            turtle.forward(a)
            turtle.left(90)
            
    elif round(turtle.xcor())==-a:
        #trou en haut à gauche du carré
        turtle.forward(a)
        turtle.left(90)
    
    elif round(turtle.ycor())==-a:
        #trou en bas à droite du carré
        turtle.right(90)
        turtle.backward(a)
    
    #sinon le trou est en haut a droite du carré
    
    dessineTrimino(a)
        
    

def dessineComplexe(taille,ordre):
    '''Dessine un trimino qui selon son ordre sera formé de plusieurs triminos de taille inférieure'''
    
    #si l'ordre est 1 alors il n'y a q'un trimino simple a tracer
    if ordre==1:
        dessineTrimino(taille)
    
    #sinon on dessine un trimino qui sera lui-même formé de quatre triminos d'ordre inférieur de 1
    #la récurrence s'arrête lorsque l'on atteint l'ordre 1
    else:
        #on dessine le premier trimino
        dessineComplexe(taille,ordre-1)
        
        #la complexité des longueurs dans forward est dûe à la taille des triminos qui augmente de puissance 
        #en fonction de l'ordre qui lui varie de façon arithmétique, il faut donc trouver un moyen de lier les deux
        
        #on se place pour tracer le prochain trimino
        for i in range(2):
            turtle.forward(taille*(2**(ordre-2)))
            turtle.right(90)
        turtle.right(90)
        
        #on dessine le deuxième trimino
        dessineComplexe(taille,ordre-1)
        
        #on se place pour tracer le prochain trimino puis on le trace
        for i in range(2):
            turtle.left(90)
            turtle.forward(2*taille*(2**(ordre-2)))
            turtle.right(180)
            dessineComplexe(taille,ordre-1)
        
        #on se replace pour se retrouver au même endroit où on a commencé
        turtle.left(90)
        turtle.forward(taille*(2**(ordre-2)))
        turtle.right(90)
        turtle.forward(taille*(2**(ordre-2)))
        turtle.left(90)


def solutionProbleme(n,a,taillebase):
    '''Solution finale de récurrence :
    un trimino sera construit à côté du trou de façon à former un "nouveau trou" dans un cadrillage de taille 2**(n-1).
    Ainsi de suite, un trimino sera construit par rapport au nouveau trou mais celui ci sera formé lui même de triminos
    grâce à la fonction dessineComplexe. On ne verra plus que les triminos de taille taillebase (qui ne varie pas)'''
    
    #on identifie où se trouve le trou par rapport à un cadrillage d'ordre inférieur en vérifiant par le calcul
    #si la tortue est sur une ligne et une colonne paire ou impaire. A partir de cette info on peut savoir comment tracer
    #le trimino
    
    #la difficulté réside dans le fait que nous nous sommes affranchi de x et y en faisant en sorte que le carré soit
    #toujours centré alors on utilise la fonction absolue
    #la fonction arrondie est nécéssaire pour les vérifications car turtle peut renvoyer 49,999 losqu'il se trouve à 50
    
    #on vérifie le positionnement de la tortue et on se place en fonction pour tracer le trimino
    if (abs(round(turtle.xcor()))/a+2**n/2)%2==0 and (abs(round(turtle.ycor()))/a+2**n/2)%2==0:
    #trou en bas à gauche d'un potentiel carré
        for i in range(2):
            turtle.forward(a)
            turtle.left(90)
            
    elif (abs(round(turtle.xcor()))/a+2**n/2)%2==0:
    #trou en haut à gauche d'un potentiel carré
        turtle.forward(a)
        turtle.left(90)
    
    elif (abs(round(turtle.ycor()))/a+2**n/2)%2==0:
    #trou en bas à droite d'un potentiel carré
        turtle.right(90)
        turtle.backward(a)

    #sinon le trou est en haut à droite d'un potentiel carré
    
    #comme pour dessineComplexe, on doit calculer l'ordre du trimino complexe en fonction de sa taille, comme nous
    #sommes dans des puissances de 2 il faut utiliser la fonction log du module Math
    
    
    dessineComplexe(taillebase, math.log(a/taillebase,2)+1)
    
    #on se place en bas à gauche du "nouveau trou" et on relance la récurrence
    turtle.pu()
    turtle.goto(turtle.xcor()-a,turtle.ycor()-a)
    turtle.setheading(0)
    
    #la récurrence s'arrête quand le "nouveau trou" est en fait le grand carré, donc quand il est rempli
    if n-1!=0:
        solutionProbleme(n-1, a*2,taillebase)


def problemeFinal(n,a,trou=None):
    '''Fonction d'initialisation pour tracer le grand carré au centre de l'écran, tracer le trou puis lancer le remplissage.
    Le trou peut être donné ou non'''
    
    #on définit x et y pour que le carré soit centré
    x=-(2**n*a/2)
    y=-(2**n*a/2)
    
    #on crée le trou si il n'est pas donné
    if trou==None: trou=creeTrou(n)
    
    #on dessine le grand carré et le trou
    dessineProbleme(x, y, n, a, trou)
    
    #on remplit de triminos par récurrence
    if n!=0: solutionProbleme(n,a,a)

problemeFinal(4,30)