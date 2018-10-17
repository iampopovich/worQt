# -*- coding: utf-8 -*-
import NXOpen
import NXOpen.BlockStyler
import subprocess
import re
import codecs
import os
import ctypes

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
			self.isDrawing = 'DRAFTING' in self.theSession.ApplicationName
			self.isModeling = 'MODEL' in self.theSession.ApplicationName
			self.lw = self.theSession.ListingWindow
		except Exception as ex:
			raise ex

	def Show(self):
		try: self.theDialog.Show()
		except Exception as ex:
			self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))

	def Dispose(self):
		if self.theDialog != None:
			self.theDialog.Dispose()
			self.theDialog = None

	def initialize_cb(self):
		try:
			self.group0 = self.theDialog.TopBlock.FindBlock("group0")
			self.blockHeight = self.theDialog.TopBlock.FindBlock("blockHeight")
			self.blockWidth = self.theDialog.TopBlock.FindBlock("blockWidth")
			self.blockLength = self.theDialog.TopBlock.FindBlock("blockLength")
			self.blockOrigin = self.theDialog.TopBlock.FindBlock("blockOrigin")
			self.blockColor = self.theDialog.TopBlock.FindBlock("blockColor")
			self.enum0 = self.theDialog.TopBlock.FindBlock("enum0")
		except Exception as ex:
			self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))

	def dialogShown_cb(self):
		try: pass
		except Exception as ex:
			self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
	
	def apply_cb(self):
		errorCode = 0
		blockFeatureBuilder1 = None
		try:
			if self.enum0.GetProperties().GetEnum("Value") == 0:
				self.createTechRequirements(self)
			elif self.enum0.GetProperties().GetEnum("Value") == 1:
				self.rebuildTechRequirements(self)
			elif self.enum0.GetProperties().GetEnum("Value") == 2:
				self.removeTechRequirements(self)
			else: pass
				
		except Exception as ex:
			errorCode = 1
			self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
		finally:
			if not blockFeatureBuilder1 == None:
				blockFeatureBuilder1.Destroy()
		return errorCode
	
	def createTechRequirements(self, parent):
		try:
			ctr_subprocess = subprocess.Popen([self.theExecutablePath], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			text = ctr_subprocess.communicate()[0]
			text = text.decode('utf-8')
			self.lw.Open()
			self.lw.WriteLine(str(text))
			#if self.isDrawing: создаем один контейнер ТТ
			#if self.isModeling: создаем другой контейнер ТТ
				#specificNoteBuilder = self.workPart.PmiManager.PmiAttributes.CreateSpecificNoteBuilder(NXOpen.Annotations.SpecificNote.Null)
				#specificNoteBuilder.Origin.Anchor = NXOpen.Annotations.OriginBuilder.AlignmentPosition.MidCenter
				#specificNoteBuilder.Origin.SetInferRelativeToGeometry(True)
				#specificNoteBuilder.Origin.Plane.PlaneMethod = NXOpen.Annotations.PlaneBuilder.PlaneMethodType.ModelView
				#specificNoteBuilder.SetText([text])
				#specificNoteBuilder.Commit()
				#specificNoteBuilder.Destroy()
			#s = child.stdout.readline().decode('cp866')
		except Exception as ex:
			self.lw.Open()
			self.lw.WriteLine(str(ex))		
		pass
	
	def rebuildTechRequirements(self, parent):
		self.theUI.NXMessageBox.Show("__alarm__template__", NXOpen.NXMessageBox.DialogType.Warning, "В разработке.")
		pass

	def removeTechRequirements(self, parent):
		self.theUI.NXMessageBox.Show("__alarm__template__", NXOpen.NXMessageBox.DialogType.Warning, "В разработке.")
		pass	

def main():
	try:
		theColoredBlock = ColoredBlock()
		theColoredBlock.Show()
	except Exception as ex:
		NXOpen.UI.GetUI().NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
	finally:
		theColoredBlock.Dispose()

if __name__ == "__main__":
	main()


