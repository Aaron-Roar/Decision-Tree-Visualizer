#DataPreperationProgram (DPP)

The case of percentages over 100% has not been handled, THINGS WILL BREAK IF PREFORMED
For commas the sys.argv[4] in the program will have to be manually changed to the value "," i appolagize in advance

##Arguements
- Input File
- Output file 1 (percent applied)
- output file 2 (1 - percent applied)
- delimiter character
- percent to split
- Column to translate (optional)
- Column to translate to (optional)


##Example Use
Example 1
- python3 input.data output1.data output2.data \ 40
- The input file will be randomly split 40% into output1.data 60% into output2.data
- The delimiter for parsing used is the "\ " aka <SPACE> character

Example 2
- python3 input.data output1.data output2.data \ 70 0 4
- The input file will be randomly split 70% into output1.data 30% into output2.data
- The delimiter for parsing used is the "\ " aka <SPACE> character
- Column 0 is translated to column four

