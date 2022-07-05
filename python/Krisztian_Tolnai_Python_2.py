#given n pairs of paranthesis, write a function to generate all combinations of well formed parantheses


print('Enter a number: ')

#inputNum = int(input())


def generateParenthesis(numberOfPairs):   

        output = []

        def backtrack(openNumber, closedNumber, path):

            if openNumber == closedNumber == numberOfPairs:
                output.append(path)
                #print(path)
                return

            if openNumber < numberOfPairs:
                backtrack(openNumber + 1, closedNumber, path + "(")
                #print(path)

            if closedNumber < openNumber:
                backtrack(openNumber, closedNumber + 1, path + ")")
                #print(path)

        backtrack(0, 0, "")
        return output

try:
    inputNum = int(input())
    if  1 <= inputNum <= 8:
        #if input is correct
        print(generateParenthesis(inputNum))

    else:
        print("input cannot be less then 1 or more than 9!")
except ValueError:
    print("please enter a whole number!")




