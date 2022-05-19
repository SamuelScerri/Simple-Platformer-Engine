import Bugger
import pygame
import sys
import time
import math

Data=	[
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,12,1,1,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,1,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,59,60,59,14,15,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,12,1,1,15,15,15,1,1,1,1,1,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15,15,15,15,15,15,15,15,15,16,0,0,0,12,1,1,1,13,0,0,0,0,0,0,0,
			0,0,0,0,0,0,0,0,0,0,0,0,0,14,15,15,15,15,15,15,15,15,15,15,16,0,0,0,14,15,15,15,16,0,0,0,0,0,0,0,
		]

Data2=	[
			59,58,60,59,58,59,58,
			12,1,1,1,1,1,13,
			14,15,15,15,15,15,16,
			14,15,15,15,15,15,16,
			14,15,15,15,15,15,16,
		]

Sprite=Bugger.GraphicResource.LoadImage("sheet(1).png")
Player=Bugger.GraphicResource.LoadImage("characters.png")
TilemapSprite=Bugger.GraphicResource.LoadImage("Tilemap.png")

Manager=Bugger.ScenarioManagement("Bugger Engine",16*20,16*10)
Level=Bugger.ResourceManagement("Level 1",0,0,Manager.ReturnLength,Manager.ReturnBreath)

Level.InsertResource(Bugger.TilemapResource("Tilemap",Sprite,0,0,10,7,Data,40,10))
Level.InsertResource(Bugger.TilemapResource("Tilemap2",Sprite,40,125,10,7,Data2,7,5))

Level.InsertResource(Bugger.ResourceManagement("Player",100,100,16,16))
Level.ReturnResource(Level.SearchResource("Player")).InsertResource(Bugger.GraphicResource("Player Sprite",Player,-8,-16,23,4))

Manager.ChangeResource(Level)

CurrentTime=time.perf_counter()

SpeedX=0
SpeedY=0

Grounded=False
Yes=0

while(True):
	DT=time.perf_counter()-CurrentTime
	CurrentTime=time.perf_counter()

	Key=pygame.key.get_pressed()
	Yes+=DT

	SpeedX+=(Key[pygame.K_RIGHT]-Key[pygame.K_LEFT])*DT
	SpeedY+=DT*10

	#Level._X=Level.ReturnResource(Level.SearchResource("Player"))._X-Level.ReturnResource(Level.SearchResource("Player"))._L
	#Level._Y=math.sin(Yes*10)*10

	Level._X-=DT*10

	if (Key[pygame.K_RIGHT]-Key[pygame.K_LEFT])<0:Level.ReturnResource(Level.SearchResource("Player")).ReturnResource(0).Flip(True)
	if (Key[pygame.K_RIGHT]-Key[pygame.K_LEFT])>0:Level.ReturnResource(Level.SearchResource("Player")).ReturnResource(0).Flip(False)
	Level.ReturnResource(1)._Y=(math.sin(Yes)*10)+125
	
	SpeedY,Grounded=Bugger.CollideDetector.CollisionCheckMoveY(Level.ReturnResource(Level.SearchResource("Player")),Level,SpeedY)
	SpeedX=Bugger.CollideDetector.CollisionCheckMoveX(Level.ReturnResource(Level.SearchResource("Player")),Level,SpeedX)
	
	if Grounded:
		if (Key[pygame.K_RIGHT]-Key[pygame.K_LEFT])!=0:
			Level.ReturnResource(Level.SearchResource("Player")).ReturnResource(0).Play(0,3,.1)
		else:Level.ReturnResource(Level.SearchResource("Player")).ReturnResource(0).Stop(0)
		SpeedY+=DT*100
		if Key[pygame.K_SPACE]:SpeedY=-DT*200
	
	else:
		if SpeedY<0:
			Level.ReturnResource(Level.SearchResource("Player")).ReturnResource(0).Stop(5)
		else:Level.ReturnResource(Level.SearchResource("Player")).ReturnResource(0).Stop(7)

	if (Key[pygame.K_RIGHT]-Key[pygame.K_LEFT])==0:
		if SpeedX>0:SpeedX-=DT*3
		if round(SpeedX,1)==0:SpeedX=0
		if SpeedX<0:SpeedX+=DT*3
	
	if SpeedX>=3:SpeedX=3
	if SpeedX<=-3:SpeedX=-3

	Manager.UpdateResource()

	for Event in pygame.event.get():
		if Event.type==pygame.QUIT:
			pygame.quit()
			sys.exit(0)