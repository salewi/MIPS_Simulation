# phase two, all the combinational circuit components
# as functions in module Circuit
#By: Dennis 

from MIPSPhase1  import BoolArray
from copy import deepcopy

class CombinationalCircuits:
    def ControlUnit(op):
        # return a dictionary with keys: "RegDest", "Jump", "Branch", "MemRead",
        #           "MemToReg", "ALUOp", "MemWrite", "ALUSrc", and "RegWrite"
        # with appropriate boolean values for each (see handout or text)
        # ALUOp is set to
        #         (False, False) if op in x00,
        #         (False,True)   if op is x08, x23,or x2B
        #         (True,False)   if op is x04
               
        opco=op
        opc=opco.toHex()
        
        if opc=="00":
            dictionary={"RegDst":True, "Jump":False, "Branch":False, "MemRead":False,
              "MemtoReg":False, "ALUOp":(False,False), "MemWrite":False, "ALUSrc":False,  "RegWrite":True}
        elif opc =="02":
            dictionary={"RegDst":False, "Jump":True, "Branch":False, "MemRead":False,
              "MemtoReg":False, "ALUOp":(False,False), "MemWrite":False, "ALUSrc":False,  "RegWrite":False}
        elif opc=="04":
            dictionary={"RegDst":False, "Jump":False, "Branch":True, "MemRead":False,
              "MemtoReg":False, "ALUOp":(True,False), "MemWrite":False, "ALUSrc":False,  "RegWrite":False}
        elif opc=="08":
            dictionary={"RegDst":False, "Jump":False, "Branch":False, "MemRead":False,
              "MemtoReg":False, "ALUOp":(False,True), "MemWrite":False, "ALUSrc":True,  "RegWrite":True}
        elif opc=="23":
            dictionary={"RegDst":False, "Jump":False, "Branch":False, "MemRead":True,
              "MemtoReg":True, "ALUOp":(False,True), "MemWrite":False, "ALUSrc":True,  "RegWrite":True}
        elif opc=="2B" or opc=="2b":
            dictionary={"RegDst":False, "Jump":False, "Branch":False, "MemRead":False,
              "MemtoReg":False, "ALUOp":(False,True), "MemWrite":True, "ALUSrc":True,  "RegWrite":False}
        else:
            return
        return dictionary 
#------------------------------------------------------------------------------------------------------------------------------

   
    def ALUControl(ALUOp,shftfunc):
        # function is bits 0..5, shftamt is bits 6..10
        # create and return a dictionary with keys:
        #         "ENA", "ENB", "INVA", "INC", "SL", "SR", "amt"
        # depending on ALUOp and shft func (see handout or text)
        # "amt" is an integer 0..31,  the rest are boolean
        
        f=shftfunc
        function=f.subArray(0,6)
        funct=function.toHex()
        shiftamount=f.subArray(6,11)
        shiftamt=int(shiftamount)

        val1,val2=ALUOp[0],ALUOp[1]

        if (val1==False and val2==True) :
            dictionary={"F0":True,"F1":True,"ENA":True,"ENB":True,"INVA":False,"INCA":False,"SL":False,"SR":False,"amt":shiftamt}
            
        elif (val1==True  and val2==False) :
            dictionary={"F0":True,"F1":True,"ENA":True,"ENB":True,"INVA":True,"INCA":True,"SL":False,"SR":False,"amt":shiftamt}

        elif (val1==False  and val2==False) and  funct=="00":
            dictionary={"F0":False,"F1":True,"ENA":True,"ENB":False,"INVA":False,"INCA":False,"SL":True,"SR":False,"amt":shiftamt}

        elif (val1==False  and val2==False) and funct=="02":
            dictionary={"F0":False,"F1":True,"ENA":True,"ENB":False,"INVA":False,"INCA":False,"SL":False,"SR":True,"amt":shiftamt}


        elif (val1==False  and val2==False) and funct=="20":
            dictionary={"F0":True,"F1":True,"ENA":True,"ENB":True,"INVA":False,"INCA":False,"SL":False,"SR":False,"amt":shiftamt}

        elif (val1==False  and val2==False) and funct=="22":
            dictionary={"F0":True,"F1":True,"ENA":True,"ENB":True,"INVA":True,"INCA":True,"SL":False,"SR":False,"amt":shiftamt}

        elif (val1==False and val2==False) and funct=="24":
            dictionary={"F0":False,"F1":False,"ENA":True,"ENB":True,"INVA":False,"INCA":False,"SL":False,"SR":False,"amt":shiftamt}

        elif (val1==False  and val2==False) and funct=="25":
            dictionary={"F0":False,"F1":True,"ENA":True,"ENB":True,"INVA":False,"INCA":False,"SL":False,"SR":False,"amt":shiftamt}

        else:
            print("ALU Control internal error<unrecognised function or ALUOp>")
            
        return dictionary 
#------------------------------------------------------------------------------------------------------------------------------

    
    def Mux(A0,A1,c):
        # a two way multiplexor
        # A0 and A1 are BoolArray objects of equal length
        # if c is False it returns a copy of A0
        # if c is True  it returns a copy of A1
        A00=deepcopy(A0)
        A11=deepcopy(A1)
        if c:
            return A11
        elif not c:
            return  A00
        else:
            return 
#------------------------------------------------------------------------------------------------------------------------------
        

    def shift(A,ALUcontrol):
        # A is a 32-bit BoolArray
        # ALUcontrol is a dict with keys "SL","SR", "amt" (and possibly others)
        # amt is a non-neg integer, SL and SR are boolean
        
        b=BoolArray("0",32)

        SL,SR=ALUcontrol["SL"],ALUcontrol["SR"]
        b.setBit(0,((A.getBit(0) and not SL and not SR) or (A.getBit(1) and SR) ))  
        b.setBit(31,(A.getBit(30) and SL) or(A.getBit(31) and (not SL) and (not SR)))    

        for i in range(1,31):
            b.setBit(i,( (A.getBit(i-1) and SL) or (A.getBit(i) and (not SR) and (not SL)) or (A.getBit(i+1) and SR)))
       
        return b
        
#------------------------------------------------------------------------------------------------------------------------------

    def Shift_left_2(A):
        # return a BoolArray which is A shifted two bits left (logically)
        # if b is more than 32 bits chop high order bits to make 32
        
         dic={"SL":True,"SR":False}
         b=CombinationalCircuits.shift(A,dic)
         c=CombinationalCircuits.shift(b,dic)

         return c
#------------------------------------------------------------------------------------------------------------------------------
         
    def ALU_1(A,B,F0,F1,ENA,ENB,INVA,C):
        # implements the 1 bit ALU given on the class handout
        # returns c_out,s_out, (a carry and sum bit) both boolean
        # it is called 32 times by the AL

        T1 = B and ENB
        T2 = ENA and A
        T3 = INVA and not T2 or not INVA and T2
        
        T4 = not F0 and not F1
        T5 = not F0 and F1
        T6 = F0 and not F1
        T7 = F0 and F1

        T8 = T3 and T1
        T9 = T3 or T1
        T10 = not T1
        T11 = T8 and T4
        T12 = T9 and T5
        T13 = T10 and T6

        T14 = T3 and not T1 or not T3 and T1
        T15 = T1 and T3 and T7
        T16 = T7 and T14 and C
        T17 = T15 or T16
        T18 = C and not T14 or not C and T14
        T19 = T18 and T7
        
        c_out = T17
        s_out = T11 or T12 or T13 or T19       

        return c_out,s_out
#------------------------------------------------------------------------------------------------------------------------------

    
    def ALU(A,B,control):
        # a 32 ripple ALU that chains 32 1-bit ALUs
        # the intermediate b is then set to the shifter
        # to produce the final return b
        ####################################################
        # A and B are 32-bit BoolArray
        # control is a dictionary as output by ControlUnit
        # returns R,z where R is a 32-bit BoolArray and z is a boolean that
        # that is True of R is zero
        
        F0,F1,ENA,ENB,INVA,INCA,SL,SR,amt=control["F0"],control["F1"],control["ENA"],control["ENB"],control["INVA"],control["INCA"],control["SL"],control["SR"],control["amt"]
        sum1=BoolArray("0",32)
        c=INCA
        for i in range(32):
            c,s=CombinationalCircuits.ALU_1(A.getBit(i),B.getBit(i),F0,F1,ENA,ENB,INVA,c)
            sum1.setBit(i,s)
        for i in range(amt):
            sum1=CombinationalCircuits.shift(sum1,control)
        zero=int(sum1)==0

        return sum1,zero 
#------------------------------------------------------------------------------------------------------------------------------

    def Add(A,B):
        # A and B are 32-bit BoolArrays
        # returns A+B  a 32-bit BoolArray (may or may not use ALU)
        a=int(A)
        b=int(B)
        h=a+b
        
        return BoolArray(hex(h)[2:],32)
#------------------------------------------------------------------------------------------------------------------------------
      

    def Sign_extend(A):
        # A is a 16-bit BoolArray
        # returns 32-bit BoolArray that is A with its sign extended
        bit=A.getBit(15)
        B=BoolArray(A.toHex(),32)

        for i in range(16,32):
            B.setBit(i,bit)
            
        return B 
 #------------------------------------------------------------------------------------------------------------------------------
           

