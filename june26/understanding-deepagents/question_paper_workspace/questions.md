# Aptitude and Skills Assessment Paper
### Entry-Level Software Startup Candidate

This assessment consists of 30 multiple-choice questions divided into three sections:
1. **Logical Reasoning & Aptitude** (Questions 1-10)
2. **Basic Programming & Coding Concepts** (Questions 11-20)
3. **Communications & Workplace Collaboration** (Questions 21-30)

---

## Section 1: Logical Reasoning & Aptitude

### Question 1
In a certain code language, if the word 'SEND' is coded as '168', and the word 'PURSE' is coded as '395', how will the word 'INSULT' be coded in the same language?
- **A)** 495
- **B)** 515
- **C)** 570
- **D)** 612

### Question 2
Find the missing number in the following mathematical series: 
`4, 18, 48, 100, 180, ?, 448`
- **A)** 248
- **B)** 294
- **C)** 312
- **D)** 280

### Question 3
Given the following statements, which of the conclusions logically follow(s)?
**Statements:**
1. Only a few students are Girls.
2. Some Girls are Boys.
3. No Boy is a Student.

**Conclusions:**
* I. Some Students are not Girls.
* II. All Girls can be Students is a possibility.

- **A)** Only conclusion I follows
- **B)** Only conclusion II follows
- **C)** Both conclusion I and conclusion II follow
- **D)** Neither conclusion I nor conclusion II follows

### Question 4
If 'A + B' means 'A is the mother of B', 'A - B' means 'A is the brother of B', 'A % B' means 'A is the father of B', and 'A x B' means 'A is the sister of B', which of the following expressions indicates that 'P' is the maternal uncle of 'Q'?
- **A)** Q - N + M x P
- **B)** P + S x N - Q
- **C)** P - M + N x Q
- **D)** Q - S % P

### Question 5
One morning after sunrise, Udai and Vishal were talking to each other face-to-face at a crossing. If Vishal's shadow was cast exactly to the left of Udai, which direction was Udai facing?
- **A)** East
- **B)** West
- **C)** North
- **D)** South

### Question 6
Select the option that logically completes the word analogy:
`COMPUTERS : MOP :: PLATFORM : ?`
- **A)** LAP
- **B)** ALT
- **C)** LOT
- **D)** PAT

### Question 7
Three of the following four numbers are alike in a certain way and one is different. Select the odd one out: 
`135, 175, 518, 246`
- **A)** 135
- **B)** 175
- **C)** 518
- **D)** 246

### Question 8
What is the next term in the following letter-pair series?
`AZ, CX, FU, JQ, OL, ?`
- **A)** TG
- **B)** UF
- **C)** VE
- **D)** WD

### Question 9
Four developers—Alice, Bob, Charlie, and Diana—work on different microservices: Auth, Billing, Database, and Search. They sit in a row of four desks numbered 1 to 4 (left to right).
1. The Auth developer sits at Desk 4.
2. The Billing developer sits at Desk 2.
3. Bob works on Database and sits immediately to the right of Alice.
4. Charlie works on Search.

Which developer works on Auth, and at which desk do they sit?
- **A)** Alice, Desk 2
- **B)** Diana, Desk 4
- **C)** Charlie, Desk 1
- **D)** Bob, Desk 3

### Question 10
In a software startup of 60 employees, 35 employees know Python, 30 know Go, and 20 know Rust. Furthermore, 15 know both Python and Go, 10 know both Go and Rust, and 8 know both Python and Rust. If 5 employees know all three programming languages, how many employees in the startup know exactly one of these three languages?
- **A)** 28
- **B)** 34
- **C)** 37
- **D)** 42

---

## Section 2: Basic Programming & Coding Concepts

### Question 11
What will be the output of the following Python code?

```python
def append_to(element, to=[]):
    to.append(element)
    return to

my_list1 = append_to(12)
my_list2 = append_to(42)
print(my_list2)
```

- **A)** `[42]`
- **B)** `[12, 42]`
- **C)** `None`
- **D)** `Error: Default argument cannot be changed`

### Question 12
Given a list `numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`, what is the output of `print(numbers[::-2])`?
- **A)** `[10, 8, 6, 4, 2]`
- **B)** `[9, 7, 5, 3, 1]`
- **C)** `[2, 4, 6, 8, 10]`
- **D)** `[1, 3, 5, 7, 9]`

### Question 13
What is the result of the expression `True or False and not True` in Python?
- **A)** `True`
- **B)** `False`
- **C)** `None`
- **D)** `SyntaxError`

### Question 14
Which of the following data types can **NOT** be used as a key in a standard Python dictionary?
- **A)** tuple (e.g., `(1, 2)`)
- **B)** frozenset (e.g., `frozenset([1, 2])`)
- **C)** list (e.g., `[1, 2]`)
- **D)** int (e.g., `42`)

### Question 15
What is the output of the following Python code snippet?

```python
word = "Startup"
print(word[len(word) // 2])
```

- **A)** `'r'`
- **B)** `'t'`
- **C)** `'a'`
- **D)** `TypeError: string indices must be integers`

### Question 16
In Python, which of the following actions is most effective for freeing up memory when dealing with a very large list variable `data` that is no longer needed in the middle of a long-running script?
- **A)** Set `data = None` or use `del data`
- **B)** Call `data.clear()`
- **C)** Run a for loop to pop every item from `data`
- **D)** Write `pass` and let Python's garbage collector handle it immediately

### Question 17
Consider the following recursive function. What does `calculate(4)` return?

```python
def calculate(n):
    if n <= 1:
        return 1
    return n * calculate(n - 2)
```

- **A)** `24`
- **B)** `8`
- **C)** `4`
- **D)** `16`

### Question 18
What will the following expression evaluate to in Python?

```python
print(0.1 + 0.2 == 0.3)
```

- **A)** `True, because arithmetic operations are exact in Python.`
- **B)** `False, due to floating-point precision limitations in binary representation.`
- **C)** `TypeError, because you cannot compare floating-point values directly.`
- **D)** `True, because Python automatically rounds float comparisons to 10 decimal places.`

### Question 19
What is the output of the following Python code?

```python
keys = ['a', 'b', 'c']
values = [1, 2, 3]
my_dict = {k: v * 2 for k, v in zip(keys, values) if v % 2 != 0}
print(my_dict)
```

- **A)** `{'a': 2, 'b': 4, 'c': 6}`
- **B)** `{'a': 2, 'c': 6}`
- **C)** `{'b': 4}`
- **D)** `{'a': 1, 'c': 3}`

### Question 20
What is the output of the following Python code?

```python
list_a = [1, [2, 3], 4]
list_b = list(list_a)
list_b[1][0] = 99
list_b[2] = 100
print(list_a)
```

- **A)** `[1, [99, 3], 4]`
- **B)** `[1, [2, 3], 4]`
- **C)** `[1, [99, 3], 100]`
- **D)** `[1, [2, 3], 100]`

---

## Section 3: Communications & Workplace Collaboration

### Question 21
As an entry-level engineer drafting a bug report, which of the following sentences is grammatically correct and most appropriate for a technical email update?
- **A)** Neither the lead developer nor the systems administrator are aware of why the server crashed during the deployment.
- **B)** Neither the lead developer nor the systems administrator is aware of why the server crashed during the deployment.
- **C)** Neither the lead developer nor the systems administrator were aware of why the server crashed during the deployment.
- **D)** Neither the lead developer nor the systems administrator have been aware of why the server crashed during the deployment.

### Question 22
Your product manager asks the team to modernize the stack: *"We need to ________ the legacy payment system by the end of Q3 and transition all users to the new Stripe API."* Which phrasal verb best completes the sentence?
- **A)** phase out
- **B)** throw down
- **C)** wipe off
- **D)** pull through

### Question 23
Read the following statement:

*"Technical debt is a concept in software development that reflects the implied cost of additional rework caused by choosing an easy (quick) solution now instead of using a better approach that would take longer. While technical debt can help a startup release its MVP (Minimum Viable Product) quickly to gain market feedback, compounding debt without regular refactoring can lead to a debt trap where the team spends more time fixing bugs than shipping new features."*

According to the passage, what is the primary risk of compounding technical debt?
- **A)** The startup will lose its primary competitive advantage because it can no longer hire qualified software engineers.
- **B)** The startup's Minimum Viable Product (MVP) will fail to gain any initial market feedback.
- **C)** The engineering team will reach a point where fixing existing bugs consumes more development time than implementing new features.
- **D)** The financial cost of refactoring the codebase will exceed the company's total venture capital funding.

### Question 24
You notice that a peer on your engineering team has accidentally broken the staging build twice this week because they skipped running tests locally before pushing. What is the most constructive way to communicate with them?
- **A)** Send a message in the team's public Slack channel: *"Please run tests before committing code, you are breaking the build for everyone."*
- **B)** Report the incidents directly to the CTO so that they can take immediate disciplinary action against the engineer.
- **C)** Message them privately: *"Hey, I noticed the build broke a couple of times recently due to skipped local tests. Let's work together to make sure our local environments are set up correctly so we don't block the team."*
- **D)** Wait until the bi-weekly team retrospective meeting to raise the issue of build stability and point out their specific commits.

### Question 25
You are scheduled to give a live product demo to a client, but you are running 10 minutes late due to a sudden technical issue with your meeting client. Which of the following is the most professional email or message to send to the client?
- **A)** *Hey! So sorry, my Zoom is acting up and I can't get in. Give me like 10 mins and I'll be there!*
- **B)** *Dear Client, I apologize, but I am experiencing a brief technical issue with my meeting software. I will join our demo 10 minutes late, at 2:10 PM. Thank you for your patience.*
- **C)** *Apologies for the delay. The meeting link is broken. I will join as soon as it works.*
- **D)** *Hi team, my laptop just crashed. I am rebooting and should be online in 10 minutes. Apologies for the inconvenience.*

### Question 26
When writing technical documentation for a new caching layer, which of the following sentences is grammatically correct and free of dangling modifiers?
- **A)** Having optimized the database query, the page load time decreased by 50%.
- **B)** After completing the security audit, the code was pushed to production by the DevOps team.
- **C)** To run the local development server, Docker must be installed on your machine.
- **D)** While reviewing the pull request, I noticed several syntax errors in the utility module.

### Question 27
During a sprint planning meeting, the CTO says, *"We need to deprecate our legacy v1 authentication endpoints by the end of this month."* What does the word 'deprecate' mean in this context?
- **A)** To delete the legacy authentication code immediately from all repositories to save disk space.
- **B)** To mark the endpoints as obsolete and discourage their use, while maintaining temporary support for existing users during a transition period.
- **C)** To rewrite the v1 authentication codebase entirely in another programming language to improve efficiency.
- **D)** To restrict access to the v1 endpoints using multi-factor authentication and advanced encryption standards.

### Question 28
Read the following Slack exchange between a Product Manager (PM) and a Software Engineer (SWE):

**PM:** *"Hi Alex, can we ship the dark mode toggle today?"*
**SWE:** *"The frontend code is ready, but the feature flag backend API is throwing 500 errors on staging. I am waiting on the backend team to merge the PR that fixes this. Once they do, we will need to run a quick regression test before pushing."*

What is the primary bottleneck preventing the dark mode feature from being released today?
- **A)** Alex has not finished writing the frontend user interface code for the dark mode toggle.
- **B)** The staging server is completely offline due to database connectivity issues.
- **C)** The backend team has not yet merged the pull request that resolves the feature flag API errors.
- **D)** The regression testing process is taking too long to run on the production server.

### Question 29
Your engineering manager asks you to focus entirely on finishing a critical feature for a client demo tomorrow. Simultaneously, your tech lead messages you to immediately fix a minor cosmetic bug in the onboarding flow. How should you handle this conflict in priorities?
- **A)** Agree to both requests, work on the minor onboarding bug first, and then work late into the night to finish the demo feature.
- **B)** Tell the tech lead that you cannot work on the onboarding bug because your manager's request is much more important.
- **C)** Create a group thread with both the manager and tech lead, explain the conflict, and politely ask them to help prioritize: *"I want to align with team priorities. Which of these should I prioritize today?"*
- **D)** Ignore both direct requests and continue working on your pre-allocated sprint tickets to remain neutral.

### Question 30
A customer support representative reports that the 'Sign Up' button is unresponsive on mobile devices. Which of the following is the most professional, clear, and actionable bug report to submit to the engineering team?
- **A)** *The Sign Up button is broken on phones. I tried clicking it on my mobile device and absolutely nothing happened. Please fix this as soon as possible.*
- **B)** *Bug: Sign Up failure. Steps: Go to signup page on mobile Safari (iOS 17.2), fill in details, and tap 'Sign Up'. Expected: Redirection to dashboard. Actual: Button is unresponsive; no console errors or network requests are triggered.*
- **C)** *Our registration flow is completely down on mobile devices. No one can register for our service. This is a critical blocker that is costing us money.*
- **D)** *The mobile signup button doesn't work. It worked yesterday but it's not working now. I think it might be a CSS styling issue or a problem with the layout.*
