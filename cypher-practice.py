#every 2 letters a space will be added.
plaintext = input("enter word: ")

for i in range(len(plaintext) - 1):
	if plaintext[i] == plaintext[i+1]:
		append_filler = "x".join([plaintext[i:i+1] for i in range(0,len(plaintext),1)])

spaced_word = " ".join([append_filler[i:i+2] for i in range(0, len(append_filler), 2)])


print(spaced_word)
