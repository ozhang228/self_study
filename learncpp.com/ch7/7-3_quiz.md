Question #1

Write a program that asks the user to enter two integers, one named smaller, the other named larger. If the user enters a smaller value for the second integer, use a block and a temporary variable to swap the smaller and larger values. Then print the values of the smaller and larger variables. Add comments to your code indicating where each variable dies. Note: When you print the values, smaller should hold the smaller input and larger the larger input, no matter which order they were entered in.

The program output should match the following:

Enter an integer: 4
Enter a larger integer: 2
Swapping the values
The smaller value is 2
The larger value is 4
Show Solution

Question #2

What’s the difference between a variable’s scope, duration, and lifetime? By default, what kind of scope and duration do local variables have (and what do those mean)?

A variable’s scope determines where the variable is accessible within the source code. Duration defines the rules that govern when a variable is created and destroyed. A variable’s lifetime is the actual time between its creation and destruction.

Local variables have block scope, which means they can be accessed from their point of definition to the end of the block they are defined within.

Local variables have automatic duration, which means they are created at the point of definition, and destroyed at the end of the block in which they are defined.


