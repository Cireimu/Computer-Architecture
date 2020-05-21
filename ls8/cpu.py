import sys
program = []


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # create ram with 256 bytes of memory
        self.reg = [0] * 8  # general registry with 8 slots
        self.pc = 0
        self.instructions = {
            "LDI": 0b10000010,
            "HLT": 0b00000001,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "ADD": 0b10100000,
            "SUB": 0b10100001,
            "POP": 0b01000110,
            "PUSH": 0b01000101,
            "CALL": 0b01010000,
            "RET": 0b00010001
        }
        self.SP = 7
        self.reg[7] = 0xf4

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) > 1:
            program_file = sys.argv[1]
            with open(program_file) as f:
                for line in f:
                    line = line.split('#')
                    line = line[0].strip()
                    if line == '':
                        continue
                    line = int(line, 2)
                    program.append(line)
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, ma):  # ma = Memory Access
        return self.ram[ma]

    def ram_write(self, ma, v):  # v = value
        self.ram[ma] = v

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.instructions["HLT"]:
                running = False
                self.pc += 1

            elif ir == self.instructions["LDI"]:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == self.instructions["PRN"]:
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == self.instructions["MUL"]:
                self.alu("MUL", operand_a, operand_b)
            elif ir == self.instructions["ADD"]:
                self.alu("ADD", operand_a, operand_b)
            elif ir == self.instructions["SUB"]:
                self.alu("SUB", operand_a, operand_b)

            elif ir == self.instructions["PUSH"]:
                # decrement the stack pointer
                self.reg[self.SP] -= 1
                # copy the value from register into memory
                reg_num = self.ram[self.pc+1]
                value = self.reg[reg_num]  # this is what should be pushed
                address = self.reg[self.SP]
                # store the value on the stack
                self.ram[address] = value
                self.pc += 2
            elif ir == self.instructions["POP"]:
                # copy the value from the address pointed to by 'SP', to the given register
                value = self.ram_read(self.reg[self.SP])
                self.reg[operand_a] = value
                # increment the stack pointer
                self.reg[self.SP] += 1
                self.pc += 2
            elif ir == self.instructions["CALL"]:
                ret_add = self.pc + 2
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = ret_add
                reg_num = self.ram[self.pc + 1]
                dest_add = self.reg[reg_num]

                self.pc = dest_add
            elif ir == self.instructions["RET"]:
                ret_add = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1

                self.pc = ret_add
            else:
                print("unknown instruction")
                running = False
