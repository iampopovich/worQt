#!/usr/bin/pythom
#-*-coding: utf-8-*-
import math
import openpyxl
import time as tt
import datetime as dt
import re
import os
import sys
'''
def findFiles(cwd):
def createJournal(cwd):
def compileFile(jList,config,journal,cwd):
def readWriteConfig(conf,mode,dict = None):
'''
def getHeaders(key):
	names = {'ДД':['Директивный документ','Этап контроля','Обозначение ДД',
					'Размещение ДД в структуре папок ОКБ','Процедура выпуска',
					'Оформление ДД','Соответствие ДД модели данных',
					'Модуль создания ДД','Применяемость','Указание о внедрении/заделе',
					'Согласовано','Примечание','Дата','Проверку выполнил'],
			'ДТЭ':['Обозначение КД/Ревизия-Наименование',
					'Тип объекта','Владелец','Подразделение','Обозначение ДД',
					'Этап контроля','Обозначение /Процедура выпуска',
					'Размещение в структуре папок ОКБ\nВходимость в головную сборку/проект',
					'Соответствие модели данных/Время сохранения',
					'Оформление/Состав ЭМ','Ограничения/WAVE-связи','Масса/Материал/Атрибуты',
					'Геометрия/Допуски','Слои/Ссылочные наборы','Анализ зазоров','Согласовано'
					'Документ на отклонение от требований НД','Дата','Проверку выполнил']}
	return names.get(key)

def findFiles(cwd):
	currentYear = dt.datetime.now().year
	xlFiles = [f for f in os.listdir(cwd) if isfile(os.join(cwd, f))]
	xlFiles = [lambda x: re.search(r'.*DTE.*%s.*xlsm' %currentYear, xlFiles).group(0)]
	for xlItem in xlFiles:
		if re.search(r'.*Сводный_журнал_ДТЭ.*%s.*xlsm' %currentYear, xlItem) == None:
			createJournal(cwd)
		else:
			cJournal = xlItem
			xlFiles.pop(xlFiles.index(xlItem))
	return xlFiles,cJournal

def createJournal(cwd):
	wb = openpyxl.Workbook()
	for name in ['ДД','ДТЭ']:
		wb.create_sheet(name)
		activeSheet = wb.get_sheet_by_name(name)
		activeSheet.append(getHeaders(name))
	currentYear = dt.datetime.now().year
	wb.save('%s\\Сводный_журнал_ДТЭ_%s.xlsm' %(cwd,currentYear))
	return None
	
def compileFile(jList,journal,cwd): #by cells
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
	tStart = dt.datetime.now().hour
	workDir = os.getcwd()
	stopSwitch = False
	journalList,journalFile = findFiles(workDir)
	while not(stopSwitch):
		compileFile(journalList,journalFile,workDir)
		tt.sleep(900) #wait for 15 minutes and repeat cycle
		stopSwitch = ((dt.datetime.now().hour - tStart) > 9)
	tt.sleep(10)
	sys.exit(0)
	
if __name__ == '__main__':
	main()
