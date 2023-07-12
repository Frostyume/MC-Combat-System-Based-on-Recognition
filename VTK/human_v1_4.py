import time
import vtk

class WalkTimerCallback():
    def __init__(self,speed,actors):
        self.angle = 20
        self.xspeed = speed
        self.speed = speed
        self.zspeed = 0
        self.actors = actors
        self.count = 0

    def execute(self,obj,event):
        
        self.actors[2].RotateY(self.angle)
        self.actors[3].RotateY(-self.angle)
        self.actors[4].RotateY(-self.angle)
        self.actors[5].RotateY(self.angle)

        for i in range(len(self.actors)):
            x,y,z=self.actors[i].GetPosition()
            self.actors[i].SetPosition(x+self.xspeed,y,z+self.zspeed)

        x,y,z = self.actors[0].GetPosition()    
        if(z>0):
            self.zspeed = -10
            self.xspeed = 0
        else:
            self.zspeed = 0
            self.xspeed = self.xspeed

        iren = obj
        iren.GetRenderWindow().Render()
        self.angle =self.angle*-1

        print(Camera.GetPosition())
        print(Camera.GetViewUp())
        print(Camera.GetFocalPoint())
        print(Camera.GetViewAngle())

class FireBumpTimerCallback():
    def __init__(self,actor,chaser):
        self.actor = actor
        self.chaser = chaser
        self.speed = 20
        
    
    def execute(self,obj,event):
        x,y,z=self.actor.GetPosition()
        x0,y0,z0 = self.chaser[0].GetPosition()
        if(x<x0):
            self.actor.SetPosition(x+self.speed,y,z)
        else:
            self.actor.SetPosition(5000,y,z)
            
            Property1 = vtk.vtkProperty()
            Property1.SetColor(255, 0, 0)
            Property1.SetDiffuse(0.7)
            Property1.SetSpecular(0.4)
            Property1.SetSpecularPower(20)
            for i in range(len(self.chaser)):
                self.chaser[i].SetProperty(Property1)

        iren = obj
        iren.GetRenderWindow().Render()

class IceBumpTimerCallback():
    def __init__(self,actor,chaser):
        self.actor = actor
        self.chaser = chaser
        self.speed =30
        
    
    def execute(self,obj,event):
        x,y,z=self.actor.GetPosition()
        x0,y0,z0 = self.chaser[0].GetPosition()
        if(x<x0):
            self.actor.SetPosition(x+self.speed,y,z)
        else:
            self.actor.SetPosition(5000,y,z)
            walkTimer2.xspeed = 5

            Property1 = vtk.vtkProperty()
            Property1.SetColor(185, 205, 246)
            Property1.SetDiffuse(0.7)
            Property1.SetSpecular(0.4)
            Property1.SetSpecularPower(20)
            for i in range(len(self.chaser)):
                self.chaser[i].SetProperty(Property1)

        

        iren = obj
        iren.GetRenderWindow().Render()
        
class TNTTimerCallback():
    def __init__(self,actor,chaser):
        self.high = 0
        self.actor = actor
        self.chaser = chaser
        self.count = 0

    def execute(self,obj,event):

        x,y,z = self.chaser.actors[0].GetPosition()
        x0,y0,z0 = self.actor.GetPosition()

        Property = vtk.vtkProperty()
        Property.SetColor(0, 0, 0)
        if self.count<20:
            if self.count%2!=0:
                Property.SetColor(0, 0, 0)
            else:
                Property.SetColor(255, 255, 255)
        self.count+=1
        self.actor.SetProperty(Property)

        if self.count == 20:
            walkTimer2.zspeed = 100

        iren = obj
        iren.GetRenderWindow().Render()

class CageTimerCallback():
    def __init__(self,cage,chaser):
        self.cage = cage
        self.chaser = chaser

    def execute(self, obj, event):
        x = self.cage.x
        y = self.cage.y
        z = self.cage.z
        
        x0,y0,z0 = self.chaser.actors[0].GetPosition()

        transform = vtk.vtkTransform()
        transform.Scale(0.5,0.5,40)
        if(x0<x+10 and x0>x-10):
            for i in range(len(self.cage.actors)):
                if i!=4:
                    self.cage.actors[i].SetUserTransform(transform)
                    self.cage.actors[i].SetPosition(x,y,z)
            walkTimer2.xspeed = 0
        iren = obj
        iren.GetRenderWindow().Render()

class LightningTimerCallback():
    def __init__(self,lightning,chaser):
        self.lightning = lightning
        self.chaser = chaser
    
    def execute(self, obj, event):
        x,y,z=self.lightning.actor.GetPosition()
        x0,y0,z0 = self.chaser[0].GetPosition()

        if(x-10<x0 and x0<x+10):
            walkTimer2.xspeed = 2
            self.lightning.actor.SetPosition(5000,y,z)

            Property1 = vtk.vtkProperty()
            Property1.SetColor(0, 253, 150)
            Property1.SetDiffuse(0.7)
            Property1.SetSpecular(0.4)
            Property1.SetSpecularPower(20)
            for i in range(len(self.chaser)):
                self.chaser[i].SetProperty(Property1)

Property = vtk.vtkProperty()
Property.SetColor(0, 1, 0)
Property.SetDiffuse(0.7)
Property.SetSpecular(0.4)
Property.SetSpecularPower(20)

file_address="D:\\WorkProject\\Open Source HardWare\\VTKHomework\\"
file_names = ["head.stl","body.stl","leftarm.stl","rightarm.stl","leftleg.stl","rightleg.stl"]
rotateOrigin = {"head.stl":(0,0,0),"body.stl":(0,0,0),"leftarm.stl":(5,-20,60),"rightarm.stl":(5,20,60),
                "leftleg.stl":(5,-5,40),"rightleg.stl":(5,5,40)}

class Human():
    def __init__(self,x1,y1,z1):
        bodyparts=[]
        for i in range(len(file_names)):
            Reader = vtk.vtkSTLReader()
            Reader.SetFileName(file_address+file_names[i])
    
            Mapper = vtk.vtkPolyDataMapper()
            Mapper.SetInputConnection(Reader.GetOutputPort())

            Actor=vtk.vtkActor()
            Actor.SetMapper(Mapper)
            Actor.SetProperty(Property)
            
            x,y,z = rotateOrigin[file_names[i]]
            Actor.SetOrigin(x,y,z)

            x0,y0,z0 = Actor.GetPosition()
            Actor.SetPosition(x0+x1,y0+y1,z0+z1)

            bodyparts.append(Actor)
        
        self.actors = bodyparts

class Plane():
    def __init__(self):
        plane = vtk.vtkPlaneSource()
        plane.SetXResolution(50)
        plane.SetYResolution(50)
        plane.SetCenter(0,0,0)
        plane.SetNormal(0,0,1)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetRepresentationToWireframe()
        #actor.GetProperty().SetOpacity(0.4)  # 1.0 is totally opaque and 0.0 is completely transparent

        transform = vtk.vtkTransform()
        transform.Scale(2000,2000, 1)#规模
        actor.SetUserTransform(transform)

        self.actor = actor

class Sphere():
    def __init__(self,x,y,z):
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(x,y,75)
        sphere.SetRadius(5)

        #Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.actor = actor

class Cube():
    def __init__(self,x,y,z,xl,yl,zl):
        cube = vtk.vtkCubeSource()
        cube.SetCenter(x,y,z-25)
        cube.SetXLength(xl)
        cube.SetYLength(yl)
        cube.SetZLength(zl)

        #Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.actor = actor
    
class Cage():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

        self.actors = []
        length = 50
        for i in range(0,3):
            for j in range(0,3):
                cube = vtk.vtkCubeSource()
                cube.SetCenter(x+(i-1)*length,y+(j-1)*length,z)
                cube.SetXLength(length)
                cube.SetYLength(length)
                cube.SetZLength(2)

                #Create a mapper and actor
                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection(cube.GetOutputPort())
        
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                self.actors.append(actor)

file_name = "lightning.stl"
class Lightning():
    def __init__(self,x,y,z):
        Reader = vtk.vtkSTLReader()
        Reader.SetFileName(file_address+file_name)

        Mapper = vtk.vtkPolyDataMapper()
        Mapper.SetInputConnection(Reader.GetOutputPort())

        Property1 = vtk.vtkProperty()
        Property1.SetColor(253, 253, 150)

        Actor=vtk.vtkActor()
        Actor.SetMapper(Mapper)
        Actor.SetPosition(x,y,z)
        Actor.SetProperty(Property1)

        self.actor = Actor


Interactor = vtk.vtkRenderWindowInteractor()
RenderWindow = vtk.vtkRenderWindow()
Render = vtk.vtkRenderer()
Render.SetBackground(0.1, 0.2, 0.4)

Camera = Render.GetActiveCamera()
Camera.SetPosition(-707.739081445586, -612.7302383291877, 1136.6778468715568)
Camera.SetViewUp(0.25263156642518736, 0.3238438155067556, 0.9117579036145409)
Camera.SetFocalPoint(50,0,0)
#人物初始化
human1 = Human(0,0,0)
human2 = Human(200,0,0)
for j in range(len(human1.actors)):
    Render.AddActor(human1.actors[j])
for j in range(len(human2.actors)):
    Render.AddActor(human2.actors[j])

#平面初始化
plane = Plane()
Render.AddActor(plane.actor)


##具体技能实现
#火球 被球命中后燃烧
#追逐动作设置
'''
walkTimer1 = WalkTimerCallback(10,human1.actors) 
walkTimer2 = WalkTimerCallback(5,human2.actors)

RenderWindow.AddRenderer(Render)
RenderWindow.SetSize(500, 500)
RenderWindow.Render()

Interactor.SetRenderWindow(RenderWindow)

Interactor.Initialize()

Interactor.AddObserver('TimerEvent', walkTimer1.execute)
Interactor.AddObserver('TimerEvent', walkTimer2.execute)
timerId = Interactor.CreateRepeatingTimer(250)

x,y,z = human1.actors[0].GetPosition()
sphere = Sphere(x,y,z)
Render.AddActor(sphere.actor)

bumpTimer = FireBumpTimerCallback(sphere.actor,human2.actors)
Interactor.AddObserver('TimerEvent', bumpTimer.execute)

Interactor.Start()
'''
#冰球 被球命中后减速
'''
walkTimer1 = WalkTimerCallback(10,human1.actors) 
walkTimer2 = WalkTimerCallback(10,human2.actors)

RenderWindow.AddRenderer(Render)
RenderWindow.SetSize(500, 500)
RenderWindow.Render()

Interactor.SetRenderWindow(RenderWindow)

Interactor.Initialize()

Interactor.AddObserver('TimerEvent', walkTimer1.execute)
Interactor.AddObserver('TimerEvent', walkTimer2.execute)
timerId = Interactor.CreateRepeatingTimer(250)

x,y,z = human1.actors[0].GetPosition()
sphere = Sphere(x,y,z)
Render.AddActor(sphere.actor)

bumpTimer = IceBumpTimerCallback(sphere.actor,human2.actors)
Interactor.AddObserver('TimerEvent', bumpTimer.execute)

Interactor.Start()
'''
#TNT爆炸
'''
walkTimer1 = WalkTimerCallback(20,human1.actors) 
walkTimer2 = WalkTimerCallback(15,human2.actors)

RenderWindow.AddRenderer(Render)
RenderWindow.SetSize(500, 500)
RenderWindow.Render()

Interactor.SetRenderWindow(RenderWindow)

Interactor.Initialize()

Interactor.AddObserver('TimerEvent', walkTimer1.execute)
Interactor.AddObserver('TimerEvent', walkTimer2.execute)
timerId = Interactor.CreateRepeatingTimer(250)

x,y,z = human2.actors[0].GetPosition()
cube = Cube(x+400,y,z,50,50,50)
Render.AddActor(cube.actor)

TNTTimer = TNTTimerCallback(cube.actor,human2)
Interactor.AddObserver('TimerEvent', TNTTimer.execute)

Interactor.Start()
'''
#笼子
'''
walkTimer1 = WalkTimerCallback(20,human1.actors) 
walkTimer2 = WalkTimerCallback(15,human2.actors)

RenderWindow.AddRenderer(Render)
RenderWindow.SetSize(500, 500)
RenderWindow.Render()

Interactor.SetRenderWindow(RenderWindow)

Interactor.Initialize()

Interactor.AddObserver('TimerEvent', walkTimer1.execute)
Interactor.AddObserver('TimerEvent', walkTimer2.execute)
timerId = Interactor.CreateRepeatingTimer(250)

x,y,z = human2.actors[0].GetPosition()
cage = Cage(x+100,y,z)
for i in range(len(cage.actors)):
    Render.AddActor(cage.actors[i])

CageTimer = CageTimerCallback(cage,human2)
Interactor.AddObserver('TimerEvent', CageTimer.execute)

Interactor.Start()
'''
#闪电

walkTimer1 = WalkTimerCallback(10,human1.actors) 
walkTimer2 = WalkTimerCallback(10,human2.actors)

RenderWindow.AddRenderer(Render)
RenderWindow.SetSize(500, 500)
RenderWindow.Render()

Interactor.SetRenderWindow(RenderWindow)

Interactor.Initialize()

Interactor.AddObserver('TimerEvent', walkTimer1.execute)
Interactor.AddObserver('TimerEvent', walkTimer2.execute)
timerId = Interactor.CreateRepeatingTimer(250)

lightning = Lightning(300,0,100)
Render.AddActor(lightning.actor)

LightningTimer = LightningTimerCallback(lightning,human2.actors)
Interactor.AddObserver('TimerEvent', LightningTimer.execute)


Interactor.Start()
