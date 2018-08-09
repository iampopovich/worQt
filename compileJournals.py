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

def getHeaders(key):
	names = {'ДД':['Директивный документ','Этап контроля','Обозначение ДД',
					'Размещение ДД в структуре папок ОКБ','Процедура выпуска',
					'Оформление ДД','Соответствие ДД модели данных',
					'Модуль создания ДД','Применяемость','Указание о внедрении/заделе',
					'Согласовано','Примечание','Дата','Проверку выполнил'],
			'ДТЭ':['Обозначение КД / Ревизия-Наименование',
					'Тип объекта','Владелец','Подразделение','Обозначение ДД',
					'Этап контроля','Обозначение / Процедура выпуска',
					'Размещение в структуре папок ОКБ\nВходимость в головную сборку / проект',
					'Соответствие модели данных / Время сохранения',
					'Оформление / Состав ЭМ','Ограничения / WAVE-связи','Масса / Материал / Атрибуты',
					'Геометрия / Допуски','Слои / Ссылочные наборы','Анализ зазоров','Согласовано'
					'Документ на отклонение от требований НД','Дата','Проверку выполнил']}
	return names.get(key)

def findFiles(cwd):
	currentYear = dt.datetime.now().year
	xlFiles = [path.join(cwd, f) for f in os.listdir(cwd) if path.isfile(path.join(cwd, f))] #сеим директории, оставляем файлы
	try:	#этих файлов может и не быть , на всякий случай расставь экспы
		cJournalName = '%sСводный_журнал_ДТЭ_%s.xlsm' %(cwd,currentYear)
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
		activeSheet.append(getHeaders(sheetName))
	wb.save('%s' %(name))
	return None
	
def clearJournal(journal):
	wbToCopy = openpyxl.load_workbook(journal)
	for sheet in wbToCopy.sheetnames:
		cSheet = wbToCopy[sheet]
		for row in cSheet.iter_rows(): #check specs for iter_rows
			for cell in row:
				cSheet.cell(row = cSheet._current_row, column = cell.col_idx, value ='')
	wbToCopy.save(journal)

def compileFile(jList,journal): #by cells
	wbToCopy = openpyxl.load_workbook(journal)
	for jItem in jList: 
		wbFromCopy = openpyxl.load_workbook(jItem,read_only=True)
		for sheetFromCopy in wbFromCopy.sheetnames:
			sheetName = sheetFromCopy.title.split('_')[0]  #example : DTE_NAME
			sheetToCopy = wbToCopy[sheetName.title] #copy cells to the same sheet in new workbook
			for row in sheet.iter_rows(): #check specs for iter_rows
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
	tStart = dt.datetime.now().hour
	workDir = whatOSRun(os.getcwd()) #определяем параметры ввода пути до файла
	stopSwitch = False
	journalList,journalFile = findFiles(workDir)
	#while not(stopSwitch):
	#	clearJournal(journalFile)
	#	compileFile(journalList,journalFile)
	#	tt.sleep(900) #wait for 15 minutes and repeat cycle
	#	stopSwitch = ((dt.datetime.now().hour - tStart) > 9)
	#tt.sleep(10)
	#sys.exit(0)
	
if __name__ == '__main__':
	main()
