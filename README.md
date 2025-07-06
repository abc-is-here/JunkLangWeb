# JunkLang

**JunkLang** is a junk food-themed esoteric programming language where your code tastes as good as it runs. Inspired by BhaiLang and other meme langs, I won't mind if you call this a piece of junk!

---

## Features

- `order` variables and `eat` expressions  
- Arithmetic operations  
- `whisper` to print  
- `reheat:` to define functions, `deliver()` to call  
- `if you like` ... `else:` conditionals  
- `until thirsty <condition>` loops  
- Input with `open your mouth and say`  
- Custom errors with `barf("message")`  
- CLI interpreter (`junk program.jnk`)

---

## Installation

You can install it globally via `pip`:

```bash
pip install junklang
```

Now you can run `.jnk` files using:

```bash
junklang <yourfile>.jnk
```

---

## Example Code

```junk
open your mouth and say burgers
order fries = 5
order meal = eat burgers + fries
whisper "You ordered a meal of " + meal

if you like meal more than 5:
    whisper "That's a big meal!"
else:
    whisper "That’s a light snack."
done

order total = 0
until thirsty total < 3:
    order total = eat total + 1
    whisper "Nom #" + total
done

reheat: make_burger
    order patty = 1
    order bun = 2
    order burger = eat patty + bun
done

order my_burger = deliver(make_burger)
whisper "I got a burger with " + my_burger + " parts"

barf("No more food for you!")
```

---

## Language Syntax

### Variables
```junk
order x = 5
order y = eat x + 10
```

### Arithmetic
Supports `+`, `-`, `*`, `/` inside `eat` expressions.

### Print
```junk
whisper "Hello World"
whisper "Value is: " + x
```

### Input
```junk
open your mouth and say name
```

### Conditionals
```junk
if you like x more than 5:
    whisper "x is big"
else:
    whisper "x is small"
done
```

### Loops
```junk
until thirsty counter < 10:
    whisper counter
    order counter = eat counter + 1
done
```

### Functions
```junk
reheat: cook
    order x = 1
    order y = 2
    order z = eat x + y
done

order result = deliver(cook)
```

### Errors
```junk
barf("Something went wrong!")
```

---

## Run a `.jnk` File

```bash
junklang hello.jnk
```

---

## Developer Setup

```bash
git clone https://github.com/abc-is-here/junkLangWeb.git
cd junklang
pip install .
```

---

## Written in Python

This language is written in Python and is intended more for learning and fun than performance.
