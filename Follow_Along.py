# import sys

# PRINT_ETHAN = 1
# HALT = 2
# SAVE_REGISTER = 3  # save a value in a register,
# # needs to tell it what register to save it and the data we're saving
# PRINT_REGISTER = 4
# memory = [
#     PRINT_ETHAN,
#     SAVE_REGISTER,
#     0,
#     37,
#     PRINT_REGISTER,
#     SAVE_REGISTER,
#     1,
#     12,
#     PRINT_REGISTER,
#     PRINT_ETHAN,
#     HALT
# ]

# registers = [0, 0, 0, 0, 0, 0, 0, 0]  # Like variables, named R0-R7

# halted = False
# pc = 0  # "Program Counter": Index into the memory array, AKA "pointer", "address", "location"
# while not halted:
#     instruction = memory[pc]

#     if instruction == PRINT_ETHAN:
#         print('Ethan!')
#         pc += 1
#     elif instruction == HALT:
#         halted = True
#     elif instruction == SAVE_REGISTER:
#         reg_num = memory[pc + 1]
#         value = memory[pc + 2]

#         registers[reg_num] = value

#         pc += 3
#     elif instruction == PRINT_REGISTER:
#         print(registers[reg_num])

#         pc += 1
#     else:
#         print(f"Unknown instruction {instruction} at address {pc}")
#         sys.exit(1)
