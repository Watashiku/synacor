import msvcrt
import struct
import sys
import time
import core
import code7


entry = []
output_cache = ''
INTERVAL = 0.05
SP = ' '
CR = '\r'
LF = '\n'
CRLF = CR + LF
CACHE = ''
is_full = False
filtered_lines = ['A strange, electronic voice is projected into your mind:',
'"Unusual setting detected!  Starting confirmation process!  Estimated time to completion: 1 billion years."',
'']


def echo(string):
  sys.stdout.write(string)
  sys.stdout.flush()


class TimeoutOccurred(Exception):
  pass


def inputimeout(timeout):
  global CACHE
  begin = time.monotonic()
  end = begin + timeout
  line = CACHE
  CACHE = ''

  while time.monotonic() < end:
    if msvcrt.kbhit():
      c = msvcrt.getwche()
      if c in (CR, LF):
        echo(CRLF)
        return line
      if c == '\003':
        raise KeyboardInterrupt
      if c == '\b':
        line = line[:-1]
        cover = SP * len(line + SP)
        echo(''.join([CR, cover, CR, line]))
      else:
        line += c
    time.sleep(INTERVAL)

  CACHE += line
  raise TimeoutOccurred


def handleInput():
  global entry
  first = is_full
  while not entry:
    try:
      if first:
        print(core.address)
        print()
        print()
        print()
        print()
        print(core.register)
        print()
        print()
        print()
        print()
        print()
        print(core.stack)
        print()
        print()
        print()
        print()
        mem = [0 for _ in range(max(core.memory))]
        for k in range(len(mem)):
          if k in core.memory:
            mem[k] = core.memory[k]
        data = struct.pack('H' * len(mem), *mem)
        with open('save.bin', mode='wb') as file:  # b is important -> binary
          file.write(data)

        code7.Code7()
        print(None)
        return None
        #core.memory[28844] = 0
      first = False
      entry = list(inputimeout(timeout=0.1)) + ['\n']
    except TimeoutOccurred:
      pass
  return entry.pop(0)


def handleOutput(data):
  global output_cache
  if data == LF:
    if output_cache.lstrip() not in filtered_lines:
      print(output_cache)
      print(output_cache)
      print(output_cache)
      input()
    output_cache = ''
  else:
    output_cache += data


def cmd(text):
  def cmd2(_):
    print(text)
    entry.extend(list(text))
  return cmd2


def full(inputs):
  global entry
  with open('challenge.bin', mode='rb') as file:  # b is important -> binary
    fileContent = file.read()
  data = struct.unpack('H' * (len(fileContent) // 2), fileContent)

  entry = list(inputs)
  core.run(data)

def checkpoint():
  
  with open('save.bin', mode='rb') as file:  # b is important -> binary
    fileContent = file.read()
  data = struct.unpack('H' * (len(fileContent) // 2), fileContent)

  for i in range(core.MAXINT, 1700, -1):
    restart(i, [d for d in data])


def restart(r8, data):
  global entry
  entry = list('use teleporter\n')
  print(r8)
  core.STOP = False
  core.LEFT = 2
  core.address = 1799 - 1
  core.register = [25975, 25974, 26006, 0, 101, 0, 0, r8]
  core.stack = [6080, 16, 6124, 1, 2826, 32, 4, 13, 101, 0]
  core.run(data)


start = '''take tablet
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
use can
use lantern
west
ladder
darkness
continue
west
west
west
west
north
take red coin
north
west
take blue coin
up
take shiny coin
down
east
east
take concave coin
down
take corroded coin
up
west
use blue coin
use red coin
use shiny coin
use concave coin
use corroded coin
north
take teleporter
use teleporter
take strange book
take business card
'''

core.handle_input = handleInput
core.handle_output = handleOutput
full(start) if is_full else checkpoint()
