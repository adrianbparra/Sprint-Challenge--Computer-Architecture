"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = True
        self.pc = 0
        self.fl = 0b00000000
        self.reg[7] = 0xF4
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.ADD = 0b10100000
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110
        self.branchtable = {}
        self.branchtable[self.LDI] = self.handle_LDI
        self.branchtable[self.PRN] = self.handle_PRN
        self.branchtable[self.HLT] = self.handle_HLT
        self.branchtable[self.MUL] = self.handle_MUL
        self.branchtable[self.ADD] = self.handle_ADD
        self.branchtable[self.PUSH] = self.handle_PUSH
        self.branchtable[self.POP] = self.handle_POP
        self.branchtable[self.CALL] = self.handle_CALL
        self.branchtable[self.RET] = self.handle_RET
        self.branchtable[self.JMP] = self.handle_JMP
        self.branchtable[self.CMP] = self.handle_CMP
        self.branchtable[self.JEQ] = self.handle_JEQ
        self.branchtable[self.JNE] = self.handle_JNE

    def load(self):
        """Load a program into memory."""


        # For now, we've just hardcoded a program:

        try:
            if len(sys.argv) < 2:
                print(f'Usage: python3 {sys.argv[0]} <filename>')
                print("Exiting Program")
                sys.exit(1)
            
            address = 0
            
            with open(f"C:\\Users\\PC1\\Documents\\Lambda_School\\Computer_Architecture\\Sprint-Challenge--Computer-Architecture\\{sys.argv[1]}.ls8") as f:
                print(f"Running file '{sys.argv[1]}.ls8'")
                print("--------------------------------")

                for line in f:
                    split_line = line.split("#")[0]
                    stripped_line = split_line.strip()
                    if stripped_line != "":
                        command = int(stripped_line, 2)

                        # print(command)

                        self.ram[address] = command
                        address += 1

        except FileNotFoundError:

            print(f"Error file '{sys.argv[1]}' not found")
            print("Exiting Program")
            sys.exit(1)
            

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # handles CMP
        elif op == "CMP":
            # fl = 00000LGE
            # print("REG A:", self.reg[reg_a])
            # print("REG B:", self.reg[reg_b])
            a = self.reg[reg_a]
            b = self.reg[reg_b]
            if a == b:
            # Equal = a == b
                self.fl = 0b00000001
            elif a > b:
            # Greater = a > b
                self.fl = 0b00000010
            else:
            # Less = a < b
                self.fl = 0b00000100
            
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | RAM: %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='REG:')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self,address):
        
        return self.ram[address]

    def ram_write(self,value,address):
        
        self.ram[address] = value

    def handle_LDI(self):
        
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        # print("LDI: ",int(value))

        self.reg[address] = value

        self.pc += 2

    def handle_PRN(self):

        address = self.ram_read(self.pc + 1)

        print(self.reg[address])

        self.pc += 1

    def handle_MUL(self):
        
        registerA = self.ram_read(self.pc + 1)
        registerB = self.ram_read(self.pc + 2)

        self.alu("MUL", registerA, registerB)

        self.pc += 2

    def handle_ADD(self):

        registerA = self.ram_read(self.pc + 1)
        registerB = self.ram_read(self.pc + 2)

        self.alu("ADD", registerA, registerB)
        
        self.pc += 2
    
    def handle_CMP(self):

        registerA = self.ram_read(self.pc + 1)
        registerB = self.ram_read(self.pc + 2)

        self.alu("CMP", registerA, registerB)

        self.pc += 2
        
    def handle_JEQ(self):
        # jump if equal flag is set to true
        # jump to address stored in givin register
        if self.fl == 0b1:
            # get register_address from ram
            register_address = self.ram_read(self.pc + 1)
            # get new pc from register
            new_pc = self.reg[register_address]
            # set pc to new address
            # has to be decremented since run fuction add one
            self.pc = new_pc - 1
        else:
            # increment pc to skip register address
            self.pc += 1

    def handle_JNE(self):
        # if "E" flag is false jump to address stored in given register
        if self.fl != 0b1:
            # if it was less or eqal this would fail there for can not be equal
            # get register_address from ram
            register_address = self.ram_read(self.pc + 1)
            # get new pc from register
            new_pc = self.reg[register_address]
            # set pc to new address
            # has to be decremented since run fuction add one
            self.pc = new_pc - 1

        else:
            self.pc += 1

    def handle_PUSH(self):
        self.reg[7] -= 1

        address = self.ram_read(self.pc+1)

        value = self.reg[address]

        self.ram_write(value, self.reg[7])

        self.pc += 1

    def handle_POP(self):

        value = self.ram_read(self.reg[7])


        address = self.ram_read(self.pc + 1)

        self.reg[address] = value
        
        self.reg[7] += 1
        self.pc += 1
    def handle_CALL(self):
    # calls a subroutine at address stored in register
        # save next address to stack
        next_command = self.pc + 2

        self.reg[7] -= 1

        self.ram_write(next_command, self.reg[7])
        # print(f"save: {self.pc+2} to ram: {stack_address}")
        # print(self.ram)

        # address to save
        register_number = self.ram_read(self.pc + 1)

        address_jump = self.reg[register_number]
        # print("Address :", address_jump)

        # pc is set to address stored in register
        self.pc = address_jump - 1
        # print(f"save pc to {self.reg[address]}")
 
    def handle_RET(self):
        # get saved pc in reg
        stack_pointer = self.reg[7]
        saved_pc =  self.ram_read(stack_pointer)
        # print("Return: ", int(saved_pc))
        
        # increment stack
        self.reg[7] += 1
        # save address to pc
        self.pc = saved_pc - 1
    
    def handle_JMP(self):
        # Jump to address stored in given register
        # get register from ram
        register_address = self.ram_read(self.pc + 1)
        # get new pc from register
        new_pc = self.reg[register_address]
        # set the PC to address
        # one si subtracted since the run function adds one
        self.pc = new_pc - 1
        pass

    def handle_HLT(self):

        self.running = False

    def run(self):
        """Run the CPU."""
        
        while self.running:
            # self.trace()
            # print("Command I: ",int(self.pc))
            
            command = self.ram[self.pc]
            
            if command in self.branchtable:


                self.branchtable[command]()
            else:
                print(f"Error: {bin(command)} not Found at pc:{self.pc}")
            

            self.pc += 1