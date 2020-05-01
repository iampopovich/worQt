import os
import sys

def main():
	version = "2.13.0"
	if os.name == 'nt':
		import worQt_nt
		worQt_nt.main([])
	else: 
		import worQt_nix
		worQt_nix.main([])

if __name__ == '__main__':
	main()
