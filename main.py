from ram import RAM


program = open("program.ram", "r").read()
ram = RAM(program)

data = 7

ram.execute_program(data)

print(data**3 + 2 * data**2 + 5)



