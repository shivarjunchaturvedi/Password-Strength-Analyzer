"""
Password Strength Analyzer — educational Tkinter application.

Passwords are analyzed locally and are not uploaded or stored.
This heuristic is not a password-breach check or a guarantee of security.
"""
import secrets
import string
import tkinter as tk
from tkinter import messagebox

COMMON_PASSWORDS = {
    "123456", "password", "12345678", "qwerty", "abc123",
    "password123", "admin", "letmein", "welcome", "iloveyou",
}
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?/\\|~"


def analyze_password(password: str) -> tuple[int, str, list[str]]:
    """Return a heuristic score, strength label, and helpful suggestions."""
    if not password:
        return 0, "EMPTY", ["Enter a password to analyze."]
    if password.casefold() in COMMON_PASSWORDS:
        return 0, "VERY WEAK", ["This is a commonly used password. Choose a unique, longer passphrase."]

    score = 0
    suggestions = []
    if len(password) >= 8:
        score += 20
    else:
        suggestions.append("Use at least 8 characters; a longer passphrase is preferable.")
    if len(password) >= 12:
        score += 20
    elif len(password) >= 8:
        suggestions.append("Consider using 12 or more characters.")

    checks = [
        (any(ch.isupper() for ch in password), 15, "Consider including an uppercase letter."),
        (any(ch.islower() for ch in password), 15, "Consider including a lowercase letter."),
        (any(ch.isdigit() for ch in password), 15, "Consider including a number."),
        (any(ch in SPECIAL_CHARACTERS for ch in password), 15, "Consider including a special character."),
    ]
    for passed, points, suggestion in checks:
        if passed:
            score += points
        else:
            suggestions.append(suggestion)

    strength = "WEAK" if score <= 40 else "MODERATE" if score <= 70 else "STRONG"
    return score, strength, suggestions


def generate_password(length: int = 16) -> str:
    """Generate a random password with secrets and all major character types."""
    if length < 12:
        raise ValueError("Password length must be at least 12 characters.")

    required = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(SPECIAL_CHARACTERS),
    ]
    alphabet = string.ascii_letters + string.digits + SPECIAL_CHARACTERS
    chars = required + [secrets.choice(alphabet) for _ in range(length - len(required))]
    for index in range(len(chars) - 1, 0, -1):
        swap_index = secrets.randbelow(index + 1)
        chars[index], chars[swap_index] = chars[swap_index], chars[index]
    return "".join(chars)


class PasswordStrengthApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Password Strength Analyzer")
        root.geometry("560x590")
        root.minsize(500, 540)
        root.configure(bg="#101827")

        tk.Label(root, text="Password Strength Analyzer",
                 font=("Segoe UI", 20, "bold"), fg="#f8fafc",
                 bg="#101827").pack(pady=(20, 4))
        tk.Label(root, text="Analyze locally on your device",
                 font=("Segoe UI", 10), fg="#a8b3c7",
                 bg="#101827").pack(pady=(0, 16))

        panel = tk.Frame(root, bg="#1b2638", padx=22, pady=18)
        panel.pack(fill="both", expand=True, padx=22, pady=(0, 20))
        tk.Label(panel, text="Enter password", font=("Segoe UI", 11, "bold"),
                 fg="#e5e7eb", bg="#1b2638").pack(anchor="w")

        entry_row = tk.Frame(panel, bg="#1b2638")
        entry_row.pack(fill="x", pady=(8, 12))
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            entry_row, textvariable=self.password_var, show="•",
            font=("Consolas", 13), relief="flat", bg="#0f1724",
            fg="#f8fafc", insertbackground="white"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))
        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            entry_row, text="Show", variable=self.show_var,
            command=self.toggle_visibility, fg="#cbd5e1", bg="#1b2638",
            selectcolor="#0f1724", activebackground="#1b2638",
            activeforeground="white"
        ).pack(side="right")

        tk.Button(panel, text="Analyze Password", command=self.check_strength,
                  font=("Segoe UI", 11, "bold"), bg="#1677ff", fg="white",
                  activebackground="#0b5ed7", activeforeground="white",
                  relief="flat", cursor="hand2", pady=9).pack(fill="x")

        self.score_label = tk.Label(panel, text="Score: — / 100",
                                    font=("Segoe UI", 13, "bold"),
                                    fg="#e5e7eb", bg="#1b2638")
        self.score_label.pack(pady=(18, 4))
        self.strength_label = tk.Label(panel, text="Strength: Not analyzed",
                                       font=("Segoe UI", 15, "bold"),
                                       fg="#94a3b8", bg="#1b2638")
        self.strength_label.pack(pady=4)
        self.suggestions_label = tk.Label(
            panel, text="Your password is analyzed locally; nothing is uploaded.",
            font=("Segoe UI", 10), fg="#cbd5e1", bg="#1b2638",
            justify="left", wraplength=450, anchor="w"
        )
        self.suggestions_label.pack(fill="x", pady=(8, 12))

        tk.Button(panel, text="Generate Secure Password (16 chars)",
                  command=self.create_password, font=("Segoe UI", 10, "bold"),
                  bg="#27364c", fg="#f8fafc", activebackground="#344760",
                  activeforeground="white", relief="flat", cursor="hand2",
                  pady=9).pack(fill="x")
        self.generated_var = tk.StringVar()
        tk.Entry(panel, textvariable=self.generated_var, state="readonly",
                 readonlybackground="#0f1724", fg="#93c5fd",
                 font=("Consolas", 11), relief="flat",
                 justify="center").pack(fill="x", pady=(10, 6), ipady=7)
        tk.Button(panel, text="Copy Generated Password",
                  command=self.copy_password, font=("Segoe UI", 9),
                  bg="#334155", fg="white", activebackground="#475569",
                  activeforeground="white", relief="flat",
                  cursor="hand2").pack(fill="x")

        self.password_entry.focus_set()
        root.bind("<Return>", lambda _event: self.check_strength())

    def toggle_visibility(self) -> None:
        self.password_entry.configure(show="" if self.show_var.get() else "•")

    def check_strength(self) -> None:
        password = self.password_var.get()
        if not password:
            self.score_label.configure(text="Score: — / 100")
            self.strength_label.configure(text="Strength: Enter a password", fg="#fbbf24")
            self.suggestions_label.configure(text="Type a password first, then select Analyze Password.")
            return

        score, strength, suggestions = analyze_password(password)
        colors = {"WEAK": "#f87171", "MODERATE": "#fbbf24",
                  "STRONG": "#4ade80", "VERY WEAK": "#f87171"}
        self.score_label.configure(text=f"Score: {score} / 100")
        self.strength_label.configure(text=f"Strength: {strength}", fg=colors[strength])
        message = "Suggestions:\n• " + "\n• ".join(suggestions) if suggestions else (
            "Composition checks passed. Prefer a unique, long password or passphrase."
        )
        self.suggestions_label.configure(text=message)

    def create_password(self) -> None:
        self.generated_var.set(generate_password())

    def copy_password(self) -> None:
        value = self.generated_var.get()
        if not value:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()
        messagebox.showinfo("Copied", "Generated password copied to the clipboard.")


def main() -> None:
    root = tk.Tk()
    PasswordStrengthApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
