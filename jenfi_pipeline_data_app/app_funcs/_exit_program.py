# Exit program
class StopExecution(Exception):
    def _render_traceback_(self):
        pass

def exit_not_applicable(self, message: str) -> None:
    # Write output

    raise StopExecution
