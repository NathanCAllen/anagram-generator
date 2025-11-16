# Anagram Test Generator

## Overview
Basic Python library for generating anagrams and verifying solutions.

## Problem description
>The customer is a psychological research lab who is studying the phenomenon of “perfectionism.”
>
>The researchers in this lab decide that they will use puzzles to conduct an experiment on self-reported “perfectionists”, determining whether those who call themselves perfectionists react differently to difficult puzzles than those who do not.
>
>To satisfy this experiment condition, the researchers seek the help of a programmer -- you. They want to generate puzzles of varying difficulty. They want to be able to easily verify that the answers provided for a puzzle are correct. And they want to be able to generate unsolvable puzzles that look like solvable ones.
>
>The only requirement is that the puzzle generator and solver is written in Python, can be easily imported from a Python REPL , and can be used by someone who is a novice in Python (make function calls, create object instances, etc.) The code should also run quickly enough that it can be used in an interactive setting while the experiment subjects are in the room. No command-line interface or GUI is required.
>
>### The Anagram Puzzle
>Through some brainstorming with the team, you come up with the idea for generating “anagram puzzles”. These are puzzles based on re-arranging character sequences into a valid English word. For example, the puzzle “dgo” has the solutions “dog” and “god”.
>
>Write code that generates anagram strings of a given difficulty level, and code that can be used to verify or solve a given anagram string. What are some strategies for generating unsolvable puzzles that look like solvable puzzles?

## Usage
The core class, `AnagramGenerator`, can be imported from the `anagram_generator` module. It provides the following methods:

- `generate_anagrams`: Provides anagrams of a given length with a number of fake, but believable, anagrams mixed in. Anagram count, word length, and fake count are provided as parameters.
- `solve`: Returns a set of possible solutions for a provided anagram.
- `verify`: Returns whether a provided word is a solution for a provided anagram.
