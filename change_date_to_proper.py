from datetime import datetime
import csv
f=open("Weatherdata.csv",'r',newline='')
f1=open("Weathercopy.csv",'w',newline='')
reader=csv.reader(f)
writer=csv.writer(f1)
data=list(reader)
i = 0
for row in data:
    if i == 0:
        i =1
    else:
        try:
            temp = datetime.strptime(row[0], '%Y%m%d').strftime('%Y-%m-%d')
            row[0] = temp
            writer.writerow(row)
            i+=1
        except Exception as e:
            print(f"invalid {row[0]}") # if a row fails to edit
print(f"Total dates are {i}")
f.close()
f1.close()
