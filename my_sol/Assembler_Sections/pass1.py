import re #分詞套件

#讀取opcode
opcodes = {}
with open("opcode.txt", 'r') as f:
  i = 0
  for line in f:
    cleaned_text = re.sub(r'[^\w\s]', '', line)
    words = cleaned_text.split()
    words[1] = words[1][2:] #去除0x
    opcodes[words[0]] = words[1]


loc_switch = 0 
#0: .bss
#1: .data
#2: .text

#loc 0000
loc = [0, 0 ,0] # .bss, .data, .text
symtab = {}
new_line = ''
writein_flag = 1 #判斷是否寫入，避免.bss, .data, .text 重複輸入

def sections(loc_switcher):
  type = {
    0 : 'B',
    1 : 'D',
    2 : 'T'
  }
  return type.get(loc_switcher, '')

#main
with open("stackmain.txt", 'r') as f:
  for line in f:
    #去除掉分號後的敘述
    cleaned_text = re.sub(r';.*$', '', line) 
    # 利用正則表達式將冒號和數字之間的逗號替換為空格
    cleaned_text = re.sub(r'(?<=:)\s*(\d)', r' \1', cleaned_text)
    # 利用正則表達式去掉逗號，補上空格
    cleaned_text = re.sub(r',', ' ', cleaned_text)

    words = cleaned_text.split()
    #找到假指令
    if '.' in words[0]: 
      #假指令定址loc
      if words[0] == '.bss': 
        loc_switch = 0
      elif words[0] == '.data':
        loc_switch = 1
      elif words[0] == '.text':
        loc_switch = 2
      else: #.global .extern
        pass

    elif ':' in words[0]: #找到symbol,修改loc
      #flag
      writein_flag = 1
      #每行前面加入loc
      format_loc = '{:04X}'.format(loc[loc_switch])
      #symbol table
      symtab[words[0]] = format_loc

      #每行前面加入loc
      new_line = f'{sections(loc_switch)} {format_loc} {line}'

      if len(words) == 1:
        pass
      elif len(words) > 1 and words[1] =='BYTE': #加上len(words) > 1 的判斷
        loc[loc_switch] += 1*(len(words)-2)
      elif len(words) > 1 and words[1] =='WORD': #加上len(words) > 1 的判斷
        loc[loc_switch] += 4*(len(words)-2)
      elif len(words) > 1 and words[1] =='RESB': #加上len(words) > 1 的判斷
        loc[loc_switch] += int(words[2])
      elif len(words) > 1 and words[1] =='RESW': #加上len(words) > 1 的判斷
        loc[loc_switch] += 4*int(words[2])
      else:
        print("error on", words)
        exit()
    elif words[0] in opcodes.keys(): #找到opcode修改loc
      #flag
      writein_flag = 1
      #每行前面加入loc
      format_loc = '{:04X}'.format(loc[loc_switch])
      new_line = f'{sections(loc_switch)} {format_loc}\t{line}'

      loc[loc_switch] += 4


    #寫入loc.txt，依行寫入
    if writein_flag == 1:
      writein_flag = 0
      with open('stackmain_addloc.txt', 'a') as new_f:
        new_f.write(new_line)

#寫入symtab
with open('stackmain_sym.txt', "w") as new_f:
  for key, value in symtab.items():
    new_f.write(f"{key} {value}\n")
    