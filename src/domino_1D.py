from domino import*
N=16
floor=box(length=1200,height=0.01,width=12,color=color.blue,pos=(0,-0.01,0))
Ds=[]
for i in range(N):
    D=domino(pos=vector(-i*(b+d),a/2,0),length=b,height=a,width=c,material=materials.wood)
    D.fulcrum=D.pos+vector(-b/2,-a/2,0)
    D.colli_point=D.pos+vector(-b/2,a/2,0)
    D.w_colli,D.w_gravity=vector(0,0,0),vector(0,0,0)
    Ds.append(D)

#use keyboard (a,w,s,d),(q,e) to change the scene.center and scene.forward respectively
def keyinput(evt): 
    move={'a':vector(-5,0,0),'d':vector(5,0,0),'w':vector(0,0,-1),'s':vector(0,0,1)}
    axle={'e':vector(0.1,0,0),'q':vector(-0.1,0,0)}
    s=evt.key
    if s in move : scene.center+=move[s]
    if s in axle : scene.forward+=axle[s]
scene.bind('keydown', keyinput)

Ds[0].w_colli=vector(0,0,5) #initial angular velocity
Vd,delta_E1=0,0
for i in range(N-1): #push the first domino
    x=range(i+1)
    while distance(Ds[i],Ds[i+1]) > b: #before hitting the next one
        rate(1000)
        t+=dt
        for j in x[-5:-1]:
            if distance(Ds[j],Ds[j+1])<=b: delta_E1=collision1(Ds[j],Ds[j+1],delta_E1) #collision
        for j in x[-5:]: Ds[j].w_gravity+=cross(Ds[j].r(),vector(0,-M*g,0))*dt/I       #gravity
        for j in x[-5:]: Ds[j].rotation(dt)                                            #rotation
    if i==len(Ds)-2: #for the last domino
        x=range(i+2)
        while Ds[-1].colli_point.y>Ds[-1].fulcrum.y:
            rate(10000)
            for j in x[-5:-1]:                                                          #collision
                if distance(Ds[j],Ds[j+1])<=b: delta_E1=collision1(Ds[j],Ds[j+1],delta_E1)        
            for j in x[-5:]: Ds[j].w_gravity+=cross(Ds[j].r(),vector(0,-M*g,0))*dt/I    #gravity
            for j in x[-5:]: Ds[j].rotation(dt)
    #graph
    W_g,K_rot=0,0
    for j in x:
        W_g+=M*g*(a/2)-M*g*Ds[j].pos.y
        K_rot+=0.5*I*mag2(Ds[j].omega)
    Vd+=b+d
    Vs=Vd/t
    g1.plot(pos=(t,Vs))
    g2.plot(pos=(t,K_rot))
    g3.plot(pos=(t,W_g))
    g4.plot(pos=(t,delta_E1))
    g5.plot(pos=(t,W_g+delta_E1))
