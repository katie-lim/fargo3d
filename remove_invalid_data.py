import os

setupName = "7j_7j_1s_0.7a_8h_0pe"
files_to_remove = []
output_types = ["gasdens", "gasenergy", "gasvx", "gasvy", "summary"]

for i in range(1282, 1331):
    for output_type in output_types:
        files_to_remove.append("outputs/%s/%s%d.dat" % (setupName, output_type, i))

print(files_to_remove)
ans = input("Remove these files? (Y/N): ")

if ans.upper() == "Y":
    for file in files_to_remove:
        os.system("rm %s" % file)