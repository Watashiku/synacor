import msvcrt
import struct
import sys
import time
import keyboard
import core
import reader


entry = []
INTERVAL = 0.05
SP = ' '
CR = '\r'
LF = '\n'
CRLF = CR + LF
CACHE = ''


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
  first = True
  while not entry:
    try:
      if first:
        # core.log_state()
        core.register[-1] = 10000
        #core.memory[28844] = 0
      first = False
      entry = list(inputimeout(timeout=0.1)) + ['\n']
    except TimeoutOccurred:
      pass
  return entry.pop(0)


def handleOutput(data):
  print(data, end='')


def cmd(text):
  def cmd2(_):
    print(text)
    entry.extend(list(text))
  return cmd2


def full(inputs):
  global entry
  with open('C:\\Users\\Titi\\Downloads\\synacor-challenge\\challenge.bin', mode='rb') as file:  # b is important -> binary
    fileContent = file.read()
  data = struct.unpack('H' * (len(fileContent) // 2), fileContent)

  reader.pretty_python(data, 2980, len(data))
  return
  #core.run(data[1262:], handleInput=handleInput, handleOutput=handleOutput)
  # return

  for key, text in (('up', 'north\n'), ('left', 'west\n'), ('right', 'east\n'), ('down', 'south\n')):
    keyboard.on_press_key(
        key, cmd(text), suppress=True)

  entry = list(inputs)
  core.run(data, handleInput=handleInput, handleOutput=handleOutput)


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

full(start)
