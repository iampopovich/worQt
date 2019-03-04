import os
import worQt_nt

def main():
	if os.name == 'nt':
		worQt_nt.main()
	else: pass

if __name__ == '__main__':
	main()
