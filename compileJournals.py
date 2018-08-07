#!/usr/bin/pythom
#-*-coding: utf-8-*-
import math
import openpyxl
import time as tt
import datetime as dt
import re
import os
import sys
import lib_headers as hh
'''
def findFiles(cwd):
def createJournal(cwd):
def compileFile(jList,config,journal,cwd):
def readWriteConfig(conf,mode,dict = None):
'''

def findFiles(cwd):
	currentYear = dt.datetime.date.now().year
	xlFiles = [f for f in os.listdir(cwd) if isfile(os.join(cwd, f))]
	xlFiles = [lambda x: re.search(r'.*DTE.*%s.*xlsm' %currentYear, xlFiles).group(0)]
	for xlItem in xlFiles:
		if re.search(r'.*svodniy_jurnal_DTE.*%s.*xlsm' %currentYear, xlItem) == None:
			createJournal(cwd)
		else:
			cJournal = xlItem
			xlFiles.pop(xlFiles.index(xlItem))
	for file in os.listdir(cwd):
		if file.endswith("config.txt"):
			config = os.join(cwd,file)
	return xlFiles,config,cJournal

def createJournal(cwd):
	wb = openpyxl.Workbook()
	for name in ['DD','DTE']:
		wb.create_sheet(name)
		activeSheet = wb.get_sheet_by_name(name)
		activeSheet.append(hh.getHeaders(name))
	currentYear = datetime.date.now().year
	wb.save('%s\\svodniy_jurnal_DTE_%s.xlsm' %(cwd,currentYear))
	try:
		path = '%s\\config.txt' %cwd 
		fn = None if os.path.exists(path) else open(path,'tw',encoding='utf-8').close()
	except Exteption as ex:
		print('При создании файла конфигурации возникла ошибка')
	return None
	
def readWriteConfig(conf,mode,dict = None):
	if mode: #try to read config file
		cfgDict = {}	
		with open(conf,'r') as cfg:
			for line in cfg:
				splitLine = line.split('--')
				cfgDict[splitLine[0]] = [splitLine[1],splitLine[2]] #get values for path - sheetName - lastRow
		return cfgDict
	else: #try to write config file
		pass 
		if os.path.exists('%s\\config.txt' %cwd):
			pass
		else:
			file = open('config.txt', 'tw', encoding='utf-8')
			file.close()
		#open(conf, 'w').close() #clear config file
		with open(conf,'a') as cfg:
			for key in dict:
				for subKey in subDict:
					cfg.write('%s--%s--%s\n' %(key,subKey,subDict[subKey])) #path - sheetName - lastRow
	
def compileFile(jList,config,journal,cwd): #by cells
	wbToCopy = openpyxl.load_workbook(journal)
	#####clear compiled book
	for sheet in wbFromCopy.sheetnames:
		for row in sheet.iter_rows(row_offset=1, min_row = 1,max_row = sheet.max_row): #check specs for iter_rows
			for cell in row:
				sheetToCopy.cell(row = row ,column = cell.col_idx, value ='')
	#############
	for jItem in jList: 
		wbFromCopy = openpyxl.load_workbook(jItem,read_only=True)
		for sheetFromCopy in wbFromCopy.sheetnames:
			sheetName = sheetFromCopy.title.split('_')[0]  #example : DTE_NAME
			sheetToCopy = wbToCopy.get_sheet_by_name(sheetName.title) #copy cells to the same sheet in new workbook
			for row in sheet.iter_rows(row_offset=1, min_row = 1,max_row = sheetFromCopy.max_row): #check specs for iter_rows
				lastRow = sheetToCopy.max_row
				for cell in row:
					newCell = sheetToCopy.cell(row = lastRow + 1 ,column = cell.col_idx, value = cell.value)
					if cell.has_style: #get and copy cell style if it possible
						new_cell.style.font = cell.style.font
						new_cell.style.border = cell.style.border
						new_cell.style.fill = cell.style.fill
						new_cell.style.number_format = cell.style.number_format
						new_cell.style.protection = cell.style.protection
						new_cell.style.alignment = cell.style.alignment
				#lastRow += 1
	return None # ¯\_(ツ)_/¯
	
def main():
	timeStart = dt.datetime.now().hour
	workDir = os.getcwd()
	stopSwitch = False
	while stopSwitch:
		journalList,configFile,journalFile = findFiles(workDir)
		compileFile(journalList,configFile,journalFile,workDir)
		tt.sleep(900) #wait for 15 minutes and repeat cycle
		stopSwitch = ((dt.datetime.now().hour - timeStart) > 9)
	print(workDir)
	tt.sleep(10)
	sys.exit(0)
	
if __name__ == '__main__':
	main()
