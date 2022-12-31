import struct
from inputimeout import inputimeout, TimeoutOccurred
import tkinter as tk

memory = {}
register = [0 for _ in range(8)]
stack = []
address = 0
codes = []
entry = []
T = None

MAXINT = 32768


def tkSetup():
  global T

  root = tk.Tk()
  root.geometry("700x400")
  T = tk.Text(root, height=20, width=70)
  l = tk.Label(root, text="Synacor")
  l.config(font=("Courier", 14))

  bs = []
  for text in ("north\n", "west\n", "east\n", "south\n"):
    bs.append(tk.Button(root, text=text[:-1],
              command=cmd(text)))
  b2 = tk.Button(root, text="Exit",
                 command=root.destroy)

  l.pack()
  b2.pack(side=tk.RIGHT)
  T.pack()
  for b in bs:
    b.pack(side=tk.LEFT)


def cmd(text):
  def cmd2():
    entry.extend(list(text))
  return cmd2


def error(s):
  print(codes[-30:])
  raise Exception('Error at address ' + str(address) + ' : ' + s)


def addToStack(v):
  stack.append(v)


def removeFromStack():
  return stack.pop()


def setRegister(i, v):
  if 0 <= i < 8:
    register[i] = v
  elif MAXINT <= i < MAXINT+8:
    register[i-MAXINT] = v
  else:
    error('setRegister ' + str(i))


def getRegister(i):
  if 0 <= i < 8:
    return register[i]
  elif MAXINT <= i < MAXINT+8:
    return register[i-MAXINT]
  else:
    error('getRegister ' + str(i))


def store(a, v):
  if 0 <= a < MAXINT:
    memory[a] = v
  elif MAXINT <= a < MAXINT+8:
    setRegister(a, v)
  else:
    error('store ' + str(a))


def get(a):
  if 0 <= a < MAXINT:
    return memory[a]
  elif MAXINT <= a < MAXINT+8:
    return getRegister(a)
  else:
    error('get ' + str(a))


def valueOrRegister(v):
  if v < MAXINT:
    return v
  return getRegister(v)


def readValue():
  v = valueOrRegister(readNext())
  return v


def readAddress():
  v = readNext()
  return v


def readNext():
  global address
  v = get(address)
  address += 1
  return v


def jump(to):
  global address
  address = to


def run(bin, inputs):
  global entry
  for i in range(len(bin)):
    store(i, bin[i])
  entry = inputs
  pL = -1

  # for key, text in ((72, "north\n"), ("left", "west\n"), ("right", "east\n"), ("down", "south\n")):
  #  keyboard.on_press_key(
  #      key, lambda _: entry.extend(list(text)), suppress=True)

  while True:
    code = readValue()
    codes.append((code, address))

    # if code == 19 and codes[-2][0] != 19:
    #  print(codes[-10:])
    # if 2200 < address and not 2740 < address < 3335 and not 5800 < address < 5950:
    #  print(address)
    # if len(codes) == pL:
    #  print('\n'.join([str(c) for c in codes[-1000:]]))
    match code:
      case 0:
        print(codes[-30:])
        return
      case 1:
        setRegister(readAddress(), readValue())
      case 2:
        addToStack(readValue())
      case 3:
        store(readAddress(), removeFromStack())
      case 4:
        store(readAddress(), 1 if readValue() == readValue() else 0)
      case 5:
        store(readAddress(), 1 if readValue() > readValue() else 0)
      case 6:
        jump(readValue())
      case 7:
        a, b = readValue(), readValue()
        if a != 0:
          jump(b)
      case 8:
        a, b = readValue(), readValue()
        if a == 0:
          jump(b)
      case 9:
        store(readAddress(), (readValue() + readValue()) % MAXINT)
      case 10:
        store(readAddress(), (readValue() * readValue()) % MAXINT)
      case 11:
        store(readAddress(), readValue() % readValue())
      case 12:
        store(readAddress(), readValue() & readValue())
      case 13:
        store(readAddress(), readValue() | readValue())
      case 14:
        store(readAddress(), ~readValue() % MAXINT)
      case 15:
        store(readAddress(), get(readValue()))
      case 16:
        store(readValue(), readValue())
      case 17:
        addToStack(address + 1)
        jump(readValue())
        continue
      case 18:
        jump(removeFromStack())
      case 19:
        handleOutput(readValue())
      case 20:
        handleInput()
      case 21:
        pass
      case other:
        error('code missing ' + str(other))


def handleOutput(char):
  char = chr(char)
  if char == '=':
    T.delete('0.0', 'end')
  print(char, end='')
  T.insert(tk.END, char)
  T.update()


def handleInput():
  global entry
  while not entry:
    print('mainloop', entry)
    tk.mainloop()
    # try:
    #  value = list(inputimeout(timeout=0.1)) + ['\n']
    #  entry.extend(value)
    # except TimeoutOccurred:
    #  pass
  store(readAddress(), ord(entry.pop(0)))


def full(inputs):
  with open('C:\\Users\\Titi\\Downloads\\synacor-challenge\\challenge.bin', mode='rb') as file:  # b is important -> binary
    fileContent = file.read()
  a = struct.unpack("H" * (len(fileContent) // 2), fileContent)
  # print('----------------------------------------------------------------------------------------------------------------------------------')
  # print(a[845:900])

  T.insert(tk.END, "Start")
  T.update()
  run(a, list(inputs))


start = """take tablet
doorway
north
north
bridge
continue
down
east
take empty lantern
west
west
passage
ladder
west
south
north
take can
west
"""

tkSetup()
full(start)
