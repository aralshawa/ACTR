import os
import re

REF_SPECTRUM = {};

#Call me on startup to generate the dict
def CreateReference():
     for root, dirs, files in os.walk(os.path.dirname(os.path.realpath('__file__'))+"\spectraldata"):
        for file in files:
            if file.endswith(".txt"):
                
                element = os.path.splitext(file)[0]
                f = os.path.join(root, file)
                spec = open(f,"r") 
                data = spec.read().split()
                wavelength = data [::2]
                intensity = data[1::2]
                tuples = []

                for i in range(len(wavelength)):
                    wavelength[i] =  float("%.4f"%(float(wavelength[i])/10000.0))
                    temp = (wavelength[i],intensity[i])
                    tuples.append(temp)

                REF_SPECTRUM[element.upper()] = tuples 

#Call me to retrieve the dict
def GetReferece():
    return REF_SPECTRUM

def main():
    CreateReference()
    g = GetReferece()
    #print (REF_SPECTRUM) 
    for key,val in g.items():
        print (key)
        for s in val:
            print (s[0],"-",s[1])
        print ("")
 
if __name__ == '__main__':
    main()
