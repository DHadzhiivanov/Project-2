#every 2 letters a space will be added.
plaintext = input("enter word: ").lower()

i=0
prepared=""

while i<len(plaintext):
	prepared += plaintext[i]
	if i + 1 < len(plaintext):
		if plaintext[i] == plaintext[i+1]:
			prepared += "x"
			i+=1
		else:
			prepared+=plaintext[i+1]
			i+=2
	else:
		i+=1

if len(prepared) % 2 != 0:
	prepared += "x"

spaced_word = " ".join([prepared[i:i+2] for i in range(0, len(prepared), 2)])

print("".join(spaced_word))
