import reader

memory = {}
register = [0 for _ in range(8)]
stack = []
address = 0
codes = []

MAXINT = 32768


def log_state():
  print(register)
  print(codes[-150:])
  reader.pretty(memory, 6027, 50)
  input()


def error(s):
  print(codes[-30:])
  raise Exception('Error at address ' + str(address) + ' : ' + s)


def add_to_stack(v):
  stack.append(v)


def remove_from_stack():
  return stack.pop()


def set_register(i, v):
  if 0 <= i < 8:
    register[i] = v
  elif MAXINT <= i < MAXINT+8:
    register[i-MAXINT] = v
  else:
    error('set_register ' + str(i))


def get_register(i):
  if i == 7 or i - MAXINT == 7 and register[7] != 0:
    print('register 8')
    log_state()
  if 0 <= i < 8:
    return register[i]
  elif MAXINT <= i < MAXINT+8:
    return register[i-MAXINT]
  else:
    error('get_register ' + str(i))


def store(a, v):
  if 0 <= a < MAXINT:
    memory[a] = v
  elif MAXINT <= a < MAXINT+8:
    set_register(a, v)
  else:
    error('store ' + str(a))


def get(a):
  if 0 <= a < MAXINT:
    return memory[a]
  elif MAXINT <= a < MAXINT+8:
    return get_register(a)
  else:
    error('get ' + str(a))


def value_or_register(v):
  if v < MAXINT:
    return v
  return get_register(v)


def read_value():
  v = value_or_register(read_next())
  return v


def read_address():
  v = read_next()
  return v


def read_next():
  global address
  v = get(address)
  address += 1
  return v


def jump(to):
  global address
  address = to


def run(data, handleInput, handleOutput):
  for i in range(len(data)):
    store(i, data[i])

  while True:
    code = read_value()
    codes.append((code, address-1))

    # if code == 19 and codes[-2][0] != 19:
    #  print(codes[-10:])
    # if 2200 < address and not 2740 < address < 3335 and not 5800 < address < 5950:
    #  print(address)
    # if len(codes) == pL:
    #  print('\n'.join([str(c) for c in codes[-1000:]]))
    match code:
      case 0:  # halt
        return
      case 1:  # set
        set_register(read_address(), read_value())
      case 2:  # push
        add_to_stack(read_value())
      case 3:  # pop
        store(read_address(), remove_from_stack())
      case 4:  # eq
        store(read_address(), 1 if read_value() == read_value() else 0)
      case 5:  # gt
        store(read_address(), 1 if read_value() > read_value() else 0)
      case 6:  # jmp
        jump(read_value())
      case 7:  # jt
        a, b = read_value(), read_value()
        if a != 0:
          jump(b)
      case 8:  # jf
        a, b = read_value(), read_value()
        if a == 0:
          jump(b)
      case 9:  # add
        store(read_address(), (read_value() + read_value()) % MAXINT)
      case 10:  # mult
        store(read_address(), (read_value() * read_value()) % MAXINT)
      case 11:  # mod
        store(read_address(), read_value() % read_value())
      case 12:  # and
        store(read_address(), read_value() & read_value())
      case 13:  # or
        store(read_address(), read_value() | read_value())
      case 14:  # not
        store(read_address(), ~read_value() % MAXINT)
      case 15:  # rmem
        store(read_address(), get(read_value()))
      case 16:  # wmem
        store(read_value(), read_value())
      case 17:  # call
        add_to_stack(address + 1)
        function_name = read_value()
        if function_name == 1767:
          print(register)
          input()
        jump(function_name)
        continue
      case 18:  # ret
        jump(remove_from_stack())
      case 19:  # out
        handleOutput(chr(read_value()))
      case 20:  # in
        store(read_address(), ord(handleInput()))
      case 21:  # noop
        pass
      case other:
        error('code missing ' + str(other))
