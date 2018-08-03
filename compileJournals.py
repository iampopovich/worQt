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
	currentYear = datetime.date.today().year
	xlFiles = [f for f in os.listdir(cwd) if isfile(os.join(cwd, f))]
	xlFiles = [lambda x: re.search(r'.*ДТЭ.*%s.*xlsm' %currentYear, xlFiles).group(0)]
	for item in xlFiles:
		if re.search(r'.*Сводный_журнал_ДТЭ.*%s.*xlsm' %currentYear, item) == None:
			createJournal(cwd)
		else:
			cJournal = item
			xlFiles.pop(xlFiles.index(item))
	for file in os.listdir(cwd):
		if file.endswith("config.txt"):
			comfigFile = os.join(cwd,file)
	return xlFiles,config,cJournal

def createJournal(cwd):
	wb = openpyxl.Workbook()
	for name in ['ДД','ДТЭ']:
		wb.create_sheet(name)
		activeSheet = wb.get_sheet_by_name(name)
		activeSheet.append(hh.getHeaders(name))
	currentYear = datetime.date.today().year
	wb.save('%s\\Сводйный_журнал_ДТЭ_%s.xlsm' %(cwd,currentYear))
	try:
		f = pass if os.path.exists('%s\\config.txt' %cwd) else open('config.txt', 'tw', encoding='utf-8').close()
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
		f = pass if os.path.exists('%s\\config.txt' %cwd) else open('config.txt', 'tw', encoding='utf-8').close()
		open(conf, 'w').close() #clear config file
		with open(conf,'a') as cfg:
			for key in dict:
				for subKey in subDict:
					cfg.write('%s--%s--%s\n' %(key,subKey,subDict[subKey])) #path - sheetName - lastRow
	
def compileFile(jList,config,journal,cwd): #by cells
	workbook = openpyxl.load_workbook(journal)
	#wb = op.load_workbook('/tmp/test.xlsx', use_iterators=True) без этого может не работать итератор
	if os.stat(config).st_size == 0:
		startPos = 0
	else:
		userConf = readWriteConfig(config,True)
	for jItem in jList: #append new row in journal  
		wb = openpyxl.load_workbook(jItem,read_only=True)
		for sheet in wb.sheetnames:
			sheetName = sheet.title.split('_')[0]  #example : DTE_NAME
			userName = sheet.title.split('_')[1]   #example : DD_NAME
			startPosRow = userConf[jItem][sheetName] + 1
			endPosCol = sheet.max_column #get max column for iterator through columns in same sheets
			startPosRowToCopy = wb.max_row + 1 #get first empty row in book
			sheetToCopy = workbook.get_sheet_by_name(sheetName.title) #copy cells to the same sheet in new workbook
			for row in sheet.iter_rows(row_offset=1, min_row = startPos,max_row = endPos):
				for cell in row:
					newCell = sheetToCopy.cell(row = startPosRowToCopy,column = cell.col_idx, value = cell.value)
					if cell.has_style: #get and copy cell style if it possible
						new_cell.style.font = cell.style.font
						new_cell.style.border = cell.style.border
						new_cell.style.fill = cell.style.fill
						new_cell.style.number_format = cell.style.number_format
						new_cell.style.protection = cell.style.protection
						new_cell.style.alignment = cell.style.alignment
				newCell = sheetToCopy.cell(row = startPosRowToCopy,column = endPosCol + 1, value = userName) #дописываем фамилию в конец строки (после последнего столбца)
				startPosRowToCopy+=1
		userConf[jItem] = {sheetName:endPos}#####
		readWriteConfig(config,False,userConf)
	return None # ¯\_(ツ)_/¯
	
def main():
	workDir = os.getcwd()
	journalList,configFile,journalFile = findFiles(workDir)
	compileFile(journalList,configFile,journalFile,workDir)
	
if __name__ == '__main__':
	main()
