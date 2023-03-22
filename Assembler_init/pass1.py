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

#loc 0000
loc = 0
symtab = {}

#main
with open("test.txt", 'r') as f:
  for line in f:
    #去除掉分號後的敘述
    cleaned_text = re.sub(r';.*$', '', line) 
    # 利用正則表達式將冒號和數字之間的逗號替換為空格
    cleaned_text = re.sub(r'(?<=:)\s*(\d)', r' \1', cleaned_text)
    # 利用正則表達式去掉逗號，補上空格
    cleaned_text = re.sub(r',', ' ', cleaned_text)

    words = cleaned_text.split()
    if ':' in words[0]: #找到symbol,修改loc
      #symbol table
      format_loc = '{:04X}'.format(loc)
      symtab[words[0]] = format_loc

      #每行前面加入loc
      #format_loc = '{:04X}'.format(loc)
      new_line = f'{format_loc} {line}'

      if len(words) == 1:
        pass
      elif len(words) > 1 and words[1] =='BYTE': #加上len(words) > 1 的判斷
        loc += 1*(len(words)-2)
      elif len(words) > 1 and words[1] =='WORD': #加上len(words) > 1 的判斷
        loc += 4*(len(words)-2)
      elif len(words) > 1 and words[1] =='RESB': #加上len(words) > 1 的判斷
        loc += words[2]
      elif len(words) > 1 and words[1] =='RESW': #加上len(words) > 1 的判斷
        loc += 4*words[2]
      else:
        print("error on", words)
        exit()
    elif words[0] in opcodes.keys(): #找到opcode修改loc
      #每行前面加入loc
      format_loc = '{:04X}'.format(loc)
      new_line = f'{format_loc}\t{line}'

      loc += 4

    #寫入test_addloc.txt，依行寫入
    with open('test_addloc.txt', 'a') as new_f:
      new_f.write(new_line)

#寫入symtab
with open('symtab.txt', "w") as new_f:
  for key, value in symtab.items():
    new_f.write(f"{key} {value}\n")
    