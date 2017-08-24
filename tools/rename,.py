import os
import time

path = 'E:\\big_image'
i = 1

timer_start = time.clock()
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path,file)) == True:
        new_name = file.replace(file, "%d.jpg"%i)
        os.rename(os.path.join(path, file), os.path.join(path, new_name))
        i += 1

print 'END'

timer_end = time.clock()
time_total = timer_end - timer_start
print 'Time is ', time_total, 's'

