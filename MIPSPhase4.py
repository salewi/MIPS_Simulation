# phase4
#By: Dennis, Nii & Nobert
from MIPSPhase1 import BoolArray
from MIPSphase2 import CombinationalCircuits
from stage3outline import Memory,RegisterFile
from time import sleep 

class MIPS:
    def __init__(self):
        # Create and initalize the various permanent components
        # of the system diagram. {BoolArrays and Sequential circuit objects}
        # recall: The combinational components are simulated by functions
        #         not objects and can not be made into instance variables
        
        self.regs=RegisterFile()
        self.mem=Memory()
        
        self.pc=BoolArray("0",32)
        self.opcode=BoolArray("0",32)
        self.contrSig={}
        self.IR=self.mem.instrCycle(self.pc)
        self.pc4=BoolArray("0",32)
        self.jumpAdd=0


        self.rdData1=BoolArray("0",32)
        self.rdData2=BoolArray("0",32)
        self.extended=BoolArray("0",32)

        self.ir=BoolArray("0",32)
        
        self.data=0


                                           

        self.sum1,self.zero,self.memData,self.writeReg=0,0,0,0
        

        
#--------------------------------------------------------------------------

    #ADD helper functions as needed
    
        
    def run(self):
        
        #while opcode is not 63=3F=111111:
            # instruction fetch cycle
            
            
            # instruction decode cycle
            
            # register read cycle

            # execute cycle

            # memory access cycle

            # write back cycle

            # IO cycle

        r=0
        while self.opcode.toHex() !="3f " or self.opcode !=None:
            
            self._fetchCycle()
            self._decodeCycle()
            self._regReadCycle()
            self._executeCycle()
            self._accessCycle()
            self._ioCycle()
            r+=1

            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("THE END OF CIRCLE:",r)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            input("return to continue")

            
#--------------------------------------------------------------------------------------------------------

    def _fetchCycle(self):
        self.pc4=CombinationalCircuits.Add(self.pc,BoolArray("00000004",32))
        print("*************************************************************************************")
        print("The PC + 4 value is:",self.pc4)
        print("*************************************************************************************\n")

        self.IR=self.mem.instrCycle(self.pc)
        print("The instruction Register IR is:",self.IR)
        print("*************************************************************************************\n")

        self.opcode=self.IR.subArray(26,32)
        print("The opcode is:",self.opcode)
        print("*************************************************************************************\n")


#--------------------------------------------------------------------------------------------------------
                                           
                                        
    def _decodeCycle(self):
        self.contrSig=CombinationalCircuits.ControlUnit(self.opcode)
        print("The control Signal is:\n",self.contrSig)
        print("*************************************************************************************\n\n")

        p=self.IR.subArray(0,26)
        t="0000"+str(p)+"00"
        self.jumpAdd=hex(int(t,2))[2:]
        print("The jump address is:",self.jumpAdd)
        print("*************************************************************************************\n")
        
#--------------------------------------------------------------------------------------------------------

    def _regReadCycle(self):
        readReg1,readReg2,self.writeReg=int(self.IR.subArray(21,26)),int(self.IR.subArray(16,21)),int(self.IR.subArray(11,16))
        self.rdData1,self.rdData2=self.regs.readCycle(readReg1,readReg2,self.writeReg)
        print("*************************************************************************************\n")
        print("------------------------RegRead Circle--------------------------------------------")
        print("The regReg1 is:",readReg1)
        print("The regReg2 is:",readReg2)
        print("The WrtReg is:",self.writeReg)


        self.ir=self.IR.subArray(0,16)
        p=BoolArray(self.ir.toHex(),32)
        self.extended=CombinationalCircuits.Sign_extend(p)
        print("The sign extended value is:",self.extended)
        self.data=CombinationalCircuits.Mux(self.rdData2,self.extended,self.contrSig["ALUSrc"])
        print("The result from the Multiplexor in readCycle is:",self.data)
        print("*************************************************************************************\n")

         
#--------------------------------------------------------------------------------------------------------
       
    def _executeCycle(self):

        a=CombinationalCircuits.ALUControl(self.contrSig["ALUOp"],self.ir)
        self.sum1,self.zero=CombinationalCircuits.ALU(self.rdData1,self.data,a)
        print("*************************************************************************************\n")
        print("-------------------------Execute Cycle-------------------------------------------")
        print("The output from ALU is:",self.sum1)
        print("The zero bit is:",self.zero)

        shiftL2=CombinationalCircuits.Shift_left_2(self.extended)
        print("The shift left two value is:",shiftL2)        
        adder=CombinationalCircuits.Add(shiftL2,self.pc4)
        control=self.zero and self.contrSig["Branch"]

        self.data=CombinationalCircuits.Mux(self.pc4,adder,control)
        print("First Multiplexor after adder is:",self.data)

        self.data=CombinationalCircuits.Mux(self.data,BoolArray(self.jumpAdd,32),self.contrSig["Jump"])
        self.pc=self.data
        print("The value of PC is:",self.pc)
        print("*************************************************************************************\n")

                                                    

#--------------------------------------------------------------------------------------------------------

    def _accessCycle(self):
        self.memData=self.mem.dataCycle(self.sum1,self.rdData2,self.contrSig["MemWrite"],self.contrSig["MemRead"])
        print("*************************************************************************************\n")
        print("--------------------Memory Acces Cycle------------------------------------------")
        print("The value of the memory output is:",self.memData)
        self.data=CombinationalCircuits.Mux(self.sum1,self.memData,self.contrSig["MemtoReg"])
        print("The output from the multiplexor is:",self.data)
        self.regs.writeCycle(self.contrSig["RegWrite"],self.data)
        if self.contrSig["RegWrite"]:
            print(self.data.toHex(),"store in", self.regs.writeReg)
        print("The writeReg current value is:",self.writeReg)
        print("*************************************************************************************\n")

    

#--------------------------------------------------------------------------------------------------------

    def _ioCycle(self):
        print("*************************************************************************************\n")
        print("--------------------------IO Cycle----------------------------------------------------")
        
        print("*************************************************************************************\n")

        inflag=int(self.mem.instrCycle(BoolArray("3f0",32)))
        inbuffer=self.mem.instrCycle(BoolArray("3f4",32))
        outflag=int(self.mem.instrCycle(BoolArray("3f8",32)))
        outbuffer=self.mem.instrCycle(BoolArray("3fc",32))

        
        if inflag !=0:
            inbuffer=BoolArray(input("Enter a  8bit Hexadecimal: "),32)
            inflag=0
            
        if outflag !=0:
            print("The output buffer is:\n")
            print(outbuffer)
            outflag=0
            print("********************************************************************")
        

#--------------------------------------------------------------------------------------------------------

    def showMemory(self):
        # call your Memory object's showMemory() method
        print("*********************************************************************************")
        print("------------------------------MEMORY-------------------------------------")
        self.mem.showMemory()
        print("-------------------------------------------------\n")

#--------------------------------------------------------------------------------------------------------

    def showRegisters(self):
        # call your RegisterFile objects's showRegisters() method
        print("****************************************************************************")
        print("---------------------he REGISTERS---------------------------------------")
        self.regs.showRegisters()
    

#--------------------------------------------------------------------------------------------------------
     
    
    def loadProgram(self,fname):
        # call your Memory object's loadProgram() method
        self.mem.loadProgram(fname)

#--------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    mips=MIPS()
    mips.loadProgram(input("What machine language file?: "))
    mips.run()
    mips.showMemory()
    mips.showRegisters()
