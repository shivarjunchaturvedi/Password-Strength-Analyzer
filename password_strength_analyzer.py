import tkinter as tk
from tkinter import messagebox
import re
import random
import string

COMMON_PASSWORDS = [
    "123456", "password", "12345678",
    "qwerty", "abc123", "password123"
]

def analyze_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning("Warning", "Enter a password!")
        return

    score = 0
    suggestions = []

    if password.lower() in COMMON_PASSWORDS:
        result_label.config(
            text="❌ Common Password Detected!",
            fg="red"
        )
        score_label.config(text="Score: 0/100")
        suggestions_label.config(
            text="Use a unique password."
        )
        return

    if len(password) >= 8:
        score += 20
    else:
        suggestions.append("Use at least 8 characters")

    if len(password) >= 12:
        score += 20

    if re.search(r"[A-Z]", password):
        score += 15
    else:
        suggestions.append("Add uppercase letter")

    if re.search(r"[a-z]", password):
        score += 15
    else:
        suggestions.append("Add lowercase letter")

    if re.search(r"\d", password):
        score += 15
    else:
        suggestions.append("Add number")

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        score += 15
    else:
        suggestions.append("Add special character")

    if score <= 40:
        strength = "WEAK ❌"
        color = "red"
    elif score <= 70:
        strength = "MEDIUM ⚠️"
        color = "orange"
    else:
        strength = "STRONG ✅"
        color = "green"

    score_label.config(text=f"Score: {score}/100")
    result_label.config(text=f"Strength: {strength}", fg=color)

    if suggestions:
        suggestions_label.config(
            text="Suggestions:\n" + "\n".join(suggestions)
        )
    else:
        suggestions_label.config(
            text="Excellent Password! 🎉"
        )

def generate_password():
    chars = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*"
    )

    password = ''.join(
        random.choice(chars)
        for _ in range(12)
    )

    generated_password.config(
        text=f"Generated Password:\n{password}"
    )

root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("500x500")

title = tk.Label(
    root,
    text="Password Strength Analyzer",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

password_entry = tk.Entry(
    root,
    width=35,
    show="*",
    font=("Arial", 12)
)
password_entry.pack(pady=10)

check_btn = tk.Button(
    root,
    text="Check Strength",
    command=analyze_password
)
check_btn.pack(pady=5)

score_label = tk.Label(
    root,
    text="Score: 0/100",
    font=("Arial", 12)
)
score_label.pack()

result_label = tk.Label(
    root,
    text="Strength:",
    font=("Arial", 14, "bold")
)
result_label.pack(pady=10)

suggestions_label = tk.Label(
    root,
    text="",
    justify="left"
)
suggestions_label.pack(pady=10)

generate_btn = tk.Button(
    root,
    text="Generate Password",
    command=generate_password
)
generate_btn.pack(pady=10)

generated_password = tk.Label(
    root,
    text="",
    font=("Arial", 12)
)
generated_password.pack()

root.mainloop()