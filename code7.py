import core


class Code7:
    def __init__(self):
        self.memoryBackup = {k:v for k, v in core.memory.items()}
        self.registerBackup = [r for r in core.register]
        self.stackBackup = [s for s in core.stack]
        self.addressBackup = core.address
        
        core.handle_output = self.custom_output
        core.handle_input = self.custom_input
        self.input_value = []
        self.output_value = ''
        self.known_lines = []


    def custom_input(self):
        return self.input_value.pop(0)

    def custom_output(self, char):
        if char == '\n':
            if output_cache not in self.known_lines:
                print(output_cache)
                output_cache = ''
        else:
            output_cache += char

    def brute_force(self):
        for i in range(1, core.MAXINT):
            print(i)
            self.try_with(i)

    def try_with(self, register_value):
        core.memory = {k: v for k, v in self.memoryBackup.items()}
        core.register = [r for r in self.registerBackup]
        core.stack = [s for s in self.stackBackup]
        core.address = self.addressBackup

        core.register[-1] = register_value

        self.input_value = list('use teleporter\n')

        
