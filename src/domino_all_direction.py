from domino import *
floor=box(length=1200,height=0.01,width=1200,color=color.white,pos=(0,-0.01,0),opacity=0.5)
Ds=[]
D=domino(pos=vector(0,a/2,0),length=b,height=a,width=c,material=materials.wood)
D.fulcrum=D.pos+vector(-b/2,-a/2,0)
D.colli_point=D.fulcrum+vector(0,a,0)
D.w_colli,D.w_gravity=vector(0,0,0),vector(0,0,0)
Ds.append(D)
left,right=0,0
"""
Use w,s,a,d and space to generate different directions of dominos.
After determining the arangement, click the mouse and it will exeute.
"""
def keyinput(evt):
    global Ds,left,right
    s=evt.key
    move={' ','w','s','a','d','z','x'}
    if s in move:
        if s=='z' or s=='x':
            if s=='z':scene.center+=vector(-5,0,0)
            if s=='x':scene.center+=vector(5,0,0)
        else:
            D=domino(length=b,height=a,width=c,material=materials.wood)
            if s==' ':
                Ds[-1].col=1 #collision type1
                D.pos=Ds[-1].pos+(b+d)*Ds[-1].J_vec()
                D.fulcrum=D.pos-sqrt(a**2+b**2)/2*norm(Ds[-1].r())
            if s=='w':
                Ds[-1].col=1 #collision type1
                D.pos=Ds[-1].pos+(b+d)*Ds[-1].J_vec()+vector(0,0.8,0)
                D.fulcrum=D.pos-sqrt(a**2+b**2)/2*norm(Ds[-1].r())
            if s=='s':
                Ds[-1].col=1 #collision type1
                D.pos=Ds[-1].pos+(b+d)*Ds[-1].J_vec()-vector(0,0.8,0)
                D.fulcrum=D.pos-sqrt(a**2+b**2)/2*norm(Ds[-1].r())
            if s=='a':
                Ds[-1].col=2 #collision type2
                left+=1
                Ds[-1].orgin=Ds[-1].fulcrum+r*Ds[-1].omega_vec()
                D.pos=Ds[-1].orgin+rotate(Ds[-1].pos-Ds[-1].orgin,pi/8,vector(0,1,0))
                D.fulcrum=Ds[-1].orgin+rotate(-r*Ds[-1].omega_vec(),pi/8,vector(0,1,0))
            if s=='d':
                Ds[-1].col=2 #collision type2
                right+=1
                Ds[-1].orgin=Ds[-1].fulcrum-r*Ds[-1].omega_vec()
                D.pos=Ds[-1].orgin+rotate(Ds[-1].pos-Ds[-1].orgin,-pi/8,vector(0,1,0))
                D.fulcrum=Ds[-1].orgin+rotate(r*Ds[-1].omega_vec(),-pi/8,vector(0,1,0))
            D.rotate(angle=(left-right)*pi/8,axis=vector(0,1,0),orgin=D.pos)
            D.colli_point=D.fulcrum+vector(0,a,0)
            D.w_colli,D.w_gravity=vector(0,0,0),vector(0,0,0)
            Ds.append(D)
scene.bind('keydown', keyinput)

Ds[0].w_colli=vector(0,0,3)
delta_E1,delta_E2,Vd=0,0,0
scene.waitfor('click')
for i in range(len(Ds)-1): #push the first domino
    scene.center=Ds[i].pos                      #let the scene synchronize with dominos
    #scene.forward=Ds[i].J_vec()+vector(0,-0.3,0)
    x=range(i+1)
    while distance(Ds[i],Ds[i+1]) > b:
        rate(1000)
        t+=dt
        for j in x[-5:-1]:                                                          #collision
            if distance(Ds[j],Ds[j+1])<=b:
                if Ds[j].col==1: delta_E1=collision1(Ds[j],Ds[j+1],delta_E1)        #type1
                if Ds[j].col==2: delta_E2=collision2(Ds[j],Ds[j+1],delta_E2)        #type2
        for j in x[-5:]: Ds[j].w_gravity+=cross(Ds[j].r(),vector(0,-M*g,0))*dt/I    #gravity
        for j in x[-5:]: Ds[j].rotation(dt)                                         #rotation
    if i==len(Ds)-2: #for the last domino
        x=range(i+2)
        while Ds[-1].colli_point.y>Ds[-1].fulcrum.y:
            rate(1000)
            for j in x[-5:-1]:                                                          #collision
                if distance(Ds[j],Ds[j+1])<=b:
                    if Ds[j].col==1: delta_E1=collision1(Ds[j],Ds[j+1],delta_E1)        #type1
                    if Ds[j].col==2: delta_E2=collision2(Ds[j],Ds[j+1],delta_E2)        #type2
            for j in x[-5:]: Ds[j].w_gravity+=cross(Ds[j].r(),vector(0,-M*g,0))*dt/I    #gravity
            for j in x[-5:]: Ds[j].rotation(dt)
                
##    #graph
##    W_g,K_rot=0,0
##    for j in range(len(Ds)):
##        W_g+=M*g*a/2-M*g*Ds[j].pos.y
##        K_rot+=0.5*I*mag2(Ds[j].omega)
##    if Ds[i].col==1:Vd+=b+d
##    if Ds[i].col==2:Vd+=sqrt(r**2+(b/2)**2)*pi/8
##    Vs=Vd/t
##    g1.plot(pos=(t,Vs))
##    g2.plot(pos=(t,K_rot))
##    g3.plot(pos=(t,W_g))
##    g4.plot(pos=(t,delta_E1+delta_E2))
##    g5.plot(pos=(t,W_g+delta_E1+delta_E2))
print("end")
while 1:
    rate(1000)
    pass
