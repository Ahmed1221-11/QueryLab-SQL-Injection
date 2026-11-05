# QueryLab - SQL Injection: Attack and Repair
ECE4113 - Secure Software Development

## Windows: start here
1. Extract the ZIP (do not run from inside the ZIP).
2. Double-click START_WINDOWS.bat. Python is already installed if the previous project ran.
3. A browser opens at http://127.0.0.1:8765. Keep the command window open.
4. If it does not open, enter that address manually in your browser.
5. Stop the server with Ctrl+C in the command window.

Alternative: open a terminal in the extracted folder and run `py app.py`.
On macOS/Linux use `python3 app.py`. Requires Python 3.9+ with sqlite3;
no pip packages, database server or internet connection are needed.
Do not open index.html directly: the Python server handles real SQLite queries.

## Live demonstration
Click a preset, then Run both versions. Presets only fill inputs: results are
computed by SQLite on the Python backend, not hard-coded by JavaScript.

| Preset | Vulnerable | Fixed |
|---|---|---|
| Valid credentials | Access granted | Access granted |
| Wrong password | Access denied | Access denied |
| Injection attempt | Access granted (admin) | Access denied |

The local attack input is username `admin' -- ` (a space after the two hyphens)
and password `wrong-password`. Expand Inspect SQL & parameters to explain it.
You may also type your own local demo inputs. Reset clears results and loads
wrong credentials. Changes do not persist: SQLite is recreated per attempt.

Test accounts: admin / AdminDemo42! and student / StudyDemo42!.
These are fictional, public demonstration credentials.

## Files and validation
- app.py: HTTP routes, disposable database, vulnerable and parameterized queries.
- index.html: browser interface with two forms and inspectable queries.
- test_app.py: seven automated backend tests.
- Report.pdf / Report.md: three-page report and editable source.
- Arabic_Guide.md: code explanation and viva questions.

Run `py -m unittest -v` in this folder (or python3 instead of py).

## Scope and limitations
This project implements an active SQL injection login-bypass attack against its
own local target, and demonstrates the parameterized-query repair. It is not a
production authentication system. It creates no sessions or protected dashboard.
Passwords are plaintext solely to keep the SQL example small; real systems must
use appropriate salted password hashing, session management and other controls.
The 'fixed' label means this query is fixed against this injection, not that the
whole application is secure. SQL errors and queries are deliberately visible
for teaching; production systems should not expose them.
The server binds only to 127.0.0.1. Do not expose the vulnerable lab to a network.
All demonstrations concern the included dummy accounts only.

## Submission
Confirm the new SQL Injection topic with the TA before submission. Fill in both
students' names, IDs and actual contributions in the report; update the PDF to
match. Each member must understand all code. Submit before the Week 7 lab.
ChatGPT assistance is disclosed in the report, as the brief permits.

## Sources
- https://docs.python.org/3/library/sqlite3.html
- https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- Supplied ECE4113 project brief.
- OpenAI ChatGPT: assisted design, implementation, documentation and tests.
