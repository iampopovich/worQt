#!/usr/bin/pythom
#-*-coding: utf-8-*-
import math
import openpyxl
import time as tt
import datetime as dt
import re
import os
from os import path
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
	else:
		return '%s/' %path

def findFiles(cwd):
	currentYear = dt.datetime.now().year
	files = [path.join(cwd, f) for f in os.listdir(cwd) if path.isfile(path.join(cwd, f))] #сеим директории, оставляем файлы
	try:	#этих файлов может и не быть , на всякий случай расставь экспы
		cJournalName = '%sСводный_журнал_ДТЭ_%s.xlsm' %(cwd,currentYear)
		xlFiles = [item for item in files if '.xlsm' in item]
		if cJournalName in xlFiles:
			xlFiles.pop(xlFiles.index(cJournalName))
		else:
			createJournal(cJournalName)
		for xlItem in xlFiles:
			if re.search(r'.*\sДТЭ\s.*%s.*xlsm' %currentYear, xlItem) is None:
				xlFiles.pop(xlFiles.index(xlItem))	
		return xlFiles,cJournalName
	except Exception as ex:
		print('findFiles failed with: %s' %ex)

def createJournal(name):
	wb = openpyxl.Workbook()
	wb.remove(wb.active)
	for sheetName in ['ДД','ДТЭ']:
		wb.create_sheet(sheetName)
		activeSheet = wb[sheetName]
		activeSheet.append(hh.getHeaders(sheetName))
	wb.save('%s' %(name))
	return None
	
def clearJournal(journal):
	wbToCopy = openpyxl.load_workbook(journal)
	for sheet in wbToCopy.sheetnames:
		cSheet = wbToCopy[sheet]
		for row in cSheet.iter_rows(min_row = 2): #check specs for iter_rows
			for cell in row:
				cell.value = None
	wbToCopy.save(journal)

def compileFile(jList,journal): #by cells
	wbToCopy = openpyxl.load_workbook(journal)
	tempLastRow = {'ДД':2,'ДТЭ':2} 
	for jItem in jList: 
		wbFromCopy = openpyxl.load_workbook(jItem,read_only=True)
		for sheetFromCopy in wbFromCopy.sheetnames:
			sheetToCopy = wbToCopy[sheetFromCopy.split('_')[0]] #copy cells to the same sheet in new workbook
			sheet = wbFromCopy[sheetFromCopy]
			for row in sheet.iter_rows(min_row = 2):
				lastRow = tempLastRow[sheetFromCopy.split('_')[0]]
				for cell in row:
					if cell.value is None:
						pass
					else:
						newCell = sheetToCopy.cell(row = lastRow,column = cell.column, value = cell.value)
						newCell.font = cell.font
						newCell.border = cell.border
						newCell.fill = cell.fill
						newCell.number_format = cell.number_format
						newCell.protection = cell.protection
						newCell.alignment = cell.alignment
				tempLastRow[sheetFromCopy.split('_')[0]]+=1 #sheetFromCopy.split('_')[0] - заменить на переменную мб?
		wbFromCopy.close()
		wbToCopy.save(journal)

	wbToCopy.close()
	return None # ¯\_(ツ)_/¯
	
def main():
	tStart = dt.datetime.now().hour
	workDir = whatOSRun(os.getcwd()) #определяем параметры ввода пути до файла
	stopSwitch = False
	journalList,journalFile = findFiles(workDir)
	while not(stopSwitch):
		print('start')
		clearJournal(journalFile)
		compileFile(journalList,journalFile)
		print('waiting for 10 seconds')
		tt.sleep(10)
		#wait for 15 minutes and repeat cycle
		#stopSwitch = ((dt.datetime.now().hour - tStart) > 9)
	sys.exit(0)
	
if __name__ == '__main__':
	main()
