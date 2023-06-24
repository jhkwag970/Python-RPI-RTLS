#source: https://gist.github.com/michelbl/efda48b19d3e587685e3441a74457024
import os, sys
if os.name == 'nt':
    import msvcrt
else:
    import termios
    import atexit
    from select import select

class lxTerm:
    def start(self, perform=True):
        if os.name != 'nt' and perform:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
            # Support normal-terminal reset at exit
            atexit.register(self.reset)

    def reset(self, perform=True):
        if os.name != 'nt' and perform:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self, auto=False):
        self.start(auto)
        if os.name == 'nt':
            x = msvcrt.getch()
        else:
            x = sys.stdin.read(1)
        self.reset(auto)
        return x

    def kbhit(self):
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []