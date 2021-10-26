import cadquery as cq
from math import pi
import random as rd

#Generate 100 random bottles
for i in range(100):
    
    #Setting parameters
    a=rd.random()
    THeight, MHeight, BHeight, radius = 2*a, rd.random() ,3*a , rd.gauss(2.2, 0.6)
    RDiff=1/4
    ROffset=1/4
    NRings = rd.randint(2,10)
    RRadius = radius - RDiff
    
    #Volume Calculation
    BPart_Volume = pi*(radius**2)*BHeight
    TPart_Volume = pi*(radius**2)*THeight
    MPart_Height = NRings*((pi/3)*ROffset*((radius**2)+(RRadius**2) + radius*RRadius) + pi*(radius**2)*MHeight) 
    Bottle_Volume = BPart_Volume + TPart_Volume + MPart_Height
    
    #Construction of the Bottom Part
    Bresult = (cq.Workplane("front").
               circle(radius).workplane(offset=BHeight).circle(radius).loft(combine = True).edges('%CIRCLE and <Z').fillet(1))
              
    
    for i in range(NRings):
        Bresult = (Bresult.faces(">Z").workplane(centerOption="CenterOfMass")
                   .circle(radius).workplane(offset=ROffset).circle(RRadius).loft(combine = True)
                   
                   .faces(">Z").workplane(centerOption="CenterOfMass")
                   .circle(RRadius).workplane(offset=ROffset).circle(radius).loft(combine = True)
                   
                   .faces(">Z").workplane(centerOption="CenterOfMass")
                   .circle(radius).workplane(offset=MHeight).circle(radius).loft(combine = True))
        
        
        
        Tresult = (Bresult.faces(">Z").workplane(centerOption="CenterOfMass")
                   .circle(radius).workplane(offset=THeight).circle(radius).loft(combine = True)
                   
                   .shell(.15)
                   )
        
        
        #Construction of the Top Part
        distZ, distX = rd.uniform(0.4,0.85), radius/3
        
        sPnts = [
            (distX,distZ*4),
            (2*distX+0.1,distZ*2),
            (distX*3+0.15,0)
            ]
        
        topPart = cq.Workplane("XZ").lineTo(0,distZ*5).lineTo(distX,distZ*5).lineTo(distX,distZ*4+0.01)
        topPart = topPart.spline(sPnts,includeCurrent=True).close()
        
        topPart = topPart.revolve(axisStart=(0,0), axisEnd=(0,1),clean=True)
        
        #Assembly of both parts
        topPart=topPart.translate((0,0,THeight + BHeight + 2*ROffset*NRings + (NRings)*MHeight))
        result = Bresult.union(Tresult).union(topPart)
        
        #Exporting the mesh in STL format
        exporters.export(result, 'btl'+str(i)+'.png')



