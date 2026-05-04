#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expense Tracker - приложение для отслеживания личных расходов
Автор: Вавилин Матвей
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ExpenseTrackerApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Expense Tracker - Track your expenses")
        self.root.geometry("950x650")
        self.root.resizable(True, True)
        
        self.expenses = []
        self.data_file = "expenses.json"
        
        self.categories = ["Food", "Transport", "Entertainment", "Utilities", 
                          "Clothing", "Health", "Education", "Other"]
        
        self.load_data()
        self.create_widgets()
        self.refresh_table()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add expense section
        add_frame = ttk.LabelFrame(main_frame, text="Add Expense", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 10))
        
        row1 = ttk.Frame(add_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Amount (RUB):", width=12).pack(side=tk.LEFT, padx=5)
        self.amount_entry = ttk.Entry(row1, width=20)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="Category:", width=12).pack(side=tk.LEFT, padx=5)
        self.category_combo = ttk.Combobox(row1, values=self.categories, width=20)
        self.category_combo.pack(side=tk.LEFT, padx=5)
        self.category_combo.set("Food")
        
        row2 = ttk.Frame(add_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Date (YYYY-MM-DD):", width=15).pack(side=tk.LEFT, padx=5)
        self.date_entry = ttk.Entry(row2, width=15)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(row2, text="Add Expense", command=self.add_expense).pack(side=tk.LEFT, padx=20)
        
        # Filter section
        filter_frame = ttk.LabelFrame(main_frame, text="Filter", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        filter_row = ttk.Frame(filter_frame)
        filter_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_row, text="Category:").pack(side=tk.LEFT, padx=5)
        self.filter_category = ttk.Combobox(filter_row, values=["All"] + self.categories, width=15)
        self.filter_category.pack(side=tk.LEFT, padx=5)
        self.filter_category.set("All")
        
        ttk.Label(filter_row, text="Date from:").pack(side=tk.LEFT, padx=5)
        self.filter_date_from = ttk.Entry(filter_row, width=10)
        self.filter_date_from.insert(0, "2024-01-01")
        self.filter_date_from.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_row, text="Date to:").pack(side=tk.LEFT, padx=5)
        self.filter_date_to = ttk.Entry(filter_row, width=10)
        self.filter_date_to.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.filter_date_to.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_row, text="Apply Filter", command=self.apply_filter).pack(side=tk.LEFT, padx=10)
        ttk.Button(filter_row, text="Reset Filter", command=self.reset_filter).pack(side=tk.LEFT, padx=5)
        
        # Statistics section
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        stats_row = ttk.Frame(stats_frame)
        stats_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(stats_row, text="Total Amount:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.total_label = ttk.Label(stats_row, text="0 RUB", font=('Arial', 12, 'bold'), foreground='green')
        self.total_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(stats_row, text="Period Total:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=20)
        self.period_total_label = ttk.Label(stats_row, text="0 RUB", font=('Arial', 12, 'bold'), foreground='blue')
        self.period_total_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(stats_row, text="Records:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=20)
        self.count_label = ttk.Label(stats_row, text="0", font=('Arial', 10))
        self.count_label.pack(side=tk.LEFT, padx=5)
        
        # Expenses table
        table_frame = ttk.LabelFrame(main_frame, text="Expenses List", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        columns = ("ID", "Date", "Category", "Amount (RUB)")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount (RUB)", text="Amount (RUB)")
        
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=120)
        self.tree.column("Category", width=150)
        self.tree.column("Amount (RUB)", width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Data", command=self.save_data).pack(side=tk.LEFT, padx=5)
    
    def validate_input(self, amount, date_str):
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                return False, "Amount must be positive"
            if amount_float > 10000000:
                return False, "Amount is too large"
        except ValueError:
            return False, "Amount must be a number"
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        return True, amount_float
    
    def add_expense(self):
        amount = self.amount_entry.get().strip()
        category = self.category_combo.get()
        date = self.date_entry.get().strip()
        
        is_valid, result = self.validate_input(amount, date)
        if not is_valid:
            messagebox.showerror("Input Error", result)
            return
        
        amount_float = result
        
        if self.expenses:
            expense_id = max(e['id'] for e in self.expenses) + 1
        else:
            expense_id = 1
        
        self.expenses.append({
            'id': expense_id,
            'amount': amount_float,
            'category': category,
            'date': date
        })
        
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("Food")
        
        self.save_data()
        self.refresh_table()
        
        messagebox.showinfo("Success", f"Expense {amount_float:.2f} RUB added!")
    
    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to delete")
            return
        
        item = self.tree.item(selected[0])
        expense_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this expense?"):
            self.expenses = [e for e in self.expenses if e['id'] != expense_id]
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Success", "Expense deleted")
    
    def apply_filter(self):
        self.refresh_table()
    
    def reset_filter(self):
        self.filter_category.set("All")
        self.filter_date_from.delete(0, tk.END)
        self.filter_date_from.insert(0, "2024-01-01")
        self.filter_date_to.delete(0, tk.END)
        self.filter_date_to.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.refresh_table()
    
    def get_filtered_expenses(self):
        filtered = self.expenses.copy()
        
        category_filter = self.filter_category.get()
        if category_filter != "All":
            filtered = [e for e in filtered if e['category'] == category_filter]
        
        date_from = self.filter_date_from.get().strip()
        date_to = self.filter_date_to.get().strip()
        
        if date_from:
            filtered = [e for e in filtered if e['date'] >= date_from]
        if date_to:
            filtered = [e for e in filtered if e['date'] <= date_to]
        
        return filtered
    
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered = self.get_filtered_expenses()
        filtered.sort(key=lambda x: x['date'], reverse=True)
        
        for expense in filtered:
            self.tree.insert("", tk.END, values=(
                expense['id'],
                expense['date'],
                expense['category'],
                f"{expense['amount']:.2f}"
            ))
        
        total = sum(e['amount'] for e in self.expenses)
        period_total = sum(e['amount'] for e in filtered)
        count = len(filtered)
        
        self.total_label.config(text=f"{total:.2f} RUB")
        self.period_total_label.config(text=f"{period_total:.2f} RUB")
        self.count_label.config(text=str(count))
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.expenses = json.load(f)
            except:
                self.expenses = []
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Success", "Data saved!")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    print("Starting Expense Tracker...")
    app = ExpenseTrackerApp()
    app.run()
