import os

setupsToMove = [
    "2j_2j_2s_4a_2pe",
    "2j_2j_2s_4a_0pe",
    "3j_3j_3s_4a_0pe",
    "3j_3j_3s_4a_3pe",
    "3j_5j_4s_4a_0pe",
    "2j_2j_1s_4a_0pe",
    "2j_2j_1s_4a_1pe",
    "3j_5j_4s_4a_4pe"
]

print(setupsToMove) 
ans = input("Move these folders? (Y/N): ")

if ans.upper() == "Y":
    for setupName in setupsToMove:
            print(setupName)
            ans = input("Move %s? (Y/N): " % setupName)

            if ans.upper() == "Y":
                os.system("rclone copy onedrive:urop/2022/initial_outputs/%s outputs/%s -P" % (setupName, setupName))
