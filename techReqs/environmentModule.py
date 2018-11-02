# -*- coding: utf-8 -*-

import NXOpen
import NXOpen.BlockStyler
import NXOpen.UF
import NXOpen.Features
import subprocess
import re
import math
import collections
import itertools

class ColoredBlock:
	SnapPointTypesEnabled_UserDefined =	 1
	SnapPointTypesEnabled_Inferred =	 2
	SnapPointTypesEnabled_ScreenPosition =	 4
	SnapPointTypesEnabled_EndPoint =	 8
	SnapPointTypesEnabled_MidPoint =	16
	SnapPointTypesEnabled_ControlPoint =	32
	SnapPointTypesEnabled_Intersection =	64
	SnapPointTypesEnabled_ArcCenter =   128
	SnapPointTypesEnabled_QuadrantPoint =   256
	SnapPointTypesEnabled_ExistingPoint =   512
	SnapPointTypesEnabled_PointonCurve =  1024
	SnapPointTypesEnabled_PointonSurface =  2048
	SnapPointTypesEnabled_PointConstructor =  4096
	SnapPointTypesEnabled_TwocurveIntersection =  8192
	SnapPointTypesEnabled_TangentPoint = 16384
	SnapPointTypesEnabled_Poles = 32768

	SnapPointTypesOnByDefault_UserDefined =	 1
	SnapPointTypesOnByDefault_Inferred =	 2
	SnapPointTypesOnByDefault_ScreenPosition =	 4
	SnapPointTypesOnByDefault_EndPoint =	 8
	SnapPointTypesOnByDefault_MidPoint =	16
	SnapPointTypesOnByDefault_ControlPoint =	32
	SnapPointTypesOnByDefault_Intersection =	64
	SnapPointTypesOnByDefault_ArcCenter =   128
	SnapPointTypesOnByDefault_QuadrantPoint =   256
	SnapPointTypesOnByDefault_ExistingPoint =   512
	SnapPointTypesOnByDefault_PointonCurve =  1024
	SnapPointTypesOnByDefault_PointonSurface =  2048
	SnapPointTypesOnByDefault_PointConstructor =  4096
	SnapPointTypesOnByDefault_TwocurveIntersection =  8192
	SnapPointTypesOnByDefault_TangentPoint = 16384
	SnapPointTypesOnByDefault_Poles = 32768
	enum0 = NXOpen.BlockStyler.UIBlock

	def __init__(self):
		# class members
		self.group0 = None # Block type: Group
		self.blockHeight = None # Block type: Double
		self.blockWidth = None # Block type: Double
		self.blockLength = None # Block type: Double
		self.blockOrigin = None # Block type: Specify Point
		self.blockColor = None # Block type: Color Picker
		try:
			self.theSession = NXOpen.Session.GetSession()
			self.theUI = NXOpen.UI.GetUI()
			self.theUF = NXOpen.UF.UFSession.GetUFSession()
			self.workPart = self.theSession.Parts.Work
			#self.workDirectory = self.theSession.ExecutingJournal.replace(self.workFileName,'')
			self.theSessionPath = self.theSession.ExecutingJournal #путь до файла 
			self.workFileName = re.search(r'[a-zA-Zа-яА-Я]{1,}\.py',self.theSessionPath).group(0)
			self.theDialogPath =  self.theSessionPath.replace('.py','.dlx')
			self.theExecutablePath = '' #self.theSessionPath.replace('.py','.exe') придется писать хардвэй , иначе пока никак
			self.theDialog = self.theUI.CreateDialog(self.theDialogPath)
			self.theDialog.AddApplyHandler(self.apply_cb)
			self.theDialog.AddInitializeHandler(self.initialize_cb)
			self.theDialog.AddDialogShownHandler(self.dialogShown_cb)
			self.isDrafting = 'DRAFTING' in self.theSession.ApplicationName
			#self.isModeling = 'MODEL' in self.theSession.ApplicationName
			self.lw = self.theSession.ListingWindow
		except Exception as ex:
			raise ex

	def Show(self):
		try: self.theDialog.Show()
		except Exception as ex:
			self.theUI.NXMessageBox.Show('Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))

	def Dispose(self):
		if self.theDialog != None:
			self.theDialog.Dispose()
			self.theDialog = None

	def initialize_cb(self):
		try:
			self.group0 = self.theDialog.TopBlock.FindBlock('group0')
			self.blockHeight = self.theDialog.TopBlock.FindBlock('blockHeight')
			self.blockWidth = self.theDialog.TopBlock.FindBlock('blockWidth')
			self.blockLength = self.theDialog.TopBlock.FindBlock('blockLength')
			self.blockOrigin = self.theDialog.TopBlock.FindBlock('blockOrigin')
			self.blockColor = self.theDialog.TopBlock.FindBlock('blockColor')
			self.enum0 = self.theDialog.TopBlock.FindBlock('enum0')
		except Exception as ex:
			self.theUI.NXMessageBox.Show('Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))

	def dialogShown_cb(self):
		try: pass
		except Exception as ex:
			self.theUI.NXMessageBox.Show('Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))
	
	def apply_cb(self):
		errorCode = 0
		blockFeatureBuilder1 = None
		try:
			if self.enum0.GetProperties().GetEnum('Value') == 0:
				self.createTechRequirements(self)
			elif self.enum0.GetProperties().GetEnum('Value') == 1:
				self.rebuildTechRequirements(self)
			elif self.enum0.GetProperties().GetEnum('Value') == 2:
				self.editTechRequirements(self)
			elif self.enum0.GetProperties().GetEnum('Value') == 3:
				self.removeTechRequirements(self)
			else: pass
				
		except Exception as ex:
			errorCode = 1
			self.theUI.NXMessageBox.Show('Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))
		finally:
			if not blockFeatureBuilder1 == None:
				blockFeatureBuilder1.Destroy()
		return errorCode

	def scaleGrabber(self, parent): #debug function
		self.lw.Open()
		for view in self.workPart.ModelingViews:
			layout = self.workPart.Layouts.FindObject('L1') #слой вывода изображения???
			layout.ReplaceView(self.workPart.ModelingViews.WorkView, view, True)
			view.Fit()
			self.lw.WriteLine('%s -- %s' %(view.Name, view.Scale))

	def cycleObjects(self, parent, bodies = [], tmpBodyTag = 0):
		while True:
			tmpBodyTag = self.theUF.Obj.CycleObjsInPart(self.workPart.Tag, NXOpen.UF.UFConstants.UF_solid_type ,tmpBodyTag)
			if tmpBodyTag == 0: break 
			else:
				theType, theSubType = self.theUF.Obj.AskTypeAndSubtype(tmpBodyTag)
				if theSubType == NXOpen.UF.UFConstants.UF_solid_body_subtype:
					bodies.append(NXOpen.TaggedObjectManager.GetTaggedObject(tmpBodyTag))
		return bodies

	def calculateScalePoint(self, parent, view,text,scale = 1.000):
		self.lw.Open()
		bodies = self.cycleObjects(self)
		points = [theUF.ModlGeneral.AskBoundingBox(item.Tag) for item in bodies]
		x_points, y_points, z_points = [],[],[]
		[x_points.extend([bodyPoints[0],bodyPoints[3]]) for bodyPoints in points]
		[y_points.extend([bodyPoints[1],bodyPoints[4]]) for bodyPoints in points]
		[z_points.extend([bodyPoints[2],bodyPoints[5]]) for bodyPoints in points]
		x_max, y_max, z_max = max(x_points), max(y_points), max(z_points)
		x_min, y_min, z_min = min(x_points), min(y_points), min(z_points)
		line1 = self.workPart.Curves.CreateLine(NXOpen.Point3d(x_max,y_max,z_max),NXOpen.Point3d(x_min,y_min,z_min))
		line2 = self.workPart.Curves.CreateLine(NXOpen.Point3d(x_max,y_max,z_min),NXOpen.Point3d(x_min,y_min,z_max))
		pointIntersect = self.theUF.Curve.Intersect(line1.Tag, line2.Tag,[line1.StartPoint.X,line1.StartPoint.Y,line1.StartPoint.Z])
		#startPosition##########
		pointPlane = NXOpen.Point3d(x_max,y_max,pointIntersect.CurvePoint[2])
		pointText = NXOpen.Point3d(x_max,y_max,pointIntersect.CurvePoint[2])
		########################
		pmiNoteBuilder = self.workPart.Annotations.CreatePmiNoteBuilder(NXOpen.Annotations.SimpleDraftingAid.Null)
		pmiNoteBuilder.Origin.Plane.PlaneMethod = NXOpen.Annotations.PlaneBuilder.PlaneMethodType.ModelView
		pmiNoteBuilder.Origin.Origin.SetValue(NXOpen.TaggedObject.Null, NXOpen.View.Null, pointText)
		pmiNoteBuilder.Origin.Anchor = NXOpen.Annotations.OriginBuilder.AlignmentPosition.MidLeft
		pmiNoteBuilder.Style.LetteringStyle.GeneralTextSize = 5.0
		pmiNoteBuilder.Style.LetteringStyle.GeneralTextFont = self.workPart.Fonts.AddFont("cyrillic", NXOpen.FontCollection.Type.Nx)
		pmiNoteBuilder.Style.LetteringStyle.GeneralTextColor = self.workPart.Colors.Find('Yellow')
		pmiNoteBuilder.Text.TextBlock.SetText(text)
		PMIObject = pmiNoteBuilder.Commit()
		plane = PMIObject.AnnotationPlane
		plane.SetOrigin(pointPlane)
		cd = self.workPart.Annotations.CreateComponentData(PMIObject)
		scale = (z_max - z_min)/(cd.GetTextComponents()[0]).Height
		self.theSession.UpdateManager.AddToDeleteList([line1,line2])
		pmiNoteBuilder.Text.TextBlock.SetText(['<C%s>'%(scale)]+text+['<C>'])
		pmiNoteBuilder.ShowResults()
		pmiNoteBuilder.Commit()
		pmiNoteBuilder.Destroy()
		return PMIObject

	def createTechRequirements(self, parent):
		#try:	
		ctr_subprocess = subprocess.Popen([self.theExecutablePath], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		text = ctr_subprocess.communicate()[0]
		text = text.decode('utf-8')
		if self.isDrafting:
			pass
			#scale = 1.000
			#for index, part in enumerate(parts):
			#draftingNoteBuilder = self.workPart.Annotations.CreateDraftingNoteBuilder(NXOpen.Annotations.SimpleDraftingAid.Null)
			#text = ['<C%s>%s<C>'%(scale,item) for item in part]
			#draftingNoteBuilder.Text.TextBlock.SetText(text)
			#s = child.stdout.readline().decode('cp866')
			#except Exception as ex:
			#	self.lw.Open()
			#	self.lw.WriteLine(str(ex))	
		else:
			try: #проверяем наличие вида, если отсутствует - создаем
				layout = self.workPart.Layouts.FindObject('L1')
				modelingView = self.workPart.ModelingViews.FindObject('ИЗОМЕТРИЧЕСКИЙ')
				layout.ReplaceView(self.workPart.ModelingViews.WorkView, modelingView, True)
			except:
				layout = self.workPart.Layouts.FindObject('L1')
				modelingView = self.workPart.ModelingViews.FindObject('Isometric')
				layout.ReplaceView(self.workPart.ModelingViews.WorkView, modelingView, True)
				modelingView = self.workPart.Views.SaveAsPreservingCase(modelingView, 'ИЗОМЕТРИЧЕСКИЙ', True, False)
				layout.ReplaceView(self.workPart.ModelingViews.WorkView, modelingView, True)
			#for index, part in enumerate(parts):
			text = text.split('\r\n')
			PMIObject = self.calculateScalePoint(self, modelingView, text)
			objectGeneralPropertiesBuilder = self.workPart.PropertiesManager.CreateObjectGeneralPropertiesBuilder([PMIObject])
			objectGeneralPropertiesBuilder.Name = 'ТЕХНИЧЕСКИЕ_ТРЕБОВАНИЯ' #'ТЕХНИЧЕСКИЕ_ТРЕБОВАНИЯ_%i' %index
			objectGeneralPropertiesBuilder.Commit()
			objectGeneralPropertiesBuilder.Destroy()
			displayModification = self.theSession.DisplayManager.NewDisplayModification()
			displayModification.NewLayer = 9
			displayModification.Apply([PMIObject])
			displayModification.Dispose()
			modelingView.Fit()
		pass
	
	def editTechRequirements(self, parent):
		self.theUI.NXMessageBox.Show('__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'В разработке.')
		pass

	def rebuildTechRequirements(self, parent):
		try: #проверяем наличие вида, если отсутствует - выдаем алерт
			layout = self.workPart.Layouts.FindObject('L1')
			modelingView = self.workPart.ModelingViews.FindObject('ИЗОМЕТРИЧЕСКИЙ')
			layout.ReplaceView(self.workPart.ModelingViews.WorkView, modelingView, True)
		except Exception as ex:
			self.theUI.NXMessageBox.Show('__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'Вид отсутствует')
		pass

	def removeTechRequirements(self, parent):
		self.theUI.NXMessageBox.Show('__alarm__template__', NXOpen.NXMessageBox.DialogType.Warning, 'В разработке.')
		pass	

def main():
	try:
		theColoredBlock = ColoredBlock()
		theColoredBlock.Show()
	except Exception as ex:
		NXOpen.UI.GetUI().NXMessageBox.Show('Block Styler', NXOpen.NXMessageBox.DialogType.Error, str(ex))
	finally:
		theColoredBlock.Dispose()

if __name__ == '__main__':
	main()

'''
'See the APPLICATION_BUTTON's defined in the ug_main.men file
        'UG_APP_GATEWAY
        'UG_APP_MODELING
        'UG_APP_STUDIO
        'UG_APP_DRAFTING
        'UG_APP_MANUFACTURING
        'UG_APP_SFEM
        'UG_APP_DESFEM
        'UG_APP_MECHANISMS
        'UG_APP_MECHATRONICS
        'UG_APP_SHEETMETAL
        'UG_APP_PCB_DESIGN
        'UG_APP_ROUTING
        'etc.
'''
