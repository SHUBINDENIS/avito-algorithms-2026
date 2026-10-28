# Домашнее задание №4. Binary Tree

Бинарные деревья.

| Задача | Папка | Что внутри |
|---|---|---|
| 1. Tree Traversal | [tree_traversal](tree_traversal) | BST со вставкой и шесть обходов |
| 2. Validate BST | [validate_bst](validate_bst) | проверка, что дерево – корректное BST |
| 3. Balanced Binary Tree | [balanced_tree](balanced_tree) | проверка сбалансированности по высоте |

В каждой папке: `solution.py` – решение, `test_solution.py` – тесты, `README.md` – идея, оценка сложности и пошаговый разбор на примере.

Все три решения обходят дерево явным стеком, без рекурсии: у вырожденного дерева глубина равна числу узлов и может превысить лимит рекурсии Python.

Срок сдачи – 28 октября включительно.

Из корня репозитория:

```
python homework_4/Binary_Tree/tree_traversal/test_solution.py -v
python homework_4/Binary_Tree/validate_bst/test_solution.py -v
python homework_4/Binary_Tree/balanced_tree/test_solution.py -v
```

Примеры в консоль: `python homework_4/Binary_Tree/<задача>/solution.py`.
