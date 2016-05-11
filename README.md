## Synopsis
AHP allow the analytic hierarchy process by a python script.


## Code Example
A mathematical, and coherent, translation of human choices is provided.

## Motivation
Supply to everyone a clear, 


## Installation
The script only needs Python 2 installed.
Then, only execute the ahp.py file in the same directory you download the main file:
	python ahp.py
        The folders called choices_all and choices should stay in the same directory too. 

## Use
To run the AHP process, each case must be saved as a text file in the "choices" directory.
You can use an already prepared file as pattern.

To a correct visualization, please, avoid unicode character in variables (they don't matter in comment).

About the numerical evaluations. 
	You can translate as "A is really really more important than B" as:
						B		
	A 			-->     8	-->  because of ...

	The scale may be:
	2	"A is a little bit 		more 		important than B"
	3	"A is 			 		more 		important than B"
	6	"A is really	 		more 		important than B"
	9	"A is extremely	 		more 		important than B"
	1/2	"A is a little bit		less 		important than B"
	1/3	"A is 			 		less 		important than B"
	1/6	"A is really	 		less 		important than B"
	1/9	"A is extremely	 		less 		important than B"



Example:

	[:g_c:]
						B_criteria        
	A_criteria		--> 		3		--> 	     
						C_criteria         
	A_criteria 		--> 		5		--> 	 

	In this situation, with respect to the A_criteria, C_criteria is less important than B_criteria.



## API Reference


## Tests
The script is provided with a test file (called “ahp_test.py”) for testing. 

## Contributors
Permit the storage in a separate file of the choices.
Let's write the choices file in a xml style
(not a different way parsed style).

## License
Apache