#every 2 letters a space will be added.
plaintext = input("enter word: ")
spaced_word = " ".join([plaintext[i:i+2] for i in range(0, len(plaintext), 2)])
print(spaced_word)
