from visual import*
from visual.graph import*
g=9.8
a,b,c=6.,1.5,4.     #scale of the domino
M=5.                #mass of the domino
I=M*(a**2+b**2)/3   #rotational inertia of the domino
d=4.0               #the distance between dominos(3.5~4.5)
r=12.               #the radius of curvature
mu=2.               #collision coefficient
t,dt=0,0.001
scene=display(width=1000,height=1000,range=40,background=(0,0.5,0))
class domino(box):
    omega=vector(0,0,0)
    def __init__(self,*args,**kargs):
        self=box.__init__(self,*args,**kargs)
    def R(self):
        return self.colli_point-self.fulcrum
    def r(self):
        return self.pos-self.fulcrum
    def omega_vec(self): #direction of angular velocity
        return norm(cross(self.r(),self.R()))
    def J_vec(self):
        return norm(cross(self.omega_vec(),self.R()))
    def rotation(self,dt): #rotation function
        self.omega=self.w_colli+self.w_gravity
        self.delta_phi=mag(self.omega)*dt
        self.rotate(angle=self.delta_phi,axis=self.omega_vec(),origin=self.fulcrum)
        self.colli_point=self.fulcrum+rotate(self.colli_point-self.fulcrum,self.delta_phi,self.omega_vec())
#the distance between collision1 point of former domino and the collision1 plane of latter domino
def distance(a1,a2):
    return abs(dot(a2.J_vec(),a1.colli_point)-dot(a2.J_vec(),a2.fulcrum))/mag(a2.J_vec())
def collision1(a1,a2,delta_E1): #collision type1 formula
    R12=a1.colli_point-a2.fulcrum
    r1=-mag(cross(a1.R(),-a2.J_vec()))
    r2=mag(cross(R12,a2.J_vec()))
    J=-2*I*(r1*mag(a1.omega)+r2*mag(a2.omega))/(r1**2+r2**2+I/M*mu)*a2.J_vec()
    a1.w_colli+=cross(a1.R(),-J)/I
    a2.w_colli+=cross(R12,J)/I
    delta_E1+=-mu*mag2(J)/(2*M)
    return delta_E1
def collision2(a1,a2,delta_E2): #collision type2 formula
    R12=a1.colli_point-a1.orgin-proj(a1.colli_point-a1.orgin,a2.fulcrum-a1.orgin)
    Jeff_vec=-a2.J_vec()-proj(-a2.J_vec(),a1.omega_vec())
    r1=-mag(cross(a1.R(),Jeff_vec))
    r2=mag(cross(R12,a2.J_vec()))
    J=-2*I*(r1*mag(a1.omega)+r2*mag(a2.omega))/(r1**2+r2**2+I/M*mu)*a2.J_vec()
    Jeff=-J-proj(-J,a1.omega_vec())
    a1.w_colli+=cross(a1.R(),Jeff)/I
    a2.w_colli+=cross(R12,J)/I
    delta_E2+=-(mu*mag2(J)+mag2(-J-Jeff))/(2*M)
    return delta_E2
###graph
scene1=gdisplay(y=0,width=800,height=250,xtitle='time',ytitle='spread velocity',background=(0.5,0.35,0.25))
scene2=gdisplay(y=250,width=800,height=250,xtitle='time',ytitle='kinetic energy',background=(0.2,0.38,0.6))
scene3=gdisplay(y=500,width=800,height=250,xtitle='time',ytitle='energy',background=(0.35,0.5,0.25))
g1=gcurve(color=color.yellow,gdisplay=scene1)
g2=gcurve(color=color.black,gdisplay=scene2)
g3=gcurve(color=color.red,gdisplay=scene3)
g4=gcurve(color=color.blue,gdisplay=scene3)
g5=gcurve(color=color.white,gdisplay=scene3)
