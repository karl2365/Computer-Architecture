"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, file):
        """Construct a new CPU."""
        self.LDI = 0b10000010
        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.program_filename = file



    def load(self):
        """Load a program into memory."""
        address = 0

        with open(self.program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                line = int(line, 2)
                self.ram[address] = line

                address += 1

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
        #     self.ram[address] = instruction #instruction
        #     # print(self.ram[address])
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

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
        pc = 0 
        running = True
        # print(self.ram)
        while running:
            inst = self.ram[pc]

            if inst == self.LDI:
                self.reg[self.ram[pc+1]] = self.ram[pc+2]
                # print(self.reg[pc+1])
                pc += 3

            elif inst == self.PRN:
                reg_num = self.ram[pc + 1]
                # print(reg_num)
                print(self.reg[reg_num])
                pc += 2

            elif inst == self.MUL:
                reg_a = self.ram[pc+1]
                reg_b = self.ram[pc+2]
                self.alu('MUL', reg_a, reg_b)
                print(reg_a) 
                pc += 3

            elif inst == self.HLT:
                running = False

            else:
                print(inst)
                print('instruction not found')
                running = False


