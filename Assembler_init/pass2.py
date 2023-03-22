import re #分詞套件

#讀取opcode
opcodes = {}
with open("opcode.txt", 'r') as f:
  i = 0
  for line in f:
    cleaned_text = re.sub(r'[^\w\s]', '', line)
    words = cleaned_text.split()
    opcodes[words[0]] = words[1]

#loc 0000
loc = 0
symtab = {}
objCode = '00000000'
reg = {}

#讀取symtab
with open('symtab.txt', "r") as f:
  for line in f:
    key, value = line.strip().split(':')
    symtab[key]=value

#讀取Register
with open('register.txt', 'r') as f:
  for line in f:
    key, value = line.strip().split()
    reg[key]=value

#轉換成object code
def TranslateInstruction(parameter, PC, opRecord):
  opRecord_int = int(opRecord, 16)
  Ra = ''
  Rb = ''
  Rc = ''
  Cx = ''
  objCode = ''
  # L type
  if opRecord_int >= 0 and opRecord_int < 9:
    Ra = parameter[0]
    #address
    if '[' in parameter[1]:
      pattern = r'\[(?P<register>\w+)\+(?P<offset>\d+)\]'
      result = re.match(pattern, parameter[1]) #Not match result=None
      if result:
        register = result.group('register')
        offset = result.group('offset') #not really a offset, may be a register
        Rb = register
        if 'R' in offset:
          Rc = offset
          Cx = '000'
        else:
          Cx = int(offset)
          Cx = hex(Cx)[2:]
          Cx = Cx.zill(4)
      else:
        pattern = r'\[(?P<register>\w+)\]'
        result = re.match(pattern, parameter[1])
        if result:
          register = result.group('register')
          Rb = register
          Cx = '0000'

    elif parameter[1].isdigit():
      Cx = int(parameter[1])
      Cx = hex(Cx)[2:]
      Cx = Cx.zfill(5)
    else:
      Rb = 'R15'
      Cx = int(symtab[parameter[1]], 16) - (PC + 4)
      Cx = hex(Cx)[2:]
      Cx = Cx.zfill(4)

    objCode = opRecord[2:]+reg.get(Ra, '')+reg.get(Rb, '')+reg.get(Rc, '')+Cx

  # A type
  elif opRecord_int > 8 and opRecord_int < 32:
    Ra = parameter[0]
    Rb = parameter[1]
    if len(parameter) < 3:
      Cx = '0000'
    elif 'R' in parameter[2]:
      Rc = parameter[2]
      Cx = '000'
    else:
      Cx = int(parameter[2], 16)
      Cx = hex(Cx)[2:]
      Cx = Cx.zfill(4)
    objCode = opRecord[2:]+reg.get(Ra, '')+reg.get(Rb, '')+reg.get(Rc, '')+Cx

  # J type
  elif opRecord_int > 32 and opRecord_int < 48:
    if len(parameter) < 1:
      Cx = '000000'
    else:
      Cx = int(symtab[parameter[0]], 16) - (PC + 4)
      Cx = hex(Cx & 0xFFFFFF)[2:]
      Cx = Cx.zfill(6)
    objCode = opRecord[2:]+Cx

  #L, A, J type writein
  write_objprogram(objCode)
  # D type
  if opRecord_int > 239 and opRecord_int < 244:
    if opRecord_int == 242: #word
      for data in parameter:
        if data.isdigit():
          Cx = int(data)
          Cx = hex(Cx)[2:]
          objCode = Cx.zfill(8)
          write_objprogram(objCode)

        else:
          Cx = ord(data)
          Cx = hex(Cx)[2:]
          objCode = Cx.zfill(8)
          write_objprogram(objCode)

    elif opRecord_int == 243: #byte
      for data in parameter:
        if data.isdigit():
          Cx = int(data)
          Cx = hex(Cx)[2:]
          objCode = Cx.zfill(2)
          write_objprogram(objCode)
        else:
          Cx = ord(data)
          Cx = hex(Cx)[2:]
          objCode = Cx.zfill(2)
          write_objprogram(objCode)
  
  


class Static: #python no static
  new_line_count = 0 #when match to 4 words, then next line
  new_blank_count = 0 #when match to 4 byte, then next line

def write_objprogram(objCode):
  
  #寫入Object Program
  with open('obj_program.txt', 'a') as new_f:
    new_f.write(f'{objCode}')
    if len(objCode) == 8: #word length
      Static.new_line_count += 1
      if Static.new_line_count == 4:
        new_f.write('\n')
        Static.new_line_count = 0
      else:
        new_f.write(' ')
      
    elif len(objCode) == 2: #byte length
      Static.new_blank_count += 1
      if Static.new_blank_count == 4:
        new_f.write(' ')
        Static.new_line_count += 1
        Static.new_blank_count = 0

#main
with open('test.txt', 'r') as f:
  #分行
  for line in f:
    #去除掉分號後的敘述
    cleaned_text = re.sub(r';.*$', '', line) 
    # 利用正則表達式將冒號和數字之間的逗號替換為空格
    cleaned_text = re.sub(r'(?<=:)\s*(\d)', r' \1', cleaned_text)
    # 利用正則表達式去掉逗號，補上空格
    cleaned_text = re.sub(r',', ' ', cleaned_text)

    words = cleaned_text.split()
    #opcode parameter 轉換成 object code
    if words[0] in opcodes.keys():
      parameter = words[1:]
      TranslateInstruction(parameter, loc, opcodes[words[0]])
      loc += 4

    #symtab
    elif len(words) > 1 and (words[1] =='BYTE' or words[1] =='WORD'): #加上len(words) > 1 的判斷
      data = words[2:]
      TranslateInstruction(data, loc, opcodes[words[1]])

      if len(words) > 1 and words[1] =='BYTE':
        loc += 1*(len(words)-2)
      else: #'WORD'
        loc += 4*(len(words)-2)
    elif len(words) > 1 and words[1] =='RESB': #加上len(words) > 1 的判斷
      loc += words[2]
    elif len(words) > 1 and words[1] =='RESW': #加上len(words) > 1 的判斷
      loc += 4*words[2]
    

