# [Setup](README.md) | [Development](README_DEV.md)

## 1. Install Python

### **Windows:**
Download latest Python (3.5) from <https://www.python.org/downloads/>
and run the installer.

### **macOS:**
macOS comes with Python 2.7 but we want to use Python 3.5.

If you have [Homebrew](http://brew.sh/) installed you can use this
command to install latest Python:

        brew install python3

Otherwise, you can download latest Python from <https://www.python.org/downloads/>.

---

## 2. Make a GitHub account and install Git
Go to <https://github.com> and create a new account if you don't already have one.

The easiest way to use git is by installing [GitHub Desktop](https://desktop.github.com/).

## 3. Install Django

### **Windows:**
Open command prompt and type:

        pip install Django

### **macOS:**
Open terminal and type:

        pip3 install Django

---

## 4. Clone repository
Go to <https://github.com/ilmaria/design_www> and clone the repository to your computer.

---

### **macOS:**
In this guide, every `python` command should be replace with `python3` in macOS.
For example on Windows you would write:

        python manage.py migrate

But on macOS you write:

        python3 manage.py migrate

---

## 5. Prepare database
Go to your local cloned repository with terminal or command prompt. Use `"` marks around your path
if it has whitespaces (For example, `cd "My Documents/design_www"`):

        cd your/repo/path

Run migration command to initialize database:

        python manage.py migrate

---

## 6. Create admin account (optional)
To create an admin account to manage database run the following command:

        python manage.py createsuperuser

Fill in desired username and press enter

        Username: admin

Next, you are asked to fill in an email

        Email address: admin@example.com

And the final step is giving a password. The password field will remain blank
while you are typing but it will still register your key presses.

        Password:
        Password (again):
        Superuser created successfully.

---

### [> Development instructions](README_DEV.md)
### [> Git guide](README_GIT.md)
