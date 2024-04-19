fn = open("output.txt","w")
fn.close()

def Imm(n,b):
    if n >= 0:
        binary = bin(n)[2:]
    else:
        binary = bin(n & int("1" * (n.bit_length() + 1), 2))[2:]

    if len(binary) < b:
        if n >= 0:
            binary = '0' * (b - len(binary)) + binary
        else:                                                                       
            binary = '1' * (b - len(binary)) + binary
    elif len(binary) > b:
        binary = binary[-b:]

    return binary

def sign_ext(bits, num_bits):
    if len(bits) >= num_bits:
        return bits
    if bits[0] == '0':
        return '0' * (num_bits - len(bits)) + bits
    return '1' * (num_bits - len(bits)) + bits

nums = list()
largest_with_one = 65536
for x in range(32):
     nums.append(largest_with_one)
     largest_with_one = largest_with_one + 4
mem =dict.fromkeys(nums,0)

def bin_bits(num, num_bits):
    n="0b"+Imm(num,num_bits)
    return n
def hex_bits(num):
     n="0x000"+hex(num)[2:]
     return n
def binary_to_int(binary_string):
    return int(binary_string, 2)

def complement_to_decimal(binary):
    if binary[0] == '1':
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary)
        decimal_value = -(int(inverted_binary, 2) + 1)
    else:
        decimal_value = int(binary, 2)
    return decimal_value

register_encoding = {
    "x0": "00000",
    "zero": "00000",
    "r0": "00000",
    "x1": "00001",
    "ra": "00001",
    "r1": "00001",
    "x2": "00010",
    "sp": "00010",
    
    
    
    "r2": "00010",
    "x3": "00011",
    "gp": "00011",
    "r3": "00011",
    "x4": "00100",
    "tp": "00100",
    "r4": "00100",
    "x5": "00101",
    "t0": "00101",
    "r5": "00101",
    "x6": "00110",
    "t1": "00110",
    "r6": "00110",
    "x7": "00111",
    "t2": "00111",
    "r6": "00111",
    "x8":"01000",
    "r8":"01000",
    "s0":"01000",
    "fp":"01000",
    "x9":"01001",
    "r9":"01001",
    "s1":"01001",
    "r10": "01010",
    "x10":"01010",
    "a0":"01010",
    "x11": "01011",
    "a1": "01011",
    "r11": "01011",
    "x12": "01100",
    "a2": "01100",
    "r12": "01100",
    "x13": "01101",
    "a3": "01101",
    "r13": "01101",
    "x14": "01110",
    "a4": "01110",
    "r14": "01110",
    "x15": "01111",
    "a5": "01111",
    "r15": "01111",
    "x16": "10000",
    "a6": "10000",
    "r16": "10000",
    "x17": "10001",
    "a7": "10001",
    "x17": "10001",
    "x18": "10010",
    "s2": "10010",
    "r18": "10010",
    "x19": "10011",
    "s3": "10011",
    "r19": "10011",
    "x20": "10100",
    "s4": "10100",
    "r20": "10100",
    "x21": "10101",
    "s5": "10101",
    "r21": "10101",
    "x22": "10110",
    "s6": "10110",
    "r22": "10110",
    "x23": "10111",
    "s7": "10111",
    "r23": "10111",
    "x24": "11000",
    "s8": "11000",
    "r24": "11000",
    "x25": "11001",
    "s9": "11001",
    "r25": "11001",
    "x26": "11010",
    "s10": "11010",
    "r26": "11010",
    "x27": "11011",
    "s11": "11011",
    "r27": "11011",
    "x28": "11100",
    "t3": "11100",
    "r28": "11100",
    "x29": "11101",
    "t4": "11101",
    "r29": "11101",
    "x30": "11110",
    "t5": "11110",
    "r30": "11110",
    "x31": "11111",
    "t6": "11111",
    "r31": "11111"
}


#reg values 
r_v={
    "00000":0,
    "00001":0,
    "00010":256,
    "00011":0,
    "00100":0,
    "00101":0,
    "00110":0,
    "00111":0,
    "01000":0,
    "01001":0,
    "01010":0,
    "01011":0,
    "01100":0,
    "01101":0,
    "01110":0,
    "01111":0,
    "10000":0,
    "10001":0,
    "10010":0,
    "10011":0,
    "10100":0,
    "10101":0,
    "10110":0,
    "10111":0,
    "11000":0,
    "11001":0,
    "11010":0,
    "11011":0,
    "11100":0,
    "11101":0,
    "11110":0,
    "11111":0
}

def sll(rs1,rs2):

    amount = binary_to_int(rs2)
    r = rs1 << amount
    return r

def srl(rs1,rs2):

    amount = binary_to_int(rs2)
    r = rs1 >> amount
    return r


def Rtype(line,output,pc):
    print("Enetring r type: ")
    if line[17:20]=="000":
        if line[0:7]=="0000000":                 
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            print(r_v[sreg1],r_v[sreg2])
            r_v[dreg]=r_v[sreg1]+r_v[sreg2]
            return pc[0]+4

        elif line[0:7]=="0100000":             
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25] 
            r_v[dreg]=r_v[sreg1]-r_v[sreg2]
            return pc[0]+4

    elif line[17:20]=="001":
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            r_v[dreg]=sll(r_v[sreg1],r_v[sreg2])
            return pc[0]+4
    elif line[17:20]=="010":
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            print(sreg1)
            print(sreg2)
            print(dreg)
            print(r_v[sreg1])
            print(r_v[sreg2])
            if(r_v[sreg1])<(r_v[sreg2]):
                r_v[dreg]=1
            return pc[0]+4

    elif line[17:20]=="011":
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            if(r_v[sreg1]<r_v[sreg2]):
                r_v[dreg]=1
            return pc[0]+4
    elif line[17:20]=="100":
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            r_v[dreg]=r_v[sreg1]^r_v[sreg2]
            return pc[0]+4

    elif line[17:20]=="101":
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            r_v[dreg]=srl(r_v[sreg1],r_v[sreg2])
            return pc[0]+4
    elif line[17:20]=="110":
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            r_v[dreg]=r_v[sreg1]|r_v[sreg2]
            return pc[0]+4
    elif line[17:20]=="111":
            sreg1=line[12:17]
            sreg2=line[7:12]
            dreg=line[20:25]
            r_v[dreg]=r_v[sreg1]&r_v[sreg2]
            return pc[0]+4


def Btype(line, output, pc):
    print("Entering b type: ")
    imm = line[0] + line[24] + line[1:7] + line[20:24]+"0"
    func = line[17:20]
    rs1 = line[12:17]
    rs2 = line[7:12]
    print(r_v[rs1])
    print(r_v[rs2])
    print(func)
    print(complement_to_decimal(imm))
    if func == "000":
        if (r_v[rs1] == r_v[rs2]):
            return pc[0] + complement_to_decimal(imm)
    elif func == "001":
        if r_v[rs1] != r_v[rs2]:
            return pc[0] + complement_to_decimal(imm)
    elif func == "100":
        if r_v[rs1] < r_v[rs2]:
            return pc[0] + complement_to_decimal(imm)
    elif func == "101":
        if r_v[rs1] >= r_v[rs2]:
            return pc[0] + complement_to_decimal(imm)
    elif func == "110":
        if r_v[rs1] < r_v[rs2]:
            return pc[0] + complement_to_decimal(imm)
    elif func == "111":
        if r_v[rs1] >= r_v[rs2]:
            return pc[0] + complement_to_decimal(imm)
    return pc[0] + 4


        
def Jtype(line,output,pc):
    print("Entering j type: ")
    imm = line[0]+line[-20:-12]+line[-21]+line[-31:-21]
    rd=line[20:25]
    print(pc[0])
    r_v[rd]=pc[0]+4
    imm1=imm+"0"
    imm12=sign_ext(imm1,32)
    print(imm12)
    val=complement_to_decimal(imm12)
    print(val)
    pc[0]=pc[0]+val
    print(pc)
    return pc[0]


def Utype(line,output,pc):
    imm=line[0:20]+"000000000000"
    print(imm)
    print(complement_to_decimal(imm))
    rsd=line[20:25]
    print(rsd)
    print(r_v[rsd])
    print(pc[0])
    print("Entering U type: ")
    if(line[25:32]=="0110111"):
          r_v[rsd]=complement_to_decimal((imm))
    elif(line[25:32]=="0010111"):
          r_v[rsd]=pc[0]+complement_to_decimal((imm))
          print(pc[0])
          print(complement_to_decimal((imm)))
          print(r_v[rsd])
    return pc[0]+4


def Itype(line,output,pc):
    print("Going to I: ")
    op_code = line[-7:]
    rd = line[-12:-7]
    func = line[-15:-12]
    rs = line[-20:-15]
    imm = complement_to_decimal(line[-32:-20])
    print(imm)
    print(r_v[rd])
    ans = pc[0]
    if op_code == "0000011":
        r_v[rd]= mem[r_v[rs]+imm]
        ans = pc[0]+4
    if op_code == "0010011" and func == "000":
        r_v[rd]=r_v[rs]+imm
        ans = pc[0]+4
    if op_code == "0010011" and func == "011":
        if abs(r_v[rs])<abs(imm):
            r_v[rd]=1
            ans=pc[0] + 4
        else:
            ans = pc[0]+4
    if op_code == "1100111" :
        r_v[rd] = pc[0] +4
        ans=r_v[rs]+imm
    return ans
             
          
def Stype(line,output,pc):
     imm=line[0:7]+line[20:25]
     immd=complement_to_decimal((imm))
     rs1=line[12:17]
     rs2=line[7:12]
     print(rs1)
     print(rs2)
     print(immd)
     print(pc[0])
     val=r_v[rs1]+immd
     mem[val]=r_v[rs2]
     print(r_v[rs2])
     return pc[0]+4

 
def intruc(line,output,pc):
    print("Going to Instruction:- ")
    op = line[-7:]
    if op == "0110011":
        ans = Rtype(line,output,pc)
    elif op == "0000011" or op == "1100111" or op == "0010011":
        ans = Itype(line,output,pc)
    elif op == "0100011":
        ans = Stype(line,output,pc)
    elif op == "1100011":
        ans = Btype(line,output,pc)
    elif op == "0110111" or op== "0010111":
        ans = Utype(line,output,pc)
    elif op == "1101111":
        ans = Jtype(line,output,pc)
    r_v["00000"]=0
    return ans


ip=[]
with open("input.txt", 'r') as file:
    ip = [line.strip() for line in file]
final = dict()
for i in range(len(ip)):
    final[(i)*4] = ip[i]
pc = [0]
op=[]
while True :
    print(pc , " ")
    if (final[pc[0]]=="00000000000000000000000001100011") :
        break
    x=final[pc[0]]
    pc[0] = intruc(x,op,pc)
    optemp=bin_bits(pc[0],32)+" "+bin_bits(r_v["00000"],32)+" "+bin_bits(r_v["00001"],32)+" "+bin_bits(r_v["00010"],32)+" "+bin_bits(r_v["00011"],32)+" "+bin_bits(r_v["00100"],32)+" "+bin_bits(r_v["00101"],32)+" "+bin_bits(r_v["00110"],32)+" "+bin_bits(r_v["00111"],32)+" "+bin_bits(r_v["01000"],32)+" "+bin_bits(r_v["01001"],32)+" "+bin_bits(r_v["01010"],32)+" "+bin_bits(r_v["01011"],32)+" "+bin_bits(r_v["01100"],32)+" "+bin_bits(r_v["01101"],32)+" "+bin_bits(r_v["01110"],32)+" "+bin_bits(r_v["01111"],32)+" "+bin_bits(r_v["10000"],32)+" "+bin_bits(r_v["10001"],32)+" "+bin_bits(r_v["10010"],32)+" "+bin_bits(r_v["10011"],32)+" "+bin_bits(r_v["10100"],32)+" "+bin_bits(r_v["10101"],32)+" "+bin_bits(r_v["10110"],32)+" "+bin_bits(r_v["10111"],32)+" "+bin_bits(r_v["11000"],32)+" "+bin_bits(r_v["11001"],32)+" "+bin_bits(r_v["11010"],32)+" "+bin_bits(r_v["11011"],32)+" "+bin_bits(r_v["11100"],32)+" "+bin_bits(r_v["11101"],32)+" "+bin_bits(r_v["11110"],32)+" "+bin_bits(r_v["11111"],32)+" "+"\n"
    op.append(optemp)
f1 = open("output.txt","a")
f1.writelines(op)
f1.write(optemp)
memory = []
for i in range(65536,65664,4):
     no = hex_bits(i)+":"+bin_bits(mem[i],32)+"\n"
     memory.append(no)
print(mem)
f1.writelines(memory)
f1.close()
