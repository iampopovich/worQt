#!/usr/bin/pythom
#-*-coding: utf-8-*-
#import math
import openpyxl
import time as tt
import datetime as dt
import re
import os
#from os import path
import sys
import lib_headers as hh
'''
def findFiles(cwd):
def createJournal(cwd):
def compileFile(jList,config,journal,cwd):
def readWriteConfig(conf,mode,dict = None):
'''
def whatOSRun(path):
	if os.name.endswith('nt'):
		return '%s\\' %path
	else: return '%s/' %path

def findFiles(cwd):
	currentYear = dt.datetime.now().year
	files = [os.path.join(cwd, f) for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
	try:	#этих файлов может и не быть , на всякий случай расставь экспы
		cJournalName = '%sСводный_журнал_ДТЭ_%s.xlsx' %(cwd,currentYear)
		if cJournalName in files: files.pop(files.index(cJournalName))
		else: createJournal(cJournalName)
		xlFiles = [item for item in files if not(re.search(r'.*\sДТЭ\s.*%s.*xlsm' %currentYear, item) is None)]
		return xlFiles,cJournalName
	except Exception as ex:
		print('findFiles failed with: %s' %ex)
		return None, None

def createJournal(name):
	try:
		wb = openpyxl.Workbook()
		wb.remove(wb.active)
		for sheetName in ['ДД','ДТЭ']:
			wb.create_sheet(sheetName)
			activeSheet = wb[sheetName]
			activeSheet.append(hh.getHeaders(sheetName))
			#activeSheet.auto_filter.ref = 
			for cell in list(activeSheet.rows)[0]:
				if sheetName == 'ДД':
					cell.style = 'Input'
					border = openpyxl.styles.Border(left=openpyxl.styles.Side(style='thin'),
                     						right=openpyxl.styles.Side(style='thin'),
                     						top=openpyxl.styles.Side(style='thin'),
                     						bottom=openpyxl.styles.Side(style='thin'))
					cell.border = border
				else:
					cell.style = 'Accent5'
					border = openpyxl.styles.Border(left=openpyxl.styles.Side(style='thin'),
                     						right=openpyxl.styles.Side(style='thin'),
                     						top=openpyxl.styles.Side(style='thin'),
                     						bottom=openpyxl.styles.Side(style='thin'))
					cell.border = border
		wb.save('%s' %(name))
		return None
	except Exception as ex:
		return ('createJournal failed with: %s' %ex)
	
def clearJournal(journal):
	wbToCopy = openpyxl.load_workbook(journal)
	for sheet in wbToCopy.sheetnames:
		cSheet = wbToCopy[sheet]
		for row in cSheet.iter_rows(min_row = 2): #check specs for iter_rows
			for cell in row:
				cell.value = None
	wbToCopy.save(journal)

def compileFile(jList,journal): #by cells
	try:
		wbToCopy = openpyxl.load_workbook(journal)
	except Exception as ex:
		return 'CompileJournal failed with %s' %ex
	tempLastRow = {'ДД':2,'ДТЭ':2} 
	for jItem in jList: 
		wbFromCopy = openpyxl.load_workbook(jItem,read_only=True)
		for sheetFromCopy in wbFromCopy.sheetnames:
			try:
				subname = sheetFromCopy.split('_')[0]
				sheetToCopy = wbToCopy[subname] #copy cells to the same sheet in new workbook
				sheet = wbFromCopy[sheetFromCopy]
			except:	continue
			for row in sheet.iter_rows(min_row = 2):
				isEmptyRow = True
				lastRow = tempLastRow[subname]
				for iCell,cell in enumerate(row):
					if (cell.value is None):
						newCell = sheetToCopy.cell(row = lastRow,column = iCell+1, value = ' ')
						newCell.style = 'Good'
						border = openpyxl.styles.Border(left=openpyxl.styles.Side(style='thin'),
                     						right=openpyxl.styles.Side(style='thin'),
                     						top=openpyxl.styles.Side(style='thin'),
                     						bottom=openpyxl.styles.Side(style='thin'))
						newCell.border = border
						#newCell.border = cell.border
						#bgCLR = openpyxl.styles.colors.Color(rgb='00c6efce')
						#newCell.fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=bgCLR)
					else:
						isEmptyRow = False 
						newCell = sheetToCopy.cell(row = lastRow,column = cell.column, value = cell.value)
						newCell.font = cell.font
						newCell.border = cell.border
						newCell.fill = cell.fill
						newCell.number_format = cell.number_format
						newCell.alignment = cell.alignment
				if isEmptyRow:	continue
				else: tempLastRow[subname]+=1
		wbFromCopy.close()
		del wbFromCopy, sheetFromCopy 
		wbToCopy.save(journal)
	wbToCopy.close()
	return None # ¯\_(ツ)_/¯
	
def main():
	tStart = dt.datetime.now()#.hour
	workDir = whatOSRun(os.getcwd()) #определяем параметры ввода пути до файла
	stopSwitch = False
	journalList,journalFile = findFiles(workDir)
	while not(stopSwitch):
		print('start')
		#clearJournal(journalFile)
		compileFile(journalList,journalFile)
		print('waiting for 10 seconds')
		print(dt.datetime.now() - tStart)
		sys.exit(0) # пока выходит после сборки 
		#wait for 15 minutes and repeat cycle
		#stopSwitch = ((dt.datetime.now().hour - tStart) > 9)

	sys.exit(0)
	
if __name__ == '__main__':
	main()
