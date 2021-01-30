from domino import *
N=16
floor=box(length=50,height=0.01,width=50,color=color.blue,pos=(0,-0.01,0))
Ds=[]
D=domino(pos=vector(0,a/2,-r),length=b,height=a,width=c,material=materials.wood)
D.fulcrum=D.pos+vector(-b/2,-a/2,0)
D.colli_point=D.fulcrum+vector(0,a,0)
D.orgin=D.fulcrum+r*D.omega_vec()
D.w_colli,D.w_gravity=vector(0,0,0),vector(0,0,0)
Ds.append(D)
for i in range(N-1):
    D=domino(length=b,height=a,width=c,material=materials.wood)
    D.orgin=Ds[0].orgin
    D.pos=D.orgin+rotate(Ds[-1].pos-D.orgin,pi/8,vector(0,1,0))
    D.fulcrum=D.orgin+rotate(-r*Ds[-1].omega_vec(),pi/8,vector(0,1,0))
    D.rotate(angle=(i+1)*pi/8,axis=vector(0,1,0),orgin=D.pos)
    D.colli_point=D.fulcrum+vector(0,a,0)
    D.w_colli,D.w_gravity=vector(0,0,0),vector(0,0,0)
    Ds.append(D)
Ds.append(Ds[0])

Ds[0].w_colli=5*Ds[0].omega_vec()
Vd,delta_E2=0,0
for i in range(N):
    x=range(i+1)
    while distance(Ds[i],Ds[i+1]) > b:
        rate(1000)
        t+=dt
        for j in x[-5:-1]:
            if distance(Ds[j],Ds[j+1])<=b: delta_E2=collision2(Ds[j],Ds[j+1],delta_E2)   #collision
        for j in x[-5:]: Ds[j].w_gravity+=cross(Ds[j].r(),vector(0,-M*g,0))*dt/I        #gravity
        for j in x[-5:]: Ds[j].rotation(dt)                                             #rotation
    #graph
    W_g,K_rot=0,0
    for j in x:
        W_g+=M*g*(a/2)-M*g*Ds[j].pos.y
        K_rot+=0.5*I*mag2(Ds[j].omega)
    Vd+=sqrt(r**2+(b/2)**2)*pi/8
    Vs=Vd/t
    g1.plot(pos=(t,Vs))
    g2.plot(pos=(t,K_rot))
    g3.plot(pos=(t,W_g))
    g4.plot(pos=(t,delta_E2))
    g5.plot(pos=(t,W_g+delta_E2))
