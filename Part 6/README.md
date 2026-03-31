# 🐍 Python Bootcamp — Project 02

## 📌 Overview

This project demonstrates practical usage of multiple programming paradigms in Python:

* Object-Oriented Programming (OOP)
* Procedural Programming
* Functional Programming
* Multiparadigm Design
* Asynchronous Programming

The project consists of two independent tasks:

1. **Exam Simulation System** [link](./01/main.py)
2. **Asynchronous Image Downloader** [link](./02/main.py)

---

# 🎓 Task 1 — Exam Simulation

## 📖 Description

This task simulates a real-time exam process where:

* Students wait in a shared queue
* Multiple examiners process students simultaneously
* Each examiner runs in a **separate process**
* The system updates live exam status in the console

---

## ⚙️ How It Works

### 👨‍🎓 Students

* Stored in `students.txt`
* Each student has:

  * Name
  * Gender (affects answer probability)

### 👨‍🏫 Examiners

* Loaded from `examiners.txt`
* Each examiner:

  * Works independently (multiprocessing)
  * Takes breaks after 30 seconds
  * Has dynamic exam duration based on name length

### ❓ Questions

* Loaded from `questions.txt`
* Each student:

  * Gets 3 random questions
  * Answers by selecting random words
  * Uses **golden ratio probability distribution**

---

## 🧠 Exam Logic

### ✅ Answer Evaluation

* Examiner randomly selects correct answers
* Student passes if:

  * More correct answers than incorrect (neutral mood)
  * OR examiner is in good mood (25%)

### ❌ Failure Cases

* Automatic fail if examiner is in bad mood (12.5%)

---

## 🔄 Real-Time Output

During execution:

* 📊 Student Table:

  * In Queue
  * Passed
  * Failed

* 👨‍🏫 Examiner Table:

  * Current student
  * Total processed
  * Failed count
  * Work time

* ⏱ Timer and queue status updated **in-place**

---

## 🏁 Final Output

After completion:

* Final student results
* Examiner statistics
* Total exam duration
* 🥇 Top-performing students
* 👨‍🏫 Best examiners (lowest failure rate)
* ⚠️ Expelled students
* ⭐ Best questions
* 📊 Final success rate (>85% = success)

---

**Input**

| examiners.txt |
| --- |
| Stepan M<br>Darya F<br>Mikhail M |

| students.txt |
| --- |
| Petr M<br>Sergey M<br>Varvara F<br><br>Ivan M<br>Ekaterina F<br>Alexandra F<br>Aleksey M |

| questions.txt |
| --- |
| There is a table<br>A man is a dog’s friend<br>Solar eclipses affect people<br>Programming is an interesting activity |

**Output**

During exam

```
+------------+----------+
| Student    |  Status  |
+------------+----------+
| Aleksey    | In queue |
| Petr       |  Passed  |
| Ivan       |  Passed  |
| Ekaterina  |  Passed  |
| Sergey     |  Failed  |
| Varvara    |  Failed  |
| Alexandra  |  Failed  |
+------------+----------+

+-------------+-----------------+-----------------+---------+--------------+
| Examiner    | Current student | Total students  | Failed  | Work time    |
+-------------+-----------------+-----------------+---------+--------------+
| Stepan      | Aleksey         |        1        |    0    |    12.31     |
| Darya       | -               |        3        |    2    |    12.14     |
| Mikhail     | -               |        2        |    1    |     7.21     |
+-------------+-----------------+-----------------+---------+--------------+

Remaining in queue: 1 out of 7
Time since exam started: 12.31

```

After exam

```
+------------+----------+
| Student    |  Status  |
+------------+----------+
| Petr       |  Passed  |
| Ivan       |  Passed  |
| Ekaterina  |  Passed  |
| Sergey     |  Failed  |
| Varvara    |  Failed  |
| Alexandra  |  Failed  |
| Aleksey    |  Failed  |
+------------+----------+

+-------------+-----------------+---------+--------------+
| Examiner    | Total students  | Failed  | Work time    |
+-------------+-----------------+---------+--------------+
| Stepan      |        2        |    1    |    12.35     |
| Darya       |        3        |    2    |    12.14     |
| Mikhail     |        2        |    1    |     7.21     |
+-------------+-----------------+---------+--------------+

Time from exam start to finish: 12.35  
Top-performing students: Ivan  
Top examiners: Stepan, Mikhail  
Students to be expelled: Varvara  
Best questions: There is a table, A man is a dog’s friend  
Result: Exam failed
```

--- 

## 🚀 Key Concepts Used

* Multiprocessing (`multiprocessing`)
* Synchronization (queues, locks)
* OOP design (Student, Examiner classes)
* Randomized simulation
* Real-time console rendering

---

# 🖼 Task 2 — Async Image Downloader

## 📖 Description

An asynchronous program that downloads images from user-provided URLs.

---

## ⚙️ Features

* ⚡ Asynchronous downloads using `asyncio`
* 🌐 Multiple downloads run concurrently
* 🧾 Error handling (program never crashes)
* 📂 Custom save directory
* 🔁 Continuous input until empty line

---

## 🧠 Workflow

1. User enters download folder
2. Program validates path
3. User inputs image URLs one by one
4. Each URL is:

   * Immediately scheduled for download
   * Downloaded asynchronously
5. After empty input:

   * Program waits for all downloads to finish

---

## 📊 Output Summary

At the end:

```
+--------------------------------------+--------+
| Link                                 | Status |
+--------------------------------------+--------+
| valid_link.jpg                       | Success|
| invalid_link.png                     | Error  |
+--------------------------------------+--------+
```

---

## 🚀 Key Concepts Used

* `asyncio` event loop
* `aiohttp` for HTTP requests
* Task scheduling (`asyncio.create_task`)
* Error handling in async environment
* File handling and validation

---

# 💡 What I Learned

* How to combine **multiple programming paradigms**
* Writing **clean and modular code**
* Working with:

  * Processes (Task 1)
  * Async tasks (Task 2)
* Handling real-world problems:

  * Concurrency
  * Synchronization
  * Error handling
* Designing scalable systems

---

# ▶️ How to Run

## Task 1

```bash
pip install prettytable
cd ./01
python3 main.py
```

## Task 2

```bash
pip install prettytable requests
cd ./02
python3 main.py
```

---

# 📌 Notes

* Code follows project structure requirements
* No unnecessary files included

---

# ⭐ Conclusion

This project provides hands-on experience with:

* Real-time system simulation
* Concurrent and asynchronous programming
* Writing production-like Python applications

---

🚀 *Feel free to explore, modify, and improve the project!*
