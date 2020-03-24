"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = 8 * [0]
        self.ram = 256 * [0]
        self.pc = 0 
        self.running = True 
        self.opcodes = {
            "NOP":  0b00000000,
            "LDI":  0b10000010,
            "PRN":  0b01000111,
            "ADD":  0b10100000,
            "MUL":  0b10100010,
            "HLT":  0b00000001,
            "PUSH": 0b01000101,
            "POP":  0b01000110,
            "CALL": 0b01010000,
            "RET":  0b00010001,
            "CMP":  0b10100111,
            "JMP":  0b01010100,
            "JEQ":  0b01010101,
            "JNE":  0b01010110,
        }
        self.branch_table = {}
        self.branch_table[self.opcodes['LDI']] = self.ldi
        self.branch_table[self.opcodes['PRN']] = self.prn
        self.branch_table[self.opcodes['HLT']] = self.hlt
        self.branch_table[self.opcodes['MUL']] = self.mul

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            with open(program) as program:
                for line in program:
                    line_split = line.split('#')
                    value = line_split[0].strip()
                    
                    if value == "":
                        continue
                    formatted_value = int(value, 2)
                    
                    self.ram[address] = formatted_value
                    address += 1
        except FileNotFoundError:
            print(f"{program} not found")
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        # elif op == "DEC":
        #     self.reg[reg_a] -= 1
        # elif op == "INC":
        #     self.reg[reg_a] += 1
        # elif op == "ADDI":
        #     self.reg[reg_a] += reg_b
        # elif op == "SUB":
        #     self.reg[reg_a] -= self.reg[reg_b]
        # elif op == "MUL":
        #     self.reg[reg_a] *= self.reg[reg_b]
        # elif op == "DIV":
        #     self.reg[reg_a] //= self.reg[reg_b]
        # elif op == "MOD":
        #     self.reg[reg_a] %= self.reg[reg_b]
        if op in self.opcodes:
            self.branch_table[self.opcodes[op]]()
        else:
            raise Exception("Unsupported ALU operation")
    
    def hlt(self):
        self.running = False
        sys.exit(0)

    def ldi(self):
        reg_idx = self.ram[self.pc+1]
        reg_val = self.ram[self.pc+2]
        self.reg[reg_idx] = reg_val

    def prn(self):
        reg_idx = self.ram[self.pc+1]
        print(self.reg[reg_idx])

    def mul(self):
        self.reg[self.ram[self.pc+1]] *= self.reg[self.ram[self.pc+2]]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            instruction = self.ram_read(self.pc)
            
            self.branch_table[instruction]()
            
            self.pc += (instruction >> 6) + 1
