def execute_instruction(instruction, registers, pc, memory):
    opcode = instruction & 0b1111111

    print(f"Executing instruction: {instruction}")
    print(f"PC: {pc}")

    if opcode == 0b0110011:  # R-Type
        funct3 = (instruction >> 12) & 0b111
        funct7 = (instruction >> 25) & 0b1111111
        rd = (instruction >> 7) & 0b11111
        rs1 = (instruction >> 15) & 0b11111
        rs2 = (instruction >> 20) & 0b11111

        print(f"R-Type Instruction: funct3={funct3}, funct7={funct7}, rd={rd}, rs1={rs1}, rs2={rs2}")

        if funct3 == 0b000 and funct7 == 0b0000000:  # ADD
            registers[rd] = registers[rs1] + registers[rs2]
        elif funct3 == 0b000 and funct7 == 0b0100000:  # SUB
            registers[rd] = registers[rs1] - registers[rs2]
        elif funct3 == 0b010:  # SLT
            registers[rd] = 1 if registers[rs1] < registers[rs2] else 0
        elif funct3 == 0b011:  # SLTU
            registers[rd] = 1 if registers[rs1] < registers[rs2] else 0
        elif funct3 == 0b100:  # XOR
            registers[rd] = registers[rs1] ^ registers[rs2]
        elif funct3 == 0b001 and funct7 == 0b0000000:  # SLL
            registers[rd] = registers[rs1] << (registers[rs2] & 0b11111)
        elif funct3 == 0b101 and funct7 == 0b0000000:  # SRL
            registers[rd] = registers[rs1] >> (registers[rs2] & 0b11111)
        elif funct3 == 0b110 and funct7 == 0b0000000:  # OR
            registers[rd] = registers[rs1] | registers[rs2]
        elif funct3 == 0b111 and funct7 == 0b0000000:  # AND
            registers[rd] = registers[rs1] & registers[rs2]

    elif opcode in [0b0010011, 0b0000011, 0b1100111, 0b0001111]:  # I-Type
        rd = (instruction >> 7) & 0b11111
        funct3 = (instruction >> 12) & 0b111
        rs1 = (instruction >> 15) & 0b11111
        imm = (instruction >> 20)

        print(f"I-Type Instruction: funct3={funct3}, rd={rd}, rs1={rs1}, imm={imm}")

        if opcode == 0b0010011:  # ADDI
            registers[rd] = registers[rs1] + imm
        elif opcode == 0b0000011:  # LW
            address = registers[rs1] + imm
            registers[rd] = int.from_bytes(memory[address:address + 4], byteorder='little', signed=False)
        elif opcode == 0b1100111:  # JALR
            registers[rd] = pc + 4
            pc = (registers[rs1] + imm) & (~1)
            print(f"Jumping to address: {pc}")
            return pc, registers
        elif opcode == 0b0010011 and funct3 == 0b011:  # SLTIU
            registers[rd] = 1 if registers[rs1] < imm else 0

    elif opcode == 0b0100011:  # S-Type
        funct3 = (instruction >> 12) & 0b111
        rs1 = (instruction >> 15) & 0b11111
        rs2 = (instruction >> 20) & 0b11111
        imm = ((instruction >> 7) & 0b11111) | ((instruction >> 25) & 0b111111100000)

        print(f"S-Type Instruction: funct3={funct3}, rs1={rs1}, rs2={rs2}, imm={imm}")

        if funct3 == 0b000:  # SW
            address = registers[rs1] + imm
            memory[address:address + 4] = int(registers[rs2]).to_bytes(4, byteorder='little', signed=False)

    elif opcode == 0b1100011:  # B-Type
        funct3 = (instruction >> 12) & 0b111
        rs1 = (instruction >> 15) & 0b11111
        rs2 = (instruction >> 20) & 0b11111
        imm = ((instruction >> 7) & 0b11111) | ((instruction >> 25) & 0b111111100000)

        print(f"B-Type Instruction: funct3={funct3}, rs1={rs1}, rs2={rs2}, imm={imm}")

        if funct3 == 0b000:  # BEQ
            if registers[rs1] == registers[rs2]:
                pc += imm - 4  # -4 because PC will increment by 4 after this instruction
        elif funct3 == 0b001:  # BNE
            if registers[rs1] != registers[rs2]:
                pc += imm - 4
        elif funct3 == 0b101:  # BGEU
            if registers[rs1] >= registers[rs2]:
                pc += imm - 4
        elif funct3 == 0b100:  # BLT
            if registers[rs1] < registers[rs2]:
                pc += imm - 4
        elif funct3 == 0b110:  # BLTU
            if registers[rs1] < registers[rs2]:
                pc += imm - 4

    elif opcode in [0b0110111, 0b0010111]:  # U-Type
        rd = (instruction >> 7) & 0b11111
        imm = instruction >> 12
        print(f"U-Type Instruction: rd={rd}, imm={imm}")
        if opcode == 0b0110111:  # AUIPC
            registers[rd] = pc + imm
        elif opcode == 0b0010111:  # LUI
            registers[rd] = imm << 12

    elif opcode == 0b1101111:  # J-Type
        rd = (instruction >> 7) & 0b11111
        imm = ((instruction >> 21) & 0b1111111111) | ((instruction >> 20) & 1 << 10) | ((instruction >> 12) & 0b11111111) | ((instruction >> 31) & 1 << 20)
        registers[rd] = pc + 4
        pc += imm
        print(f"J-Type Instruction: rd={rd}, imm={imm}")

    pc += 4
    print(f"Updated PC: {pc}")
    return pc, registers


def run_program(program):
    registers = [0] * 32
    pc = 0
    memory = [0] * (32 * 4)  # 32 registers * 4 bytes/register

    while True:
        instruction = (program[pc >> 2] >> ((pc & 0b11) * 8)) & 0xFFFFFFFF
        if instruction == 0b00000000000000000000000001100011:  # Virtual Halt instruction
            break
        pc, registers = execute_instruction(instruction, registers, pc, memory)

    return registers, memory


def print_registers(registers):
    register_values = " ".join([str(reg) for reg in registers])
    print(f"Registers: {register_values}")
def print_memory(memory):
    for i in range(0, len(memory), 4):
        print(format(int.from_bytes(memory[i:i + 4], byteorder='little', signed=False), '032b'))


def main():
    # Load your binary program here
    program = [0b00000000000000000000010010110011,
0b00000000000000000000100100110011,
0b00000000000100000000010010010011,
0b00000001000000000000100100010011,
0b00000001001001001001010010110011,
0b00000000101100000000101010010011,
0b00000001010101001010000000100011,
0b00000000000001001010100100000011,
0b00000000010001001000010010010011,
0b00000000000100000000100110010011,
0b00000001001110010111100100110011,
0b00000001001000000000100001100011,
0b00000000001100000000101000010011,
0b00000001010001001010000000100011,
0b00000000000000000000000001100011,
0b00000000001000000000101000010011,
0b00000001010001001010000000100011,
0b00000000000000000000000001100011]  # Virtual Halt instruction
    registers, memory = run_program(program)
    print_registers(registers)
    print_memory(memory)


if __name__ == "__main__":
    main()
