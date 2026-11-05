# SQL Injection: Login Bypass and Repair
ECE4113 - Secure Software Development | Course project

Students: ____________________ / ____________________
Student IDs: ____________________ / ____________________
Group: ____________________

## 1. Objective and scope
QueryLab implements one active security attack: SQL injection against a small login application that we control. A browser interface compares a deliberately vulnerable query with a parameterized version. The goal is to demonstrate bypassing a password check and explain why separating SQL structure from input values prevents that bypass. The application runs locally with fictional accounts only.

## 2. Architecture
The project uses Python's standard-library HTTP server and sqlite3 module, plus HTML, CSS and JavaScript. Running app.py opens http://127.0.0.1:8765. The server binds only to the loopback address. No external packages, online services or database installation are needed.

The browser sends a JSON request containing mode, username and password to /api/login. Python creates an in-memory SQLite database with two dummy accounts, executes the selected query and returns the result as JSON. The interface displays the matched account, query and parameters. Preset buttons only populate inputs; SQLite actually determines each result.

## 3. Threat model
The attacker controls login field values and knows the public test username admin, but submits an incorrect password. The intended rule requires both username and password to match. The vulnerable implementation lets input alter SQL syntax and remove the password condition. This is an active attack because it manipulates request interpretation and bypasses the intended check.

## 4. Database and authentication boundary
The users table contains id, username, password and role. The local database is recreated and closed for every attempt, so data cannot persist between demonstrations. A successful result means a row matched the query; the lab does not create sessions, protect resources or implement an actual account portal. The comparison isolates one SQL injection flaw rather than claiming a complete authentication product.
---PAGE---
# Exploit and implementation

## 5. Vulnerable query
The vulnerable branch builds this query by directly interpolating input:
SELECT id, username, role FROM users WHERE username = '<username>' AND password = '<password>'

For the local demonstration, the username is admin' -- followed by a space, and the password is wrong-password. The resulting SQL is:
SELECT id, username, role FROM users WHERE username = 'admin' -- ' AND password = 'wrong-password'

The quote terminates the username string. The two hyphens begin an SQL comment, so the password condition is ignored. The query matches the admin row even though the supplied password is incorrect. This attack does not discover or recover the password; it bypasses its check.

## 6. Parameterized repair
The repaired branch keeps a constant SQL template:
SELECT id, username, role FROM users WHERE username = ? AND password = ?

It executes db.execute(query, [username, password]). The driver binds the input as values separately from the SQL structure [1, 2]. Consequently the entire malicious username remains a literal value rather than executable syntax. No account has that name, and the login fails. The repair uses neither keyword blacklists nor manual quote removal.

## 7. Important functions
make_database creates the disposable database and seeds the fictional accounts using parameter binding. login selects the vulnerable or fixed query, calls execute and fetchone, and returns a structured result. It reports SQL errors in the lab and always closes the database in a finally block.

Handler.do_GET serves only the interface page. Handler.do_POST checks route, request size, field types and the browser Origin before running login. The interface uses fetch to call the server and textContent to display returned values without interpreting them as HTML. main opens the local browser and stops the server when Ctrl+C is pressed.

## 8. Live demonstration
First load Valid credentials and select Run both versions: both grant access. Next load Wrong password: both deny access. Finally load Injection attempt: the vulnerable version grants access as admin, while the fixed version denies access. Inspect the displayed query and separately bound parameters to explain the different results. Reset returns the interface to a clean display.
---PAGE---
# Validation, limits and sources

## 9. Validation
Seven automated backend test methods passed during preparation: valid credentials in both modes; wrong passwords in both; injection bypass only in the vulnerable mode; unknown and empty usernames; an apostrophe treated as data in the fixed mode; a fresh database after an attempt; and rejection of an invalid mode. Run py -m unittest -v in the extracted project folder.

An additional HTTP integration check loaded the actual page and submitted the same injection payload to both API modes. The vulnerable response accepted the admin row; the fixed response rejected it. These checks verify backend behavior and HTTP wiring. They do not constitute a production security audit or full cross-browser certification.

## 10. Limitations and responsible scope
The vulnerable branch is intentional and must stay local. Tests are limited to the included application and fictional accounts. SQL queries and errors are exposed for learning; real systems should not expose them. Passwords are stored as plaintext only to keep attention on SQL construction. A real application must use appropriate salted password hashing, secure sessions, rate limits and other authentication controls.

The fixed label refers specifically to parameterization of this query. It does not imply the whole web application is secure. Input length checks are supplementary and are not the SQL injection defense. The program has no production session, HTTPS deployment, protected dashboard or general-purpose penetration-testing functionality. SQLite query behavior demonstrated here should not be assumed identical across every SQL dialect.

## 11. Contributions and tool disclosure
Student 1 actual contribution: ___________________________________
Student 2 actual contribution: ___________________________________
Complete these details honestly after reviewing and running the project. Both team members must understand the entire code and answer viva questions independently. Confirm the revised topic with the TA before submission.

ChatGPT (OpenAI) assisted with design, implementation, tests, report and study guide. Python documentation informed sqlite3 API use, and OWASP informed the explanation of parameterized-query prevention. AI assistance is declared in line with the supplied project brief.

## 12. References
[1] Python Software Foundation. sqlite3 - DB-API 2.0 interface for SQLite databases. https://docs.python.org/3/library/sqlite3.html
[2] OWASP Cheat Sheet Series. SQL Injection Prevention Cheat Sheet. https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
[3] AASTMT. ECE4113 Course Project - Security Attacks & Services. Supplied brief.
[4] OpenAI. ChatGPT, project-development assistance. 28 October 2026.
