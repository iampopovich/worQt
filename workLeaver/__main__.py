import os
import worQt_nt

def main():
	if os.name == 'nt':
		worQt_nt.main()
	else: 
		worQt_nix.main()

if __name__ == '__main__':
	main()
