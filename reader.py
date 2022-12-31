def pretty(data, fr, nb):
  def read():
    nonlocal address, output
    value = data[address] if address < len(data) else -1
    address += 1
    return value

  def f(name, args=0):
    nonlocal output
    name = str(address-1) + '\t' + name
    for _ in range(args):
      name += ' ' + str(read())
    output += [name]

  address = fr
  output = []
  while address < fr + nb:
    code = read()
    match code:
      case 0:  # halt
        f('HALT')
      case 1:  # set
        f('SET', 2)
      case 2:  # push
        f('PUSH', 1)
      case 3:  # pop
        f('POP', 1)
      case 4:  # eq
        f('EQ', 3)
      case 5:  # gt
        f('GT', 3)
      case 6:  # jmp
        f('JMP', 1)
      case 7:  # jt
        f('JT', 2)
      case 8:  # jf
        f('JF', 2)
      case 9:  # add
        f('ADD', 3)
      case 10:  # mult
        f('MULT', 3)
      case 11:  # mod
        f('MOD', 3)
      case 12:  # and
        f('OR', 3)
      case 13:  # or
        f('AND', 3)
      case 14:  # not
        f('NOT', 2)
      case 15:  # rmem
        f('RMEM', 2)
      case 16:  # wmem
        f('WMEM', 2)
      case 17:  # call
        f('CALL', 1)
      case 18:  # ret
        f('RET')
      case 19:  # out
        f('OUT', 1)
      case 20:  # in
        f('IN', 1)
      case 21:  # noop
        f('NOOP')
  print('------------------------------------------------------------------------')
  print('\n'.join(output))


def pretty_python(data, fr, nb):
  def read():
    nonlocal address, output
    value = data[address] if address < len(data) else -1
    address += 1
    if value > 32767:
      return chr(ord('A') + value - 32768)
    return str(value)

  def f(nb, l):
    nonlocal output
    output += [str(address-1) + '\t' + l([read() for _ in range(nb)])]

  address = fr
  output = []
  while address < fr + nb:
    code = read()
    match int(code):
      case 0:  # halt
        f(0, lambda _: f'exit()')
      case 1:  # set
        f(2, lambda args: f'{args[0]} = {args[1]}')
      case 2:  # push
        f(1, lambda args: f'push {args[0]}')
      case 3:  # pop
        f(1, lambda args: f'pop {args[0]}')
      case 4:  # eq
        f(3, lambda args: f'{args[0]} = ({args[1]} == {args[2]})')
      case 5:  # gt
        f(3, lambda args: f'{args[0]} = ({args[1]} > {args[2]})')
      case 6:  # jmp
        f(1, lambda args: f'jump {args[0]}')
      case 7:  # jt
        f(2, lambda args: f'if {args[0]}: jump {args[1]}')
      case 8:  # jf
        f(2, lambda args: f'if not {args[0]}: jump {args[1]}')
      case 9:  # add
        f(3, lambda args: f'{args[0]} = {args[1]} + {args[2]}')
      case 10:  # mult
        f(3, lambda args: f'{args[0]} = {args[1]} * {args[2]}')
      case 11:  # mod
        f(3, lambda args: f'{args[0]} = {args[1]} % {args[2]}')
      case 12:  # and
        f(3, lambda args: f'{args[0]} = {args[1]} | {args[2]}')
      case 13:  # or
        f(3, lambda args: f'{args[0]} = {args[1]} & {args[2]}')
      case 14:  # not
        f(2, lambda args: f'{args[0]} = ~{args[1]}')
      case 15:  # rmem
        f(2, lambda args: f'{args[0]} = mem[{args[1]}]')
      case 16:  # wmem
        f(2, lambda args: f'mem[{args[0]}] = {args[1]}')
      case 17:  # call
        f(1, lambda args: f'?? = f{args[0]}(??)')
      case 18:  # ret
        f(0, lambda _: f'return')
      case 19:  # out
        f(1, lambda args: f'print({chr(args[0])})')
      case 20:  # in
        f(1, lambda args: f'{args[0]} = input()')
      case 21:  # noop
        f(0, lambda _: f'pass')
  print('------------------------------------------------------------------------')
  print('\n'.join(output))
