class Processor:
    def __init__(self):
        self.pc = 0
        self.registers = [0] * 32
        self.memory = [0] * (2**20)  # Assuming a memory size of 1MB

    def load_program(self, program):
        # Load the program into memory starting at address 0
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def fetch_instruction(self):
        # Fetch the instruction from memory at the current PC
        instruction = self.memory[self.pc]
        return instruction

    def rtype(self, ins):
        rd = ins[::-1][7:12][::-1]
        rs1 = ins[::-1][15:20][::-1]
        rs2 = ins[::-1][20:25][::-1]
        funct3 = ins[::-1][12:15][::-1]
        funct7 = ins[::-1][25:32][::-1]
   
        if funct3 == '000' and funct7 == '0000000':  # ADD
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] + self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '000' and funct7 == '0100000':  # SUB
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] - self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '111' and funct7 == '0000000':  # AND
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] & self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '110' and funct7 == '0000000':  # OR
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] | self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '100' and funct7 == '0000000':  # XOR
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] ^ self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '001'and funct7== '0000000': #SLL
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] << self.registers[self.bin_to_int(rs2, 0)]
        elif funct3 == '010' and funct7=='0000000':  # SLT
            self.registers[self.bin_to_int(rd, 0)] = 1 if self.registers[self.bin_to_int(rs1, 0)] < self.registers[self.bin_to_int(rs2, 0)] else 0
        elif funct3 == '011' and funct7=='0000000':  # SLTU
            self.registers[self.bin_to_int(rd, 0)] = 1 if self.registers[self.bin_to_int(rs1, 0)] < self.registers[self.bin_to_int(rs2, 0)] else 0
        elif funct3 == '101' and funct7 == '0000000':  # SRL
            self.registers[self.bin_to_int(rd, 0)] = self.registers[self.bin_to_int(rs1, 0)] >> self.registers[self.bin_to_int(rs2, 0)]
   
        self.pc += 1


    def itype(self, instruction):
        opcode = instruction[-7:]
        imm = instruction[::-1][20:32][::-1]
        imm_value = self.bin_to_int(imm, 1)  # Sign-extend the immediate value
   
        rd = self.bin_to_int(instruction[::-1][7:12][::-1], 0)
        rs1 = self.bin_to_int(instruction[::-1][15:20][::-1], 0)
        funct3 = instruction[::-1][12:15][::-1]
   
        match opcode:
            case '1100111':  # jalr
                self.registers[rd] = 4 * (self.pc + 1) + 4
                self.pc = (self.registers[rs1] + imm_value) // 4
   
            case '0010011':  # I-type instructions
                if funct3 == '011':  # sltiu
                    self.registers[rd] = 1 if self.registers[rs1] < imm_value else 0
                elif funct3 == '000':  # addi
                    self.registers[rd] = self.registers[rs1] + imm_value
   
        self.pc += 1

    def stype(self, ins):
        imm = ins[::-1][25:32][::-1] + ins[::-1][7:12][::-1]
        imm_value = self.bin_to_int(imm, 1)
        rs1 = ins[::-1][15:20][::-1]
        rs2 = ins[::-1][20:25][::-1]
        funct3 = ins[::-1][12:15][::-1]
        memadr = imm_value + self.registers[self.bin_to_int(rs1, 0)] - 16**4
        self.memory[memadr//4] = self.registers[self.bin_to_int(rs2, 0)]
        self.pc += 1


    def btype(self, instruction):
        opcode = instruction[-7:]
        imm = instruction[-31] + instruction[::-1][7:12][::-1] + instruction[-32:-25] + instruction[-20:-12] + instruction[-21] + '0'
        imm_value = self.bin_to_int(imm, 1)  # Sign-extend the immediate value
   
        rs1 = self.bin_to_int(instruction[::-1][15:20][::-1], 0)
        rs2 = self.bin_to_int(instruction[::-1][20:25][::-1], 0)
        funct3 = instruction[::-1][12:15][::-1]
   
        rs1_value = self.registers[rs1]
        rs2_value = self.registers[rs2]
   
        done = False
        match funct3:
            case '000':  # beq
                if rs1_value == rs2_value:
                    self.pc = self.pc + imm_value // 4
                    done = True
            case '001':  # bne
                if rs1_value != rs2_value:
                    self.pc = self.pc + imm_value // 4
                    done = True
            case '101':  # bge
                if rs1_value >= rs2_value:
                    self.pc = self.pc + imm_value // 4
                    done = True
            case '111':  # bgeu
                if signed_to_unsigned(rs1_value) >= signed_to_unsigned(rs2_value):
                    self.pc = self.pc + imm_value // 4
                    done = True
            case '110':  # bltu
                if signed_to_unsigned(rs1_value) < signed_to_unsigned(rs2_value):
                    self.pc = self.pc + imm_value // 4
                    done = True
            case '100':  # blt
                if rs1_value < rs2_value:
                    self.pc = self.pc + imm_value // 4
                    done = True
   
        if not done:
            self.pc += 1

    def utype(self, ins):
        opcode = ins[-7:]
        rd = ins[::-1][7:12][::-1]
        rdint = self.bin_to_int(rd, 0)
        imm = ins[::-1][12:32][::-1]
        if opcode == "0110111": # lui
            self.registers[rdint] = self.bin_to_int(imm + "0" * 12, 1)
        if opcode == "0010111": # auipc
            self.registers[rdint] = self.bin_to_int(imm + "0" * 12, 1) + 4 * self.pc
        self.pc += 1

    def jtype(self, instruction):
        rd = instruction[-12:-7]
        imm = "0" * 21
        imm[-21] = instruction[-32]
        imm[-11:-1] = instruction[-31:-21]
        imm[-12] = instruction[-21]
        imm[-20:-12] = instruction[-20:-12]

        self.registers[self.bin_to_int(rd, 0)] = 4 * self.pc + 4
        self.pc += self.bin_to_int(self.sext(self.int_to_bin(imm), 32)) // 4  # imm 0 bit is 0

    def bin_to_int(self, binary, signed):
        # Convert binary string to integer
        if signed and binary[0] == '1':
            return -((int(''.join('1' if x == '0' else '0' for x in binary), 2) + 1) & int('1' * len(binary), 2))
        return int(binary, 2)

    def int_to_bin(self, num):
        # Convert integer to binary string
        return bin(num)[2:]

    def sext(self, number, n):
        # Sign extend the number to the specified length
        binary = bin(int(number, 2))[2:]
        if binary[0] == '1':
            binary = '1' + binary[1:]
        return (binary + '0' * (n - len(binary)))[-n:]

    def finished(self):
        return self.pc >= len(self.memory) or self.memory[self.pc] == 0


def main():
    # Initialize your processor or emulator
    processor = Processor()

    # Load your program into memory
    program = ['00000000101001001000001010010011',
'11111110110010010011001100010011',
'00000001111010011000001110010011',
'11111101100010100011111000010011',
'00000011001010101000111010010011',
'11111100010010110011111100010011',
'00000100011010111000111111100111',
'11111011000010101011111110010011',
'00000000000000000000000001100011']
    processor.load_program(program)

    # Run the program
    while not processor.finished():
        # Fetch instruction from memory
        if processor.pc >= len(processor.memory):
            print("Error: Program Counter out of bounds")
            break
        instruction = processor.fetch_instruction()
        processor.pc += 1

        if instruction == 0:
            print("Error: Invalid instruction (zero)")
            break        

        # Decode and execute the instruction based on its type
        opcode = instruction[-7:]
        if opcode == '0110011':  # R-type
            processor.rtype(instruction)
        elif opcode == '0010011':  # I-type
            processor.itype(instruction)
        elif opcode == '0100011':  # S-type
            processor.stype(instruction)
        elif opcode == '1100011':  # B-type
            processor.btype(instruction)
        elif opcode == '0010111':  # U-type
            processor.utype(instruction)
        elif opcode =='1101111':  # J-type
            processor.jtype(instruction)

        # Print the current state after each instruction execution
        print("PC:", processor.pc)
        print("Registers:")
        for i, reg in enumerate(processor.registers):
            print(f"    x{i}: {reg}")
        print("Memory:")
        for i, mem in enumerate(processor.memory):
            if mem != 0:
                print(f"    {i}: {mem}")

    # After the program finishes, print the final state of registers and memory
    print("Final PC:", processor.pc)
    print("Final Registers:")
    for i, reg in enumerate(processor.registers):
        print(f"    x{i}: {reg}")
    print("Final Memory:")
    for i, mem in enumerate(processor.memory):
        if mem != 0:
            print(f"    {i}: {mem}")

if __name__ == "__main__":
    main()
