import threading 
import time as tt

 
glob_index = 0

def iterate(queries):
	global glob_index
	try:
		for i,query in enumerate(queries):
			tt.sleep(1)
			glob_index+=i
	except Exception as ex : return ex

def main():	
	global glob_index
	while True:
		try:
			if glob_index == len(queries): break
			t1 = threading.Thread(target = iterate, args = (queries[index:]))
			t1.start()
			t1.join()
		except:
			print('oops')
			tt.sleep(10)
			continue

if __name__ == '__main__':
	main()
