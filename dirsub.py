import re

def assign_line_type(line, linetype=''):
    if line.startswith('/eos/'):
        linetype = 'dir'
        return linetype
    if line.endswith('.root'):
        linetype = 'file'
        return linetype

f_read = open('test.list', 'r')
lines = f_read.readlines()

f_write = open('DYfiles.txt', 'w')

num_lines = 0

for line in lines:
    line = line.strip()
    linetype= assign_line_type(line)

    if linetype == 'dir':
        dir_str = re.sub('/eos/cms', 'root://cms-xrd-global.cern.ch/', line)
        dir_str = dir_str[:-1] + '/'
    
    if linetype == 'file':
        f_write.write(dir_str + line + '\n')
        num_lines += 1
        if num_lines == 1000: break

f_read.close()
f_write.close()