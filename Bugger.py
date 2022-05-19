import pygame
import copy
import time

class ScenarioManagement():
	def __init__(self,Format,Length,Breath):
		#Filter Input
		self._FORMAT=str(Format)
		self._LENGTH=int(Length)
		self._BREATH=int(Breath)

		self._Resource=None
		#Create Window And Caption
		pygame.display.set_caption(self._FORMAT)
		self._WINDOW=pygame.display.set_mode((self._LENGTH,self._BREATH),pygame.SCALED|pygame.FULLSCREEN,vsync=1)

	def ChangeResource(self,Resource):
		self._Resource=Resource
		self._Resource._ChangeCreator(self._WINDOW)

	def UpdateResource(self):
		self._Resource._Update()
		pygame.display.flip()
		self._WINDOW.fill((0,100,100))
		
	def ReturnFormat(self):return self._FORMAT
	def ReturnLength(self):return self._LENGTH
	def ReturnBreath(self):return self._BREATH



class ResourceManagement:
	def __init__(self,Name,X,Y,L,B):
		self._X=X
		self._Y=Y
		self._L=L
		self._B=B

		self._Name=Name

		self._InstanceCreator=None
		self._Creator=None
		self._Parent=None
		self._Resource=[]

		print(Name+" Resource Successfully Created!")

	def ReturnResource(self,Index):
		return self._Resource[Index]

	def SearchResource(self,Name):
		for Resource in range(len(self._Resource)):
				if self._Resource[Resource]._Name==Name:
					return Resource
	
	def DeleteResource(self,Index):
		self._Resource.pop(Index)
	
	#Insert Child Resource
	def InsertResource(self,Resource):
		self._Resource.append(copy.copy(Resource))

		self._Resource[-1]._Parent=self
		self._Resource[-1]._Creator=self._Creator

		Resource=None
	
	def _ChangeCreator(self,Creator):
		self._Creator=Creator

		for Resource in range(len(self._Resource)):
			self._Resource[Resource]._ChangeCreator(Creator)
	
	def _GetParent(self):
		return self._Parent

	def _GetGlobalX(self):
		self._TemporaryFinalX=copy.copy(self._X)
		self._TemporaryFinalY=copy.copy(self._Y)
		self._TemporaryParent=self._GetParent()

		#Accumulate All Parent X And Y Offsets
		if self._TemporaryParent:
			self._TemporaryFinalX+=self._TemporaryParent._X

			while True:
				self._TemporaryParent=copy.copy(self._TemporaryParent._GetParent())
				if self._TemporaryParent:
					self._TemporaryFinalX+=self._TemporaryParent._X

				else:break
		
		return self._TemporaryFinalX
	
	def _GetGlobalY(self):
		self._TemporaryFinalY=copy.copy(self._Y)
		self._TemporaryParent=self._GetParent()

		#Accumulate All Parent X And Y Offsets
		if self._TemporaryParent:

			self._TemporaryFinalY+=self._TemporaryParent._Y
			while True:
				self._TemporaryParent=copy.copy(self._TemporaryParent._GetParent())
				if self._TemporaryParent:

					self._TemporaryFinalY+=self._TemporaryParent._Y
				else:break
		
		return self._TemporaryFinalY

	#Update Child Resource
	def _Update(self):
		for Resource in range(len(self._Resource)):
			self._Resource[Resource]._Update()
	
	#Render Child Resource
	def _Render(self):
		for Resource in range(len(self._Resource)):
			self._Resource[Resource]._Render()

class GraphicResource(ResourceManagement):
	def __init__(self,Name,File,XOffset,YOffset,AmountX,AmountY):
		self._SURFACE=File
		self._SUBSURFACE=self._SURFACE.subsurface(0,0,32,32)
		self._Play=False
		self._Start=0
		self._End=0
		

		self._OffsetX=0
		self._Speed=0

		self._Flip=False

		self._AnimationOffset=pygame.rect.Rect(0,0,self._SURFACE.get_width()/AmountX,self._SURFACE.get_height()/AmountY)

		super().__init__(Name,XOffset,YOffset,self._SURFACE.get_width()/AmountX,self._SURFACE.get_height()/AmountY)

		self._Time=time.time()
		#print(self._Parent._X)
		
	
	@staticmethod
	def LoadImage(File):
		Image=pygame.image.load(File)
		if Image:
			print(File+" Image Successfully Loaded!")
			return Image
		
	def Play(self,Start,End,Speed):
		self._Play=True
		self._Start=Start
		self._End=End
		self._Speed=Speed
	
	def Stop(self,Start):
		self._Play=False
		self._OffsetX=Start*self._L
	
	def Flip(self,FlipMode):
		if self._Flip!=FlipMode:
			#self._SUBSURFACE=pygame.transform.flip(self._SUBSURFACE,True,False)
			self._Flip=FlipMode



	def _Update(self):
		self._TimerCheck=time.time()-self._Time


		#TODO: Rewrite Sprite Animation System To Be More Flexible
		if self._TimerCheck>=self._Speed:
			self._Time=time.time()
			if self._Play:

				self._OffsetX+=self._L

				if self._OffsetX>self._End*self._L:self._OffsetX=0
				if self._OffsetX==0:self._OffsetX=self._Start*self._L
		
		self._AnimationOffset.x=self._OffsetX
		self._SUBSURFACE=self._SURFACE.subsurface(self._AnimationOffset)

		self._SUBSURFACE=pygame.transform.flip(self._SUBSURFACE,self._Flip,False)
		
		self._Creator.blit(self._SUBSURFACE,(self._GetGlobalX(),self._GetGlobalY()))

		super()._Update()


class TilemapResource(ResourceManagement):
	def __init__(self,Name,File,X,Y,AmountX,AmountY,Data,DataAmountX,DataAmountY):
		self._SURFACE=File
		self._AMOUNTX=int(AmountX)
		self._AMOUNTY=int(AmountY)

		self._DATA=Data
		self._DATAAMOUNTX=DataAmountX
		self._DATAAMOUNTY=DataAmountY

		self._OFFSETX=0
		self._OFFSETY=0

		self._SourceX=0
		self._SourceY=0

		super().__init__(Name,X,Y,self._SURFACE.get_width()/self._AMOUNTX,self._SURFACE.get_height()/self._AMOUNTY)
	
	def _Update(self):
		self._OFFSETX=0
		self._OFFSETY=0

		self._SourceX=0
		self._SourceY=0

		for Tilemap in range(len(self._DATA)):
			
			if self._OFFSETX==self._L*self._DATAAMOUNTX:
				self._OFFSETY+=self._B
				self._OFFSETX=0
			
			if self._DATA[Tilemap]!=0:
				self._SourceX=(self._DATA[Tilemap]-1)*self._L
				while self._SourceX>self._SURFACE.get_width():
					self._SourceX-=self._SURFACE.get_width()
					self._SourceY+=self._B
				self._Creator.blit(self._SURFACE,(self._OFFSETX+self._GetGlobalX(),self._OFFSETY+self._GetGlobalY()),pygame.rect.Rect(self._SourceX,self._SourceY,self._L,self._B))
				self._SourceX=0
				self._SourceY=0
			self._OFFSETX+=self._L

		self._OFFSETX=0
		self._OFFSETY=0
		self._SourceX=0
		self._SourceY=0
		

class LayeredResource(ResourceManagement):pass

class CollideDetector():

	@staticmethod
	def CollisionCheckMoveY(Resource,TilemapResources,MoveY):
		Resource._Y+=MoveY
		Grounded=False

		for LoopResourceList in range(len(TilemapResources._Resource)):
			TemporaryResource=TilemapResources.ReturnResource(LoopResourceList)
			if type(TemporaryResource)is TilemapResource and TemporaryResource!=Resource:
				TemporaryResource._OFFSETX=0
				TemporaryResource._OFFSETY=0

				for Tilemap in range(len(TemporaryResource._DATA)):
			
					if TemporaryResource._OFFSETX==TemporaryResource._L*TemporaryResource._DATAAMOUNTX:
						TemporaryResource._OFFSETY+=TemporaryResource._B
						TemporaryResource._OFFSETX=0
			
					if TemporaryResource._DATA[Tilemap]!=0 and TemporaryResource._DATA[Tilemap]<=50:
						if pygame.rect.Rect(Resource._X,Resource._Y,Resource._L,Resource._B).colliderect(pygame.rect.Rect(TemporaryResource._OFFSETX+TemporaryResource._X,TemporaryResource._OFFSETY+TemporaryResource._Y,TemporaryResource._L,TemporaryResource._B)):
							#If It Collides, Teleport Next To The Collided And Stop Momentum
							if Resource._Y>=TemporaryResource._OFFSETY+TemporaryResource._Y:
								Resource._Y=TemporaryResource._OFFSETY+TemporaryResource._Y+TemporaryResource._B
							else:
								Resource._Y=TemporaryResource._OFFSETY+TemporaryResource._Y-Resource._B
								Grounded=True
						
							MoveY=0
							TemporaryResource._OFFSETX+=TemporaryResource._L
							TemporaryResource._OFFSETX=0
							TemporaryResource._OFFSETY=0
							return MoveY,Grounded
					
					TemporaryResource._OFFSETX+=TemporaryResource._L

				TemporaryResource._OFFSETX=0
				TemporaryResource._OFFSETY=0

			
			
			if type(TemporaryResource)is ResourceManagement and TemporaryResource!=Resource:
				if pygame.rect.Rect(Resource._X,Resource._Y,Resource._L,Resource._B).colliderect(pygame.rect.Rect(TemporaryResource._X,TemporaryResource._Y,TemporaryResource._L,TemporaryResource._B)):
						#If It Collides, Teleport Next To The Collided And Stop Momentum
						if Resource._Y>=TemporaryResource._Y:
							Resource._Y=TemporaryResource._Y+TemporaryResource._B
						else:
							Resource._Y=TemporaryResource._Y-Resource._B
							Grounded=True
						
						MoveY=0
						return MoveY,Grounded

		return MoveY,Grounded		

	@staticmethod
	def CollisionCheckMoveX(Resource,TilemapResources,MoveX):
		Resource._X+=MoveX

		for LoopResourceList in range(len(TilemapResources._Resource)):
			TemporaryResource=TilemapResources.ReturnResource(LoopResourceList)
			if type(TemporaryResource)is TilemapResource and TemporaryResource!=Resource:
				TemporaryResource._OFFSETX=0
				TemporaryResource._OFFSETY=0

				for Tilemap in range(len(TemporaryResource._DATA)):
			
					if TemporaryResource._OFFSETX==TemporaryResource._L*TemporaryResource._DATAAMOUNTX:
						TemporaryResource._OFFSETY+=TemporaryResource._B
						TemporaryResource._OFFSETX=0
			
					if TemporaryResource._DATA[Tilemap]!=0 and TemporaryResource._DATA[Tilemap]<=50:
						if pygame.rect.Rect(Resource._X,Resource._Y,Resource._L,Resource._B).colliderect(pygame.rect.Rect(TemporaryResource._OFFSETX+TemporaryResource._X,TemporaryResource._OFFSETY+TemporaryResource._Y,TemporaryResource._L,TemporaryResource._B)):
							#If It Collides, Teleport Next To The Collided And Stop Momentum
							if Resource._X>=TemporaryResource._OFFSETX+TemporaryResource._X:
								Resource._X=TemporaryResource._OFFSETX+TemporaryResource._X+TemporaryResource._L
							else:
								Resource._X=TemporaryResource._OFFSETX+TemporaryResource._X-Resource._L
						
							MoveX=0
							TemporaryResource._OFFSETX+=TemporaryResource._L
							TemporaryResource._OFFSETX=0
							TemporaryResource._OFFSETY=0
							return MoveX
					
					TemporaryResource._OFFSETX+=TemporaryResource._L

				TemporaryResource._OFFSETX=0
				TemporaryResource._OFFSETY=0
			
			if type(TemporaryResource)is ResourceManagement and TemporaryResource!=Resource:
				if pygame.rect.Rect(Resource._X,Resource._Y,Resource._L,Resource._B).colliderect(pygame.rect.Rect(TemporaryResource._X,TemporaryResource._Y,TemporaryResource._L,TemporaryResource._B)):
						#If It Collides, Teleport Next To The Collided And Stop Momentum
						if Resource._X>=TemporaryResource._X:
							Resource._X=TemporaryResource._X+TemporaryResource._L
						else:
							Resource._X=TemporaryResource._X-Resource._L
							Grounded=True
						
						MoveX=0
						return MoveX

		return MoveX
				


class ParticleGeneraor():pass

class MusicHandler():pass
class InputHandler():pass









