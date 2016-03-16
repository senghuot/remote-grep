buffs = 'data.txt\r\ndummy\r\n\r\ndata.txt\r\nhello\r\n\r\n'
buffs = buffs.split("\r\n\r\n")
buffs = buffs[:len(buffs)-1]

print buffs