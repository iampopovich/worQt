import threading 
import time as tt
 
glob_index = 0

def iterate():
	global glob_index
	try:
		for i in range(7):
			tt.sleep(1)
			glob_index+=i
			print(glob_index)
		#glob_index/=0
	except Exception as ex : return ex

def main():	
	global glob_index
	while True:
		try:
			print('glob_index is equal now ...%s' %glob_index)
			if glob_index == 30: break
			t1 = threading.Thread(target = iterate, args = ())
			t1.start()
			t1.join()
		except:
			print('oops')
			tt.sleep(10)
			continue

if __name__ == '__main__':
	main()
