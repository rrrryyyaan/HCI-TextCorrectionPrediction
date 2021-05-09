import tkinter as tk
import time
import re
import operator
import random
from PyDictionary import PyDictionary
from tkinter import scrolledtext
from tkinter import messagebox
from collections import Counter

"""
    File Name: Main.py
    Author: Ryan Bell & Sam Woodworth
    Date Created: 4/19/2021
    Date Last Modified: 5/9/2021
    Python Version: 3.8.5
"""

#Taken from norvig: https://norvig.com/spell-correct.html
def lowercase(text): 
    return re.findall(r'\w+', text.lower())


#Taken from norvig to read in all the words from big.txt: https://norvig.com/spell-correct.html
WORDS = Counter(lowercase(open('big.txt').read()))


def removeDuplicates(list_replace):
    seen = set()
    list_replace[:] = [item for item in list_replace if item not in seen and not seen.add(item)]
    return list_replace


def biPairs(word):
    splits = list()
    for i in range(len(word) - 1):
        splits.append(word[i] + word[i+1])

    return splits


def wordFromPairs(bi_pairs):
    word = ""
    counter = 0
    for chars in bi_pairs:
        if counter == 0:
            word = chars
        else:
            word = word + chars[1]
        counter += 1
    return word


def findNext(word):
    next_words = {}
    f = open("big.txt")
    text = f.read()
    text = text.split()
    index = 0
    for words in text:
        if words == word:
            next_words[text[index + 1]] = next_words.get(text[index + 1], 0) + 1
        index += 1

    return next_words


def findPrevious(word):
    prev_words = {}
    f = open("big.txt")
    text = f.read()
    text = text.split()
    index = 0
    for words in text:
        if words == word:
            prev_words[text[index - 1]] = prev_words.get(text[index - 1], 0) + 1
        index += 1

    return prev_words


def findBoth(word):
    next_words = {}
    prev_words = {}
    f = open("big.txt")
    text = f.read()
    text = text.split()
    index = 0
    for words in text:
        if words == word:
            prev_words[text[index - 1]] = prev_words.get(text[index - 1], 0) + 1
            next_words[text[index + 1]] = next_words.get(text[index + 1], 0) + 1
        index += 1

    return (prev_words, next_words)


def probability(word):
    return WORDS[word] / sum(WORDS.values())


def compareDic(word):
    for w in WORDS:
        if word == w:
            return True

    return False


def correctFile():
    print("File name to read from?")
    file_name_read = input()
    print("File name to write to?")
    file_name_write = input()
    f = open(file_name_read, 'r')
    w = open(file_name_write, 'w')
    words = f.read().lower()
    words = words.split()
    
    print("Running correction.. Please wait...")
    for word in words:
        if word[0] == "$":
            w.write(word)
            w.write("\n")
            continue
        if(compareDic(word)):
            w.write(word)
            w.write("\n")
            continue
        potential = oneEdit(word)
        if potential:
            w.write(potential[0])
            w.write("\n")
        else:
            w.write(suggestFromPairs(word))
            w.write("\n")
            

    print("Correction finished. It can be found in ", file_name_write)

    f.close()


def correctWord(word):
    potential = oneEdit(word)
    if potential:
        corrected = potential[0]
    else:
        corrected = suggestFromPairs(word)
    return corrected


def suggestFromPairs(word):
    if(compareDic(word)):
        return
    new_list = list()
    pairs = biPairs(word)
    counter = 0
    for pot_word in WORDS:
        for pair in pairs:
            if pair in pot_word:
                counter += 1
                if counter == 3 and (len(pot_word) <= len(word) + 1 and len(pot_word) >= len(word) - 1):
                    new_list.append(pot_word)
        counter = 0

    return generateBestWords(word, new_list)


def generateBestWords(pot_word, pot_list):
    new_list = list()
    bi_word = biPairs(pot_word)
    
    for each in pot_list:
        new_list.append(biPairs(each))

    counter = 0
    max = 0
    best_word = list()
    for word in new_list:
        index = 0
        for pair in word:
            if index < len(bi_word):
                if pair == bi_word[index]:
                    counter += 1
                index += 1
        if counter > 0 and counter >= max:
            best_word.append(word)
            max = counter
        counter = 0

    return pickBestWord(pot_word, best_word)


def pickBestWord(word, pot_list):
    final_list = list()
    bi_word = biPairs(word)
    good_counter = 0
    pot_pair_index = 0
    max = 0
    for pairs in pot_list:
        for pair_index in range(len(bi_word) - 1):
            if pot_pair_index < len(bi_word):
                if pairs[pot_pair_index] == bi_word[pair_index]:
                    good_counter += 1
                pot_pair_index += 1
        if good_counter > 0 and good_counter >= max:
            final_list.append(pairs)
            max = good_counter
        good_counter = 0
        pot_pair_index = 0

    if(len(final_list) > 1):
        x = random.randint(0, len(final_list) - 1)
        final_word = wordFromPairs(final_list[x])
    elif (len(final_list) == 1):
        final_word = wordFromPairs(final_list[0])
    else:
        final_word = "NA"

    if(compareDic(final_word)):
        final_word = final_word
    else:
        final_word = "NA"
    return final_word


def oneEdit(word):
    all_list = list()
    updated_list = list()

    letters = 'abcdefghijklmnopqrstuvwxyz'

    #delete - create list of words where each index is removed
    for count in range(len(word)):
        deletes = word[0 : count :] + word[count + 1 : :]
        all_list.append(deletes)

    #inserts - create list of words where each letter of the alphabet is inserted in each index
    for count in range(len(word)):
        for c in letters:
            inserts = word[:count] + c + word[count:]
            all_list.append(inserts)

    #transpose - create list of words where 2 letters are swapped for all letters in the word
    for count in range(len(word)):
        if(count < len(word) - 1):
            new_word = word[:count] + word[count + 1] + word[count+2:count+1] + word[count] + word[count+2:]
            all_list.append(new_word)

    #replacement - create list of words where each index is replaced by every letter in the alphabet
    for count in range(len(word)):
        for c in letters:
            word_list = list(word)
            word_list[count] = c
            replacement = "".join(word_list)
            all_list.append(replacement)
    
    all_list = removeDuplicates(all_list)

    for k in range(len(all_list)):
        if(compareDic(all_list[k])):
            updated_list.append(all_list[k])

    return updated_list


def textPrediction():
    run = True
    use_suggested = False
    list_mem = list()
    while run:
        showCurrent(list_mem)
        if use_suggested:
            suggested_word = suggestNext(word)
            if(len(suggested_word) > 0):
                if(showSuggestions(suggested_word)):
                    list_mem.append(suggested_word)
                    word = suggested_word
                else:
                    use_suggested = False
            else:
                use_suggested = False
        else:
            word = input("Please enter a word ('q' to quit): ")
            if(word == "q"):
                run = False
                showCurrent(list_mem)
                continue
            if not compareDic(word):
                word = correctWord(word)
            list_mem.append(word)
            showCurrent(list_mem)
            suggested_word = suggestNext(word)
            if(len(suggested_word) > 0):
                if(showSuggestions(suggested_word)):
                    use_suggested = True
                    list_mem.append(suggested_word)
                    word = suggested_word


def showCurrent(list_mem):
    if list_mem:
        print("\nCurrent text:")
        for word in list_mem:
            print(word, end = " ")
    print("\n")


def suggestNext(word):
    #print(findNext(word))
    sorted_dic = dict(sorted(findNext(word).items(), key = operator.itemgetter(1), reverse=True))
    suggest_list = list(sorted_dic)
    #print(suggest_list)
    if suggest_list:
        suggest = suggest_list[0]
    else:
        suggest = ""
    return suggest


def showSuggestions(suggested):
    print("Suggested next word: ", suggested)
    choice = input("Would you like to use this suggested word? (Y/N) ")
    if(choice == "Y" or choice == "y" or choice == "Yes" or choice == "yes"):
        return True
    else:
        return False



if __name__ == '__main__':

    print("Would you like to use Text Prediction or Text Correction? (P/C)")
    selection = input()

    if(selection == "P" or selection == "p" or selection == "Prediction" or selection == "prediction"):
        print("Text PREDICTION program selected. Please follow the prompts.")
        textPrediction()
    else:
        print("Text CORRECTION program selected. Please follow the prompts.")
        #suggestFromPairs("fining")
        correctFile()

    
