#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модульные тесты для Expense Tracker
Автор: Вавилин Матвей
"""

import unittest
import json
import os
import tempfile
from datetime import datetime
from expense_tracker import ExpenseTrackerApp


class TestExpenseTracker(unittest.TestCase):
    """Тестовый класс для Expense Tracker"""
    
    def setUp(self):
        """Подготовка к тестам"""
        self.app = ExpenseTrackerApp()
        self.app.expenses = []
        self.app.data_file = tempfile.mktemp(suffix='.json')
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.app.data_file):
            os.remove(self.app.data_file)
    
    # ========== ПОЗИТИВНЫЕ ТЕСТЫ (5) ==========
    
    def test_pos_01_add_valid_expense(self):
        """POS-01: Добавление расхода с корректными данными"""
        self.app.amount_entry.insert(0, "500")
        self.app.category_combo.set("Food")
        self.app.date_entry.delete(0, 'end')
        self.app.date_entry.insert(0, "2026-04-30")
        
        self.app.add_expense()
        
        self.assertEqual(len(self.app.expenses), 1)
        self.assertEqual(self.app.expenses[0]['amount'], 500)
        self.assertEqual(self.app.expenses[0]['category'], "Food")
    
    def test_pos_02_validate_correct_amount(self):
        """POS-02: Валидация корректной суммы"""
        is_valid, result = self.app.validate_input("100", "2026-04-30")
        self.assertTrue(is_valid)
        self.assertEqual(result, 100)
    
    def test_pos_03_filter_by_category(self):
        """POS-03: Фильтрация по категории"""
        self.app.expenses = [
            {'id': 1, 'amount': 100, 'category': 'Food', 'date': '2026-04-01'},
            {'id': 2, 'amount': 200, 'category': 'Transport', 'date': '2026-04-02'}
        ]
        self.app.filter_category.set("Food")
        filtered = self.app.get_filtered_expenses()
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['category'], "Food")
    
    def test_pos_04_calculate_total(self):
        """POS-04: Подсчёт общей суммы"""
        self.app.expenses = [
            {'id': 1, 'amount': 100, 'category': 'Food', 'date': '2026-04-01'},
            {'id': 2, 'amount': 200, 'category': 'Transport', 'date': '2026-04-02'},
            {'id': 3, 'amount': 300, 'category': 'Entertainment', 'date': '2026-04-03'}
        ]
        self.app.refresh_table()
        total = sum(e['amount'] for e in self.app.expenses)
        self.assertEqual(total, 600)
    
    def test_pos_05_save_and_load_json(self):
        """POS-05: Сохранение и загрузка JSON"""
        test_data = [{'id': 1, 'amount': 150, 'category': 'Food', 'date': '2026-04-01'}]
        self.app.expenses = test_data
        self.app.save_data()
        
        self.app.load_data()
        self.assertEqual(len(self.app.expenses), 1)
        self.assertEqual(self.app.expenses[0]['amount'], 150)
    
    # ========== НЕГАТИВНЫЕ ТЕСТЫ (5) ==========
    
    def test_neg_01_negative_amount(self):
        """NEG-01: Отрицательная сумма"""
        self.app.amount_entry.insert(0, "-100")
        self.app.category_combo.set("Food")
        self.app.date_entry.insert(0, "2026-04-30")
        
        self.app.add_expense()
        self.assertEqual(len(self.app.expenses), 0)
    
    def test_neg_02_zero_amount(self):
        """NEG-02: Нулевая сумма"""
        self.app.amount_entry.insert(0, "0")
        self.app.category_combo.set("Food")
        
        self.app.add_expense()
        self.assertEqual(len(self.app.expenses), 0)
    
    def test_neg_03_text_in_amount(self):
        """NEG-03: Текст вместо суммы"""
        self.app.amount_entry.insert(0, "abc")
        self.app.category_combo.set("Food")
        
        self.app.add_expense()
        self.assertEqual(len(self.app.expenses), 0)
    
    def test_neg_04_wrong_date_format(self):
        """NEG-04: Неверный формат даты"""
        self.app.amount_entry.insert(0, "500")
        self.app.category_combo.set("Food")
        self.app.date_entry.delete(0, 'end')
        self.app.date_entry.insert(0, "30-04-2026")
        
        self.app.add_expense()
        self.assertEqual(len(self.app.expenses), 0)
    
    def test_neg_05_delete_without_selection(self):
        """NEG-05: Удаление без выбора записи"""
        initial_count = len(self.app.expenses)
        self.app.delete_expense()
        self.assertEqual(len(self.app.expenses), initial_count)
    
    # ========== ГРАНИЧНЫЕ ТЕСТЫ (5) ==========
    
    def test_bnd_01_very_large_amount(self):
        """BND-01: Очень большая сумма"""
        is_valid, result = self.app.validate_input("9999999", "2026-04-30")
        self.assertTrue(is_valid)
    
    def test_bnd_02_maximum_amount(self):
        """BND-02: Максимальная сумма"""
        is_valid, result = self.app.validate_input("10000000", "2026-04-30")
        self.assertTrue(is_valid)
    
    def test_bnd_03_exceeds_limit(self):
        """BND-03: Сумма больше лимита"""
        is_valid, result = self.app.validate_input("10000001", "2026-04-30")
        self.assertFalse(is_valid)
    
    def test_bnd_04_empty_fields(self):
        """BND-04: Пустые поля"""
        self.app.add_expense()
        self.assertEqual(len(self.app.expenses), 0)
    
    def test_bnd_05_filter_no_results(self):
        """BND-05: Фильтр без результатов"""
        self.app.expenses = [
            {'id': 1, 'amount': 100, 'category': 'Food', 'date': '2026-04-01'}
        ]
        self.app.filter_category.set("Transport")
        filtered = self.app.get_filtered_expenses()
        self.assertEqual(len(filtered), 0)


def run_tests():
    """Запуск всех тестов"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestExpenseTracker)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    print(f"Total tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures) + len(result.errors)}")
    
    return result


if __name__ == "__main__":
    run_tests()
