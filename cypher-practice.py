#every 2 letters a space will be added.
plaintext = input("enter word: ")

chars = list(plaintext)

for i in range(len(chars) - 1):
	if chars[i] == chars[i+1]:
		chars.insert(i+1,'x')
		break

modified = "".join(chars)

spaced_word = " ".join([modified[i:i+2] for i in range(0, len(modified), 2)])

print(spaced_word)
