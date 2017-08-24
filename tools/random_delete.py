import os
import random
import csv

path = 'E:\\big_image'

file_num = sum([len(files) for root, dirs, files in os.walk(path)])
print 'Orignal files num :', file_num
file_list = range(1, file_num + 1)
print file_list

# Random
random.shuffle(file_list)
print file_list

# Pick out the first 100 pcs of file_num list and workout the file name list
file_name_list = []
file_list_cut = []
for num in range(0, 200):
    file_list_cut.append(file_list[num])
    file_front = str(file_list[num])
    file_name = file_front + '.jpg'
    file_name_list.append(file_name)
print file_name_list
print file_list_cut

# Move files to other dict
src_path = 'E:\\big_image'
dst_path = 'E:\\out_image'

for file_jpg in file_name_list:
    sourceFile = os.path.join(src_path,  file_jpg)
    targetFile = os.path.join(dst_path,  file_jpg)
    if os.path.isfile(sourceFile):
        open(targetFile, "wb").write(open(sourceFile, "rb").read())


csv_path = 'E:\out_image\dataset_list.csv'

# Create the csv list
file_list_order = file_list_cut
file_list_order.sort()
print file_list_order
with open(csv_path, 'wb') as csv_dstfile:
    csv_writer = csv.writer(csv_dstfile)
    csv_writer.writerow(['name'])
    for key in file_list_order:
        csv_writer.writerow([key])
csv_dstfile.close()

print 'Works finished!'
# print type(file)
