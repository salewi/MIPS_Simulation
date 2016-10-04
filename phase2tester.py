# Unit Test for the TestCombinationalCircuits class

import unittest              # import unittesting

from MIPSPhase1 import BoolArray               # import your stage one class
from MIPSphase2 import CombinationalCircuits   # import your stage two class

class TestUnitClass2(unittest.TestCase):

   def setUp(self):
      self.A = BoolArray("01234567",32)
      self.B = BoolArray("3FFEDCBA",32)
      self.C = BoolArray("01230ABC",32)
      self.D = BoolArray("00E00E00",32)


   def testMultiplexor(self):
      '''Testing MUX method'''
      A0 = BoolArray("BAD00DAD",32)
      A1 = BoolArray("F00D4DAD",32)
      self.assertEqual(int(CombinationalCircuits.Mux(A0,A1,False)), int(A0))
      self.assertEqual(int(CombinationalCircuits.Mux(A0,A1,True)),  int(A1))

   def test_SignExtention(self):
      '''Testing Sign Extender   (sign extend a 16-bit int to a 32 bit int)'''
      E = BoolArray("00BA",16)
      F = BoolArray("FF73",16)
      E1=CombinationalCircuits.Sign_extend(E).toHex()
      F1=CombinationalCircuits.Sign_extend(F).toHex()
      self.assertTrue(E1 in ["000000BA","000000ba"])
      self.assertTrue(CombinationalCircuits.Sign_extend(F).toHex() in ["FFFFFF73","ffffff73"])

   def test_ALU_add(self):
      '''Testing ALU add method'''
      control ={"F0":True,"F1":True,"ENA":True,"ENB":True,
                       "INVA":False,"INCA":False,"SL":False,"SR":False,"amt":0}
      result,zero = CombinationalCircuits.ALU(self.A,self.B,control)
      self.assertEqual(result.toHex(),"41222221")
      self.assertFalse(zero)
      
   def test_ALU_subtract(self):
      '''Testing ALU subtraction'''
      control ={"F0":True,"F1":True,"ENA":True,"ENB":True,
                       "INVA":True,"INCA":True,"SL":False,"SR":False,"amt":0}
      result,zero = CombinationalCircuits.ALU(self.A,self.B,control)
      self.assertTrue(result.toHex() in["3EDB9753","3edb9753"])
      self.assertFalse(zero)
      
   def test_ALU_zero(self):
      '''Testing zero bit'''
      control ={"F0":True,"F1":True,"ENA":True,"ENB":True,
                       "INVA":True,"INCA":True,"SL":False,"SR":False,"amt":0}

      result,zero = CombinationalCircuits.ALU(self.A,self.A,control)
      self.assertEqual(result.toHex(),"00000000")
      self.assertTrue(zero)
      
   def test_ALU_NOP(self):
      '''Testing ALU NOP'''
      control ={"F0":False,"F1":True,"ENA":True,"ENB":False,
                       "INVA":False,"INCA":False,"SL":False,"SR":False,"amt":0}
      result,zero = CombinationalCircuits.ALU(self.A,self.B,control)
      self.assertEqual(self.A.toHex(),result.toHex())
      
   def test_ALU_OR(self):
      '''Testing ALU OR'''
      control ={"F0":False,"F1":True,"ENA":True,"ENB":True,
                       "INVA":False,"INCA":False,"SL":False,"SR":False,"amt":0}
      result,zero = CombinationalCircuits.ALU(self.A,self.B,control)
      self.assertTrue(result.toHex() in ["3FFFDDFF","3fffddff"])
      self.assertFalse(zero)
      
   def test_ALU_AND(self):
      '''Testing ALU AND'''
      control ={"F0":False,"F1":False,"ENA":True,"ENB":True,
                       "INVA":False,"INCA":False,"SL":False,"SR":False,"amt":0}
      result,zero = CombinationalCircuits.ALU(self.A,self.B,control)
      self.assertEqual(result.toHex(),"01224422")
      self.assertFalse(zero)
      
   def test_ALU_shiftleft(self):
      '''Testing ALU shift left'''
      control ={"F0":False,"F1":True,"ENA":True,"ENB":False,
                       "INVA":False,"INCA":False,"SL":True,"SR":False,"amt":3}
      result,zero = CombinationalCircuits.ALU(self.A,self.B,control)
      self.assertTrue(result.toHex() in ["091A2B38","091a2b38"])
      self.assertFalse(zero)
      
   def test_ALU_shiftright(self):
      '''Testing ALU shift right'''
      control ={"F0":False,"F1":True,"ENA":True,"ENB":False,
                       "INVA":False,"INCA":False,"SL":False,"SR":True,"amt":7}
      result,zero = CombinationalCircuits.ALU(self.A,self.B,control)
      self.assertTrue(result.toHex() in ["0002468A","0002468a"])
      self.assertFalse(zero)
      
   def test_Adder(self):
      '''Testing Adder'''
      result = CombinationalCircuits.Add(self.C,self.D)
      self.assertTrue(result.toHex() in ["020318BC","020318bc"])

   def test_CU_00(self):
      '''Testing op 00'''
      rd,j,b,mr,m2r,mw,s,rw="RegDst","Jump","Branch","MemRead","MemtoReg","MemWrite","ALUSrc","RegWrite"
      # op 0x00
      d = CombinationalCircuits.ControlUnit(BoolArray("00",6))
      self.assertTrue(d["RegDst"] and not d["Jump"] and not d["Branch"] and not d["MemWrite"] and
            not d["ALUSrc"] and d["RegWrite"] and not d["ALUOp"][0] and not d["ALUOp"][1])

   def test_CU_02(self):
      '''Testing op 02'''
      d = CombinationalCircuits.ControlUnit(BoolArray("02",6))
      self.assertTrue(d["Jump"] and not d["RegWrite"])

   def test_CU_04(self):
      '''Testing op 04'''
      d = CombinationalCircuits.ControlUnit(BoolArray("04",6))
      self.assertTrue(not d["Jump"] and d["Branch"] and not d["MemWrite"] and not d["ALUSrc"] and
            not d["RegWrite"] and d["ALUOp"][0] and not d["ALUOp"][1])

   def test_CU_08(self):
      '''Testing op 08'''
      d = CombinationalCircuits.ControlUnit(BoolArray("08",6))
      self.assertTrue (not d["RegDst"] and not d["Jump"] and not d["Branch"] and not d["MemRead"] and not d["MemtoReg"] and not d["MemWrite"] and
            d["ALUSrc"] and d["RegWrite"] and not d["ALUOp"][0] and d["ALUOp"][1])

   def test_CU_23(self):
      '''Testing op 23'''
      d = CombinationalCircuits.ControlUnit(BoolArray("23",6))
      self.assertTrue(not d["RegDst"] and not d["Jump"] and not d["Branch"] and d["MemRead"] and d["MemtoReg"] and not d["MemWrite"] and
            d["ALUSrc"] and d["RegWrite"] and not d["ALUOp"][0] and d["ALUOp"][1])

   def test_CU_2B(self):
      '''Testing op 2B'''
      d = CombinationalCircuits.ControlUnit(BoolArray("2B",6))
      assert (not d["Jump"] and not d["Branch"] and d["MemWrite"] and
            d["ALUSrc"] and not d["RegWrite"] and not d["ALUOp"][0] and d["ALUOp"][1])

   def test_ALUcontrol_add(self):
      # ALUop (F,T) (add)
      c = CombinationalCircuits.ALUControl((False,True),BoolArray("0",11))
      self.assertTrue (c["F0"] and c["F1"] and c["ENA"] and c["ENB"] and not c["INVA"] and
            not c["INCA"] and not c["SL"] and not c["SR"] and c["amt"]==0 )

   def test_ALUcontrol_sub(self):
      # ALUop (T,F) (sub)
      c = CombinationalCircuits.ALUControl((True,False),BoolArray("0",11))
      self.assertTrue(c["F0"] and c["F1"] and c["ENA"] and c["ENB"] and c["INVA"] and
            c["INCA"] and not c["SL"] and not c["SR"] and c["amt"]==0)
   def test_ALUcontrol_shiftleft(self):
      # ALUop (F,F),  funct = x00  S
      c = CombinationalCircuits.ALUControl((False,False),BoolArray("C0",11))
      self.assertTrue(not c["F0"] and c["F1"] and c["ENA"] and not c["ENB"] and not c["INVA"] and
            not c["INCA"] and c["SL"] and not c["SR"] and c["amt"]==3 )

   def test_ALUcontrol_shiftright(self):
      # ALUop (F,F),  funct = x02  SR
      c = CombinationalCircuits.ALUControl((False,False),BoolArray("C2",11))
      self.assertTrue(not c["F0"] and c["F1"] and c["ENA"] and not c["ENB"] and not c["INVA"] and
            not c["INCA"] and not c["SL"] and c["SR"] and c["amt"]==3)

   def test_ALUcontrol_f20(self):
      # ALUop (F,F),  funct = x20 plus
      c = CombinationalCircuits.ALUControl((False,False),BoolArray("20",11))
      self.assertTrue(c["F0"] and c["F1"] and c["ENA"] and c["ENB"] and not c["INVA"] and
            not c["INCA"] and not c["SL"] and not c["SR"] and c["amt"]==0 )

   def test_ALUcontrol_f22(self):
      # ALUop (F,F),  funct = x22 minus
      c = CombinationalCircuits.ALUControl((False,False),BoolArray("22",11))
      self.assertTrue(c["F0"] and c["F1"] and c["ENA"] and c["ENB"] and c["INVA"] and
            c["INCA"] and not c["SL"] and not c["SR"] and c["amt"]==0 )

   def test_ALUControl_f24(self):
      # ALUop (F,F),  funct = x24 and
      c = CombinationalCircuits.ALUControl((False,False),BoolArray("24",11))
      self.assertTrue(not c["F0"] and not c["F1"] and c["ENA"] and c["ENB"] and not c["INVA"] and
            not c["INCA"] and not c["SL"] and not c["SR"] and c["amt"]==0 )
   def test_ALUcontrol_25(self):
      # ALUop (F,F),  funct = x25  or
      c = CombinationalCircuits.ALUControl((False,False),BoolArray("25",11))
      self.assertTrue(not c["F0"] and c["F1"] and c["ENA"] and c["ENB"] and not c["INVA"] and
            not c["INCA"] and not c["SL"] and not c["SR"] and c["amt"]==0 )


if __name__ == "__main__":
    unittest.main()
