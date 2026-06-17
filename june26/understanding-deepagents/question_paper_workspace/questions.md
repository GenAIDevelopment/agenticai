# Interview Question Paper for Entry-Level Software Developer

## Section 1: Reasoning (10 Questions)

1. **Pattern Recognition**
   If "CODE" is coded as "DPFE", how is "JAVA" coded?
   A) KBWA
   B) KBCB
   C) KBWB
   D) JAWB

2. **Logical Deduction**
   All software developers are logical. Some logical people are creative. Which of the following must be true?
   A) All software developers are creative.
   B) Some software developers are creative.
   C) Some creative people are logical.
   D) No software developer is creative.

3. **Algorithm Logic**
   You have an array of 100 integers. You need to find the smallest number in the array. What is the most efficient Big O time complexity to achieve this?
   A) O(1)
   B) O(log n)
   C) O(n)
   D) O(n²)

4. **Problem Solving**
   You have two hourglasses: one that measures 4 minutes and one that measures 7 minutes. How can you measure exactly 9 minutes?
   A) Start both. When the 4-min one finishes, flip it. When the 7-min one finishes, flip it.
   B) Start both. When the 4-min one finishes, restart it immediately. When the 7-min one finishes, it has been 7 minutes. You need 2 more minutes.
   C) Start both. When the 4-min runs out, turn it over. When the 7-min runs out, turn it over.
   D) There is no way to measure exactly 9 minutes with these two tools.

5. **Analytical Thinking**
   If 5 machines can produce 5 widgets in 5 minutes, how long will it take 100 machines to produce 100 widgets?
   A) 5 minutes
   B) 20 minutes
   C) 50 minutes
   D) 100 minutes

6. **System Design Logic**
   In a distributed system, what is the primary trade-off described by the CAP theorem?
   A) Consistency, Availability, and Partition Tolerance
   B) Speed, Reliability, and Scalability
   C) Cost, Complexity, and Throughput
   D) Security, Privacy, and Functionality

7. **Sequence Completion**
   What comes next in the sequence: 2, 4, 8, 16, 32, ...?
   A) 48
   B) 60
   C) 64
   D) 72

8. **Conditional Reasoning**
   If the statement "If it is raining, the street is wet" is true, which of the following is also true?
   A) If the street is wet, it is raining.
   B) If it is not raining, the street is not wet.
   C) If the street is not wet, it is not raining.
   D) The street is wet only if it is raining.

9. **Data Structure Basics**
   Which data structure follows the LIFO (Last-In-First-Out) principle?
   A) Queue
   B) Stack
   C) Array
   D) Linked List

10. **Optimization**
    You are tasked with searching for a specific item in a sorted list of 1,000,000 items. Which search method is most efficient?
    A) Linear Search
    B) Breadth-First Search
    C) Binary Search
    D) Depth-First Search

## Section 2: Programming (10 Questions)

11. What is the primary purpose of a version control system like Git?
    a) To increase the execution speed of code.
    b) To track changes in source code and facilitate collaboration.
    c) To automatically identify and fix bugs in code.
    d) To manage server infrastructure.

12. Which of the following is an example of an immutable data type in Python?
    a) List
    b) Dictionary
    c) Tuple
    d) Set

13. In object-oriented programming, what is the concept of "encapsulation"?
    a) Hiding the internal state of an object and requiring all interaction to be performed through an object's methods.
    b) Creating a new class from an existing class.
    c) Defining multiple methods with the same name but different parameters.
    d) Automatically managing memory allocation.

14. Which data structure follows the Last-In-First-Out (LIFO) principle?
    a) Queue
    b) Stack
    c) Linked List
    d) Hash Map

15. What is the Big O complexity of searching for an item in a sorted array using binary search?
    a) O(n)
    b) O(1)
    c) O(n log n)
    d) O(log n)

16. Which HTTP method is typically used to update an existing resource?
    a) GET
    b) POST
    c) PUT
    d) DELETE

17. What does the term "API" stand for?
    a) Application Programming Interface
    b) Automated Program Integration
    c) Advanced Processing Instruction
    d) Application Protocol Implementation

18. In database design, what is a "primary key"?
    a) A field that allows for fast searching across multiple tables.
    b) A column that uniquely identifies each row in a table.
    c) A password used to access the database.
    d) A temporary table used for complex queries.

19. Which of the following best describes the purpose of unit testing?
    a) Testing the performance of the entire application.
    b) Testing individual components or functions of the software in isolation.
    c) Validating that the user interface meets design requirements.
    d) Verifying the compatibility of the software with different operating systems.

20. What is a common side effect of using "global variables" in a large codebase?
    a) Increased memory usage.
    b) Improved code readability.
    c) Difficulty in debugging and testing due to unpredictable state changes.
    d) Reduced compilation time.

## Section 3: Communications (10 Questions)

21. You encounter a bug in a codebase that you don't know how to fix. What is the best initial approach?
    A) Spend the entire day trying to fix it alone to avoid looking incompetent.
    B) Immediately escalate the issue to the CTO without attempting any investigation.
    C) Spend a reasonable amount of time investigating the issue, then document your findings and ask a teammate for guidance.
    D) Ignore the bug and hope it isn't noticed during the next deployment.

22. During a code review, a senior developer leaves a comment suggesting a significant change to your code. How should you respond?
    A) Ignore the comment if you believe your way is correct.
    B) Reply defensively to justify your original implementation.
    C) Ask clarifying questions to understand their reasoning, and discuss the trade-offs before implementing changes.
    D) Delete your code and ask them to rewrite it for you.

23. When communicating technical progress in a stand-up meeting, what is the most important element to include?
    A) A detailed history of every line of code you wrote.
    B) A clear summary of what you accomplished, what you are working on, and any blockers you are facing.
    C) A list of all the technical debt you introduced.
    D) Personal anecdotes about your day.

24. You notice a potential security vulnerability in a feature that is scheduled for release today. What should you do?
    A) Wait for the next sprint to bring it up.
    B) Fix it silently without informing anyone.
    C) Immediately alert the project manager and the relevant technical lead with a clear explanation of the risk.
    D) Assume the team lead already knows about it and continue with your current task.

25. How should you communicate with a non-technical stakeholder about a technical delay?
    A) Explain the complex architecture and every technical nuance of the problem.
    B) Use industry jargon to justify why the delay is unavoidable.
    C) Briefly explain the impact of the delay in business terms and provide an updated timeline.
    D) Avoid talking to them until the task is completely finished.

26. You are working remotely and haven't heard back from a team member regarding a critical task for several hours. What is the best way to follow up?
    A) Send an urgent, angry message demanding an immediate response.
    B) Call them repeatedly until they answer.
    C) Send a polite, concise message checking in on the status and asking for an ETA.
    D) Stop working until they reach out to you.

27. What is the most effective way to provide constructive feedback to a peer?
    A) Send an anonymous email pointing out their mistakes.
    B) Bring it up in front of the whole team during a meeting to ensure everyone learns.
    C) Schedule a 1-on-1 meeting to discuss specific, observable behaviors and their impact in a supportive manner.
    D) Wait until their annual performance review to mention it.

28. You are asked to document a new API endpoint. What is your primary goal?
    A) To make the documentation as long and detailed as possible.
    B) To ensure the documentation is clear, concise, and helpful for other developers who will use the endpoint.
    C) To use complex language to showcase your technical knowledge.
    D) To omit any potential errors or edge cases to make the API look better.

29. When participating in a brainstorming session, you disagree with a proposed idea. How do you express this?
    A) Interrupt the person speaking to explain why they are wrong.
    B) Remain silent to avoid conflict.
    C) Acknowledge the idea, then share your concerns or alternative perspectives using data or clear reasoning.
    D) Ridicule the idea to discourage others from proposing similar thoughts.

30. Which of the following best describes "active listening" in a professional setting?
    A) Hearing what someone says while thinking about your next response.
    B) Nodding while the other person speaks, regardless of what they are saying.
    C) Fully concentrating on the speaker, understanding their message, and providing thoughtful feedback or questions.
    D) Recording the conversation to review later, so you don't have to pay attention in the moment.

---

## Answer Key

### Reasoning
1: C, 2: C, 3: C, 4: B, 5: A, 6: A, 7: C, 8: C, 9: B, 10: C

### Programming
11: b, 12: c, 13: a, 14: b, 15: d, 16: c, 17: a, 18: b, 19: b, 20: c

### Communications
21: C, 22: C, 23: B, 24: C, 25: C, 26: C, 27: C, 28: B, 29: C, 30: C
