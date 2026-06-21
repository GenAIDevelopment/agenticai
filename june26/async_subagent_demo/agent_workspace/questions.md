# 30-Question Assessment: Entry-Level Software Startup Role

This assessment consists of 30 multiple choice questions divided into three sections: Logical Reasoning, Basic Programming, and Professional Communications. Each question has exactly four choices.

---

## Section 1: Logical Reasoning (Questions 1–10)

### Question 1
If in a certain language, "PYTHON" is coded as "QXUGPM", how is "DJANGO" coded in that same language?
- A) EIBMHN
- B) EICMHO
- C) EJBMHN
- D) DKBMHN

### Question 2
What is the next number in the sequence: 4, 7, 12, 21, 38, ...?
- A) 71
- B) 76
- C) 69
- D) 73

### Question 3
Pointing to a photograph of a boy, Suresh (a man) says, "He is the son of the only son of my mother." How is Suresh related to that boy?
- A) Brother
- B) Uncle
- C) Cousin
- D) Father

### Question 4
Analyze the following statements and select the correct conclusion:
**Statements:**
1. All developers are creators.
2. Some creators are artists.

**Conclusions:**
I. Some developers are artists.
II. Some artists are creators.
- A) Only conclusion I follows
- B) Only conclusion II follows
- C) Both conclusions I and II follow
- D) Neither conclusion I nor II follows

### Question 5
A QA engineer starts from the office and walks 4 km South. Then she turns left and walks 3 km. Finally, she turns left again and walks 8 km. How far and in which direction is she now from her starting point?
- A) 5 km North-East
- B) 5 km South-East
- C) 7 km North-West
- D) 15 km North-East

### Question 6
An automated script can run in three modes: Fast, Normal, and Safe. The transition rules are:
1. If in 'Safe' mode, it can only transition to 'Normal' mode.
2. If in 'Normal' mode, it can transition to 'Fast' mode or 'Safe' mode.
3. If in 'Fast' mode, it can only transition to 'Safe' mode.

If the script starts in 'Fast' mode and transitions exactly 4 times, which of the following is NOT a possible sequence of modes?
- A) Fast -> Safe -> Normal -> Fast -> Safe
- B) Fast -> Safe -> Normal -> Safe -> Normal
- C) Fast -> Safe -> Normal -> Safe -> Fast
- D) All of the above are valid sequences

### Question 7
Complete the analogy based on standard technical taxonomy:
**Git : Version Control :: Docker : _________**
- A) Virtualization
- B) Containerization
- C) Cloud Computing
- D) Orchestration

### Question 8
Observe the pattern in the sequence of 3-letter terms and determine the next term:
**ABC, BDF, CFI, DHL, ...**
- A) EKO
- B) EJO
- C) EKP
- D) EJP

### Question 9
Four developers (Alice, Bob, Charlie, and Dave) are debugging a crash.
- Alice says: "Bob did not write the bug."
- Bob says: "Charlie wrote the bug."
- Charlie says: "Dave wrote the bug."
- Dave says: "Charlie is lying when he says I wrote it."

If exactly one of them is telling the truth, who wrote the bug?
- A) Alice
- B) Bob
- C) Charlie
- D) Dave

### Question 10
A microservices system has 3 types of tasks: Heavy, Medium, and Light.
- 1 Heavy task requires the same CPU capacity as 2 Medium tasks.
- 1 Medium task requires the same CPU capacity as 3 Light tasks.

If a server can run exactly 4 Heavy tasks and 3 Medium tasks simultaneously at maximum capacity, how many Light tasks can it run at maximum capacity instead?
- A) 27
- B) 30
- C) 33
- D) 36

---

## Section 2: Basic Programming & Python (Questions 11–20)

### Question 11
What is the output of the following Python code?
```python
def append_to_list(value, my_list=[]):
    my_list.append(value)
    return my_list

print(append_to_list(1))
print(append_to_list(2))
```
- A) [1] and [2]
- B) [1] and [1, 2]
- C) [1] and [2, 2]
- D) Error because a list cannot be used as a default argument

### Question 12
What is the output of the following Python expression?
```python
my_list = [10, 20, 30, 40, 50]
print(my_list[::-2])
```
- A) [50, 30, 10]
- B) [10, 30, 50]
- C) [50, 40, 30, 20, 10]
- D) [40, 20]

### Question 13
What will be the output of the following Python code?
```python
data = {"a": 1, "b": 2}
val = data.get("c", 3)
print(val + data.get("a", 0))
```
- A) 4
- B) 3
- C) KeyError: 'c'
- D) 1

### Question 14
Consider the expression: `x = True or False and False`. What is the value of `x`?
- A) True
- B) False
- C) None
- D) SyntaxError

### Question 15
Consider the following code block:
```python
s1 = "hello"
s2 = s1
s1 += " world"
print(s2)
```
What is printed?
- A) "hello world"
- B) "hello"
- C) "world"
- D) AttributeError

### Question 16
You are building a feature for a startup where users look up username availability instantly. Which data structure provides an average time complexity of O(1) for checking if a username exists?
- A) A sorted array (List)
- B) A singly linked list
- C) A hash set (Set)
- D) A binary search tree

### Question 17
What is the final value of the variable 'count' after running the following loop?
```python
count = 0
for i in range(1, 10):
    if i % 3 == 0:
        continue
    count += 1
```
- A) 9
- B) 6
- C) 3
- D) 10

### Question 18
In Python, what is the value of 'result' after executing the following expression?
```python
result = (17 // 3) % 2
```
- A) 2
- B) 1
- C) 5
- D) 1.0

### Question 19
A startup is building an "Undo" feature for their text editor. Which data structure is most appropriate for tracking the history of edits, where the last action performed is the first one to be undone?
- A) Queue (FIFO)
- B) Stack (LIFO)
- C) Graph
- D) Binary Tree

### Question 20
What is the output of the following Python script?
```python
x = 10

def update_val():
    x = 5
    return x

update_val()
print(x)
```
- A) 5
- B) 10
- C) None
- D) NameError

---

## Section 3: Professional Communications (Questions 21–30)

### Question 21
Identify the grammatically correct sentence for an email update to the team.
- A) Neither the product manager nor the developers has approved the new deployment schedule.
- B) Neither the product manager nor the developers have approved the new deployment schedule.
- C) Neither the product manager nor the developers was approving the new deployment schedule.
- D) Neither the product manager nor the developers is approving the new deployment schedule.

### Question 22
Choose the correct option to fill in the blanks:
"The new UI theme is designed to _______ the overall user experience, and we expect it will have a positive _______ on customer retention."
- A) compliment; affect
- B) complement; effect
- C) complement; affect
- D) compliment; effect

### Question 23
When should you use BCC (Blind Carbon Copy) in professional email communication?
- A) To secretly include a colleague in a sensitive argument or dispute.
- B) To protect the privacy of recipients when emailing a large, external group.
- C) To ensure everyone can reply to all recipients in the thread.
- D) To archive the email in your personal folder.

### Question 24
Read the following passage and select the most accurate inference based on it:
"Agile software development emphasizes iterative development, team collaboration, and rapid response to change. While traditional Waterfall projects plan everything upfront, Agile projects focus on delivering working software in small, frequent increments. This approach allows teams to adapt to shifting user requirements quickly, though it requires constant communication and can sometimes lead to 'scope creep' if not managed carefully."

What does the passage imply about Agile software development?
- A) It is always faster and cheaper than the traditional Waterfall method.
- B) It requires disciplined management of project scope to prevent uncontrolled expansion.
- C) It eliminates the need for formal planning or project documentation entirely.
- D) It is best suited for small teams that do not require frequent communication.

### Question 25
In a software startup's daily standup, a teammate says: "I'm really struggling to integrate this third-party API; the documentation is outdated, and I keep getting unauthorized errors." Which of the following responses demonstrates the best active listening and collaborative communication?
- A) Your best move is to check their GitHub issues rather than their official documentation website.
- B) Why didn't you ask for help yesterday? We are falling behind on our sprint goals.
- C) It sounds like you're frustrated because the API documentation isn't accurate and it's blocking your progress. Let's look at the auth headers together after this meeting.
- D) Just keep trying; APIs can be tricky but I'm sure you will figure it out eventually.

### Question 26
Which of the following sentences is the most professional, clear, and concise way to ask a client for clarification on a vague bug report?
- A) Your bug report is very confusing, so please send us more details so we can understand what is wrong.
- B) To help us resolve this issue quickly, could you please provide the steps to reproduce the bug and a screenshot of the error message?
- C) We got your ticket but it doesn't make any sense. Please tell us how you broke it or we can't fix it.
- D) Please write back and explain what you did in detail because the error you submitted doesn't work on our side.

### Question 27
Imagine a software feature release is going to be delayed by two days due to an unexpected bug found during QA. Which email update to the product owner represents the most professional and assertive communication style?
- A) I'm sorry to say that QA found another bug, so the release is ruined and we won't make the deadline. It's not our fault though.
- B) We found a critical bug during final testing. We are delaying the release by two days to resolve it, ensuring a stable deployment on Wednesday. We will keep you updated.
- C) We might not release on time because of some issues. We hope to fix it soon, but we aren't completely sure when it will be ready.
- D) Due to QA failures, we are forced to postpone the release. Hopefully, we can launch it next week if everything goes well.

### Question 28
During a retrospective, your manager mentions that the team needs to avoid "siloed working" to improve sprint velocity. What does the term "siloed working" mean in this context?
- A) Working in a highly structured environment with clear divisions of labor.
- B) Working in isolation from other team members or departments, leading to a lack of communication and collaboration.
- C) Working excessively long hours without taking sufficient breaks.
- D) Working purely on backend tasks without understanding frontend development.

### Question 29
When performing a code review, which of the following comments is the most constructive way to suggest a performance improvement to a peer?
- A) This loop is incredibly inefficient. Did you even test this with large datasets?
- B) I rewritten this section because your approach was too slow. Use my code instead.
- C) This approach works, but using a hash map here instead of nested loops would improve the time complexity from O(N^2) to O(N). What do you think?
- D) You should never use nested loops in JavaScript because they slow down the entire system.

### Question 30
You receive a Jira ticket with the description: "The checkout page needs a better user experience." The ticket is assigned to you, but there are no design mocks, acceptance criteria, or further details. What is the most appropriate next step?
- A) Implement what you think looks best and deploy it directly to production.
- B) Reject the ticket and leave a comment saying, "This ticket is useless; please provide real specifications."
- C) Reach out to the product manager or designer to schedule a brief call to clarify the goals, or ask for the missing details in a polite comment on the ticket.
- D) Wait until the next sprint planning meeting to bring it up, leaving the ticket untouched in the meantime.
