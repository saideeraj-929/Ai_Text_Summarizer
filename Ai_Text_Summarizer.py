import tkinter as tk
import os
from groq import Groq
from tkinter import messagebox
# -----Window-----
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
window=tk.Tk()
window.title(" 🤖 AI Text Summarizer")
window.geometry("700x600")
window.config(bg="lavender")

SUMMARIZE_FILE="summarize.txt"
title=tk.Label(window,text="🤖 AI Text Summarizer",font=("Arial",18,"bold"))
title.pack(pady=5)
label=tk.Label(window,text="Paste your text here").pack(pady=5)
text_entry=tk.Text(window,height=6,width=60,)
text_entry.pack(pady=5)

# -----Functions-----
def save():
    summary = summary_view.get("1.0",tk.END)
    with open(SUMMARIZE_FILE,"w")as file:
        file.write(summary)
        messagebox.showinfo(
            "Success",
            "Text saved successfully!"
        )
def load():
    try:
        with open(SUMMARIZE_FILE,"r")as file:
            summary=file.read()
            summary_view.delete("1.0", tk.END)
            summary_view.insert( tk.END,summary)
        messagebox.showinfo("Success",
            "Text loaded successfully!"
         )
    except FileNotFoundError:
        messagebox.showerror("Error",
            "No saved text found"
         )
def clear():
        text_entry.delete("1.0", tk.END)
        summary_view.delete("1.0", tk.END)
def summarize():
    text = text_entry.get("1.0", tk.END).strip()
    if text=="":
        summary_view.delete("1.0", tk.END)
        summary_view.insert(tk.END, "Please enter some text.")
        return
    window.update()
    messages=[
        {
            "role":"system",
            "content":"""
            
You are an expert text summarizer.

Summarize the user's text into a short, clear, and easy-to-understand paragraph.

Do not add extra information.
Only summarize the given text.
"""
            
        
    },
        
    {
    "role": "user",
    "content": text
}
    ]
    try:
        response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
        )
        summary=response.choices[0].message.content
        summary_view.delete("1.0",tk.END)
        summary_view.insert(tk.END,summary)
    except Exception as e:
        summary_view.delete("1.0", tk.END)
        summary_view.insert(tk.END, f"Error:\n\n{e}")

# -----Buttons-----

summarize_button=tk.Button(window,text="Summarize",font=("Arial",12,"bold"),command=summarize)
summarize_button.pack(pady=5)
save_button=tk.Button(window,text="Save",font=("Arial",12,"bold"),command=save)
save_button.pack(pady=5)
load_button=tk.Button(window,text="Load",font=("Arial",12,"bold"),command=load)
load_button.pack(pady=5)
clear_button = tk.Button(
    window,
    text="Clear",
    command=clear
)
clear_button.pack(pady=5)
summary_label = tk.Label(
    window,
    text="Summary",
    font=("Arial", 12, "bold")
)
summary_label.pack()
summary_view=tk.Text(window,height=6,width=60,wrap="word")
summary_view.pack(pady=5)
load()
window.mainloop()

