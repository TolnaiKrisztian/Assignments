#given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitions of s.

#import string
#letters = list(string.ascii_lowercase)
#print(letters)

print("Enter a string: ")

inputText = input().lower()
output = []
workingList = []
inputLength = len(inputText)

def searchPalindrome(startingIndex,List):
    if startingIndex == inputLength:
        output.append(List)
        return
    for i in range(startingIndex,inputLength):
        #check if its a palindrome
        if inputText[startingIndex:i+1] == inputText[startingIndex:i+1][::-1]:
            searchPalindrome(i+1,List+[inputText[startingIndex:i+1]])
    return output


if inputText.isalpha() and 1 <= len(inputText) <= 16:
    print(searchPalindrome(0,workingList))

else:
    print("String must only contain english letters and cannot be longer than 16 letters!")




