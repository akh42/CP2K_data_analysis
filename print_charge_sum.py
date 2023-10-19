# Script to find the sum of Mulliken charges of individual element types in CP2K output file
# CP2K input must have &MULLIKEN .. &END  inside the &PRINT section of &DFT to get the required output information
# Input format: python <scriptname.py> <cp2k_output_filename.out> <number of atoms in the system> <element name>

import sys,os

def mulliken_list(nat,cp2k_out,mkdat):
    os.system("grep Mulliken -A %d  %s | tail -%d > %s" %(nat+2, cp2k_out, nat, mkdat))

def sumchg_list(mkdat,element):
    tot_chg = 0.0
    with open(mkdat,'r') as f:
        for line in f:
            x = line.strip().split()
            if x[1].title() == element.title(): 
                tot_chg = tot_chg + float(x[5])
    return(tot_chg)

def main():
    cp2k_out = sys.argv[1]
    nat = int(sys.argv[2])
    element =sys.argv[3]
    mkdat = 'mk.dat'
    mulliken_list(nat,cp2k_out,mkdat)
    os.system("grep %s %s | awk '{print $6}' > %s_mk.dat" %(element, mkdat, element))
    tot_chg = sumchg_list(mkdat,element)
    print("Sum of Mulliken charges of all %s atoms in the system"%element)
    print("%12.6f"%tot_chg)
    with open('%s_mksum.txt'%element,'w') as f:
        f.write("%12.6f\n"%tot_chg)

if __name__ == "__main__":
    main()

#EOF
