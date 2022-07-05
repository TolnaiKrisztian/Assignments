print('Enter a string: ')
#inputText = "pwwkew"
inputText = input()
dict = {}
output = 0

j = 0

if  inputText.isascii() and (0 <= len(inputText) <= 5 * (10**4)):
    for i in range(0, len(inputText)):
        #check if the letter is already in the dictionary
        if inputText[i] in dict:
            j = max(dict[inputText[i]] + 1, i)
        #calculate the output
        output = max(output, (i - j + 1))
        #update character index
        dict[inputText[i]] = i
    print(output)
    #print(dict)
else:
    print("Only english letters, digits, symbols and spaces are allowed!")
