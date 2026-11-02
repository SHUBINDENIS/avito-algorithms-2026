# Алгоритмы на Python

Домашние задания курса «Алгоритмы на Python» (Образование Авито), осень 2026.

## Структура

Одна папка на домашнее задание, внутри — папка на каждую задачу:

```
homework_1/
├── palindrome/
├── sum/
└── prime/
homework_2/
├── stack_vs_queue/
├── validate/
└── merge_lists/
homework_3/
├── two_sum/
├── anagrams/
└── hash_table/
homework_4/
└── Binary_Tree/
    ├── tree_traversal/
    ├── validate_bst/
    └── balanced_tree/
homework_5/
├── tracer/
├── permutations/
└── AVL/
```

В каждой папке задачи:

- `solution.py` — решение;
- `test_solution.py` — тесты;
- `README.md` — условие, идея алгоритма, оценка сложности и разбор на примере.

## Запуск тестов

Тесты каждой задачи независимы и не требуют дополнительных пакетов:

```
python homework_1/palindrome/test_solution.py -v
python homework_1/sum/test_solution.py -v
python homework_1/prime/test_solution.py -v
python homework_2/stack_vs_queue/test_solution.py -v
python homework_2/validate/test_solution.py -v
python homework_2/merge_lists/test_solution.py -v
python homework_3/two_sum/test_solution.py -v
python homework_3/anagrams/test_solution.py -v
python homework_3/hash_table/test_solution.py -v
python homework_4/Binary_Tree/tree_traversal/test_solution.py -v
python homework_4/Binary_Tree/validate_bst/test_solution.py -v
python homework_4/Binary_Tree/balanced_tree/test_solution.py -v
python homework_5/tracer/test_solution.py -v
python homework_5/permutations/test_solution.py -v
python homework_5/AVL/test_solution.py -v
```

Для запуска тестов одной задачи выполните соответствующую строку из списка.
