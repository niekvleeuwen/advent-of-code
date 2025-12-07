class Computer:
    """Represents a simple Computer."""

    def __init__(self) -> None:
        self.output = []
        self.instruction_pointer = 0

        with open("dag_17/sample.txt") as f:
            registers, instructions = f.read().split("\n\n")

        registers = registers.splitlines()
        self.register_a = int(registers[0].lstrip("Register A: "))
        self.register_b = int(registers[1].lstrip("Register B: "))
        self.register_c = int(registers[2].lstrip("Register C: "))

        self.instructions = [int(ins) for ins in instructions.lstrip("Program: ").split(",")]

    def execute(self) -> None:  # noqa: C901
        """Execute the instructions."""
        while self.instruction_pointer < len(self.instructions):
            opcode = self.instructions[self.instruction_pointer]
            operand = self.instructions[self.instruction_pointer + 1]
            combo_operand = None

            match operand:
                case 4:
                    combo_operand = self.register_a
                case 5:
                    combo_operand = self.register_b
                case 6:
                    combo_operand = self.register_c
                case 7:
                    combo_operand = 0
                case _:
                    combo_operand = operand

            match opcode:
                # adv
                case 0:
                    denominator = 2**combo_operand
                    self.register_a = int(self.register_a / denominator)
                # bxl
                case 1:
                    self.register_b = self.register_b ^ operand
                # bst
                case 2:
                    self.register_b = int(combo_operand % 8)
                # jnz
                case 3:
                    if self.register_a != 0:
                        self.instruction_pointer = operand
                        continue
                # bxc
                case 4:
                    self.register_b = self.register_b ^ self.register_c
                # out
                case 5:
                    self.output.append(int(combo_operand % 8))
                # bdv
                case 6:
                    denominator = 2**combo_operand
                    self.register_b = int(self.register_a / (denominator))
                # cdv
                case 7:
                    denominator = 2**combo_operand
                    self.register_c = int(self.register_a / (denominator))

            self.instruction_pointer += 2

        print(",".join(str(x) for x in self.output))


def main() -> None:
    """Main function for day 16."""
    Computer().execute()


if __name__ == "__main__":
    main()
