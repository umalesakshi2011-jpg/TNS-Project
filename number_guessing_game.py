import random
secret = random.randint(1,20)
max_attempts=6
attempt =1

while attempt <= max_attempts:
    num = int(input("Guess Number(number between 1-20):"))
    if num == secret:
        print("Guess is correct")
        print("attempt:",attempt)
        break
    else:
        print("wrong guess")
        if num <secret:
            print("Guess Higher")
        else:
            print("Guess Lower")
    attempt+=1
