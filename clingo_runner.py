from clyngor import solve
import shutil
import os

class AspRunner:
    debug_filename = 'debug_asp_runner'
    def __init__(self):
        self.models = []
        self.program_run = False
        self.errors = 0
        if not os.path.exists(self.debug_filename):
            os.makedirs(self.debug_filename)
            #shutil.rmtree(self.debug_filename)

    def run(self, program):
        try:
            self.models = solve(inline=program)
            coreferences = set([r for answer in self.models.by_predicate for r in map(lambda args: args[1], answer.get('coref') or [])])
        except SystemError as e:
            debug_file = f'{self.debug_filename}_{str(self.errors)}'
            with open(f'{self.debug_filename}/{debug_file}', 'w') as f:
                f.write('Failed program is: \n')
                f.write(program)
                f.write('\n\n\n\n\n')
                f.write(f'{e}')
            self.errors += 1
            raise Exception(f'Clingo program failed to run successfully. See {debug_file}')
        return coreferences
