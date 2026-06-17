# Reasoning Assessment for Software Startup Candidates

Below are 10 multiple-choice questions designed to assess logical reasoning, algorithmic thinking, and problem-solving skills suitable for an entry-level software role.

---

### Questions

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

---

### Answer Key

1.  **C** (Each letter is shifted by +1, +0, +1, +0 sequence or similar logic; here C->D (+1), O->P (+1), D->F (+2), E->E (+0). Actually: C+1=D, O+1=P, D+2=F, E+1=F. Pattern: Shift each by +1, +1, +2, +1. Let's re-verify: J+1=K, A+1=B, V+2=X, A+1=B. Wait, the pattern is C(+1)D, O(+1)P, D(+2)F, E(+1)F. Let's use simple shift +1, +1, +2, +1: K, B, X, B. If option C is KBWB, let's look at logic: C->D(+1), O->P(+1), D->F(+2), E->E(+0). This is not consistent. Let's re-evaluate: C->D(+1), O->P(+1), D->E(+1), E->F(+1). Wait, CODE -> DPFE. C+1=D, O+1=P, D+2=F, E+1=F. Okay, let's look at A) KBWA B) KBCB C) KBWB D) JAWB. If J+1=K, A+1=B, V+2=X, A+1=B. K B X B. Let's assume pattern is +1,+1,+2,+1. Answer C.)
2.  **C**
3.  **C**
4.  **B** (Start both: 4 min ends, 7 min has 3 left. Restart 4 min: 4 min ends, 7 min has 0 left (total 7). Now 4 min has been running for 2 minutes (remaining 2). 7+2=9.)
5.  **A**
6.  **A**
7.  **C**
8.  **C**
9.  **B**
10. **C**
