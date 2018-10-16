import NXOpen
import NXOpen.BlockStyler
import subprocess
import re

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
		#self.theSession = None
		#self.theUI = None
		#self.theDialogName = ''
		#self.theDialog = None
		self.group0 = None # Block type: Group
		self.blockHeight = None # Block type: Double
		self.blockWidth = None # Block type: Double
		self.blockLength = None # Block type: Double
		self.blockOrigin = None # Block type: Specify Point
		self.blockColor = None # Block type: Color Picker
		try:
			self.theSession = NXOpen.Session.GetSession()
			self.theUI = NXOpen.UI.GetUI()
			self.workFileName = re.search(r'[a-zA-Zа-яА-Я]{1,}\.py',self.theSession.ExecutingJournal).group(0)
			self.workDirectory = self.theSession.ExecutingJournal.replace(self.workFileName,'')
			self.theSessionName = self.theSession.ExecutingJournal #путь до файла 
			self.theDialogName =  self.theSessionName.replace('.py','.dlx') 
			self.theDialog = self.theUI.CreateDialog(self.theDialogName)
			self.theDialog.AddApplyHandler(self.apply_cb)
			self.theDialog.AddInitializeHandler(self.initialize_cb)
			self.theDialog.AddDialogShownHandler(self.dialogShown_cb)
			self.isDrawing = 'DRAFTING' in self.theSession.ApplicationName
			self.isModeling = 'MODEL' in self.theSession.ApplicationName
		except Exception as ex:
			lw = self.theSession.ListingWindow
			lw.Open()
			lw.WriteLine(self.workDirectory)
			lw.WriteLine(str(self.theSessionName))
			lw.WriteLine(str(self.theDialogName))
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
		lw = self.theSession.ListingWindow
		errorCode = 0
		blockFeatureBuilder1 = None

		try:
			if self.enum0.GetProperties().GetEnum("Value") == 0:
				self.createTechRequirements(self)
			elif self.enum0.GetProperties().GetEnum("Value") == 1:
				self.rebuildTechRequirements(self)
			elif self.enum0.GetProperties().GetEnum("Value") == 2:
				self.removeTechRequirements(self)
			else:
				pass
				
		except Exception as ex:
			errorCode = 1
			self.theUI.NXMessageBox.Show("Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
		finally:
			if not blockFeatureBuilder1 == None:
				blockFeatureBuilder1.Destroy()
		return errorCode
	
	def createTechRequirements(self, parent):
		#ctr_subprocess = subprocess.Popen()
		#if self.isDrawing:
		#if self.isModeling:
		pass	
	
	def rebuildTechRequirements(self, parent):
		self.theUI.NXMessageBox.Show("__alarm__template__", NXOpen.NXMessageBox.DialogType.Warning, "В разработке.")
		pass

	def removeTechRequirements(self, parent):
		self.theUI.NXMessageBox.Show("__alarm__template__", NXOpen.NXMessageBox.DialogType.Warning, "В разработке.")
		pass	
###		
#def updateSwitcher():
#	if :
#		try:
#			for sheet in theSession.Parts.Work.DrawingSheets:
#				for tempView in sheet.GetDraftingViews():
#					try:
#						views = [NXOpen.View.Null] * 1 
#						views[0] = tempView
#						editViewSettingsBuilder = workPart.SettingsManager.CreateDrawingEditViewSettingsBuilder(views)
#						editsettingsbuilders = [NXOpen.Drafting.BaseEditSettingsBuilder.Null] * 1 
#						editsettingsbuilders[0] = editViewSettingsBuilder
#						workPart.SettingsManager.ProcessForMultipleObjectsSettings(editsettingsbuilders)
#					except:
#						theUI.NXMessageBox.Show("Alarm", NXOpen.NXMessageBox.DialogType.Warning, "Ошибка в обходе видов.") #debug info
#					
#					editViewSettingsBuilder.ViewStyle.ViewStyleGeneral.AutomaticUpdate = switchMode#False
#					editViewSettingsBuilder.Commit()				
#					editViewSettingsBuilder.Destroy()
#			theUI.NXMessageBox.Show("Автоматическое обновление видов", NXOpen.NXMessageBox.DialogType.Information, "Автоматическое обновление видов %s." %resUpdate)
#		except:
#			theUI.NXMessageBox.Show("Alarm", NXOpen.NXMessageBox.DialogType.Warning, "Видов с чертежами не найдено.")
#	elif  in theSession.ApplicationName:
#		theUI.NXMessageBox.Show("Alarm", NXOpen.NXMessageBox.DialogType.Warning, "Вы в режиме моделирования.")
#	else:
#		theUI.NXMessageBox.Show("Alarm", NXOpen.NXMessageBox.DialogType.Warning, "Переключитесь в режим черчения.")
###

def main():
	try:
		theColoredBlock = ColoredBlock()
		theColoredBlock.Show()
	except Exception as ex:
		NXOpen.UI.GetUI().NXMessageBox.Show(
			"Block Styler", NXOpen.NXMessageBox.DialogType.Error, str(ex))
	finally:
		theColoredBlock.Dispose()

if __name__ == "__main__":
	main()
