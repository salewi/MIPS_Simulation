# phase 3 control unit
#Dennis John Salewi,Olaniyi Omiwale, Nobert Kimario
from MIPSPhase1 import BoolArray

class RegisterFile:
    def __init__(self):
        # The register file is a list of 32 32-bit registers (BoolArray)
        # register 29 is initialized to "000003E0" the rest to "00000000"
        # an instance vaariable for writeReg is initialized to 0
        
        self.regFile=[]
        for i in range(0,32):
            if i==29:
                self.regFile.append(BoolArray("000003E0",32))
            else:
                self.regFile.append(BoolArray("00000000",32))
        self. writeReg=0
        
    def readCycle(self,readReg1,readReg2,writeReg):
        # readReg1, readReg2, and writeReg are integers 0..31
        # writeReg is 'remembered' in the instance variable
        # copies of the two read registers are returned (BoolArrays)

        self.writeReg=writeReg
        read1,read2=self.regFile[readReg1],self.regFile[readReg2]

        return read1,read2
                                    
    
    def writeCycle(self,RegWrite,data):
        # RegWrite is a boolean indicating that a write should occur
        # data is a BoolArray to be written if RegWrite is true
        # if the RegWrite control is True,
        #    the value of data is copied into the writeReg register
        #    where writeReg is the value most remembered from the most
        #    recent read cycle 
        # if RegWrite is false, no values change
        # NOTE: if writeReg is 0, nothing happens since $zero is constant

        if RegWrite==True:
            self.regFile[self.writeReg]=data
            
        else:
            return 
    
    def getReg(self,i):
        # returns a copy of the BoolArray in register i
        return self.regFile[i]
    

    def showRegisters(self):
        # prints the index and hex contents of all non-zero registers
        # printing all registers is ok too but wastes screen real estate
        h=self.regFile(self)
        for i in range(len(regFile)):
            h=self.regFile(self)
            if h !=0:
                print(str(h))
            else:
                return
                

class Memory:
    # lets use 2K memory and map
    # 3FC,3Fd,3FE,3FF for inbuff,inflag,outbuff,outflag
    # sp is 3E0 and grows down
    
    def __init__(self):
        # creates a dictionary of BoolArrays whose
        #              keys are 0, 4, 8, ... , 1020 and
        #              values are all BoolArray("0",32)
        self.dicti={}
        for i in range(0,1021):
            self.dicti[i]=BoolArray("0",32)
        

    def showMemory(self):
        # print a nicely formatted table of non-zero memory
        print(" RegLocation", "                             ", "Data")
        print("+---------------------------------------------------------------+")
        for i in range(0,1021):
            if int(self.dicti[i]) !=0:
                print("|  ",i,"         |           ",self.dicti[i].toHex(), "   |")
           
            else:
                return -1
        print("+---------------------------------------------------------------+") 
    
    def loadProgram(self,fname):
        # fname is the name of a text file that contains
        # one 8-digit hexidecimal string per line
        # they are cnverted to BoolArray and
        # read sequentially into memory in
        # locations 0, 4, 8, 12, ...
        f=open(fname,"r")
        temp=f.read()
        boolVals=[BoolArray(x[:8],32) for x in temp.split()]
        for i in range(0,len(boolVals)*4,4):
            self.dicti[i]=boolVals[i//4]
        f.close()

        
    def instrCycle(self,PC):
        # PC is a BoolArray
        # returns a copy of the memory address int(PC)
        p=PC
        return self.dicti[int(p)]
    

    def dataCycle(self,Address,WriteData,ReadMem,WriteMem):
        # Address and Write Data are BoolArrays
        # ReadMem and WriteMem are booleans (not both True)
        # if ReadMem True:
        #        return a copy of the BoolArray at mem[int(address)]
        # if WriteMem is True:
        #        a copy of WriteData is placed at mem[int(address)]
        #        a BoolArray("00000000",32) is returned
        if ReadMem:
            p= self.dicti[int(Address)]
            return p
        elif WriteMem:
            k=WriteData
            self.dicti[int(Address)]=k
            return BoolArray("00000000",32)
        else:
            return BoolArray("0",32)

if __name__=="__main__":
    d=Memory()
    d.showMemory()
