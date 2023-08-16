class RAM:
    def __init__(self, program) -> None:
        self.nmem = 32
        self.nreg = 32
        self.nbits = 32
        self.st, self.d = "start", 0
        self.state = [(self.st, self.d)]
        self.memory = [0] * self.nmem
        self.register = [0] * self.nreg
        self.cond = 0
        self.program_memory = self.program_memory = [" "] + program.splitlines()
        self.pc = 1
        self.comment_mark = "#"
        self.exec_line_total = 0
    def execute_program(self, data):
        with open("result.txt", "w") as f:
            f.write(f"Execution result : \n")
            f.close()
        self.register[1] = data
        while self.state[-1][0] != "stop":
            self.exec_line(self.program_memory[self.pc])
            self.exec_line_total += 1
        with open("result.txt", "a") as f:
            f.write(f"Output d : {self.d}\nTotal line execution : {self.exec_line_total}\n")
            f.close()
        with open("state.txt", "w") as f:
            for state in self.state:
                f.write(f"{state}\n")
            f.close()

    def exec_line(self, line: str):
        list_arg = line.split(" ")
        if list_arg[0] == self.comment_mark:
            self.pc += 1
        if len(list_arg) == 1:
            if list_arg[0] == "stop":
                self.st = "stop"
                self.state.append((self.st, self.d))
            if list_arg[0] == "reg":
                self.st = "reg"
                self.state.append((self.st, self.d))
                self.pc += 1
                with open("result.txt", "a") as f:
                    f.write(f"Register : {self.register}\n")
                    f.close()
            if list_arg[0] == "mem":
                self.st = "mem"
                self.state.append((self.st, self.d))
                self.pc += 1
                with open("result.txt", "a") as f:
                    f.write(f"Memory : {self.memory}\n")
                    f.close()
        if len(list_arg) == 2:
            if list_arg[0].lower() == "print":
                data = self.register[int(list_arg[1])]
                with open("result.txt", "a") as f:
                    f.write(f"Register {int(list_arg[1])} : {data}\n")
                    f.close()
                self.pc += 1
                self.st = "print"
                self.state.append((self.st, self.d))
            if list_arg[0].lower() == "jump":
                self.pc = int(list_arg[1])
                self.st = "jump"
                self.state.append((self.st, self.d))
            if list_arg[0].lower() == "jumpc":
                if self.cond == 1:
                    self.pc = int(list_arg[1])
                    self.st = "jumpc"
                    self.state.append((self.st, self.d))
                else:
                    self.pc += 1
                    self.state.append(("nop", self.d))
        if len(list_arg) == 3:
            if list_arg[0].lower() == "add":
                self.register[int(list_arg[1])] += self.register[int(list_arg[2])]
                self.register[int(list_arg[1])] %= 2**self.nbits
                self.st = "addi"
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "sub":
                self.register[int(list_arg[1])] -= self.register[int(list_arg[2])]
                self.register[int(list_arg[1])] %= 2**self.nbits
                self.st = "subi"
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "mul":
                self.register[int(list_arg[1])] *= self.register[int(list_arg[2])]
                self.register[int(list_arg[1])] %= 2**self.nbits
                self.st = "subi"
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "div":
                self.register[int(list_arg[1])] //= self.register[int(list_arg[2])]
                self.register[int(list_arg[1])] %= 2**self.nbits
                self.st = "subi"
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "mod":
                self.register[int(list_arg[1])] %= self.register[int(list_arg[2])]
                self.register[int(list_arg[1])] %= 2**self.nbits
                self.st = "subi"
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "store":
                k, l = int(list_arg[1]), int(list_arg[2])
                self.memory[l] = self.register[k]
                self.st = "write"
                self.d = self.memory[l]
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "storei":
                k, l = int(list_arg[1]), int(list_arg[2])
                self.memory[l] = k
                self.st = "write"
                self.d = self.memory[l]
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "load":
                k, l = int(list_arg[1]), int(list_arg[2])
                self.register[k] = self.memory[l]
                self.st = "read"
                self.d = self.memory[l]
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "loadi":
                k, l = int(list_arg[1]), int(list_arg[2])
                self.register[k] = l
                self.st = "read"
                self.d = l
                self.state.append((self.st, self.d))
                self.pc += 1
            if list_arg[0].lower() == "cond":
                r1, r2 = int(list_arg[0]), int(list_arg[1])
                self.cond = 1 if self.register[r1] == self.register[r2] else 0
                self.st = "cond"
                self.state.append((self.st, self.d))
                self.pc += 1