import sys
from structure.matrix.ListMatrix import ListMatrix
from utility_algorithms.MathUtils import MathUtils


class AssignmentProblem:
    # https://ru.wikipedia.org/wiki/Венгерский_алгоритм
    # https://en.wikipedia.org/wiki/Hungarian_algorithm 

    # One of these (Which is?)
    # Original Hungarian method or Kuhn-Munkres algorithm - O(n4)
    # Modified Hungarian method or Hopcroft–Karp algorithm - O(n3)

    @staticmethod
    def HungarianAlgorithm(matrix: ListMatrix):
        mx = matrix.clone()
        u = [0] * (mx.rows + 1)
        v = [0] * (mx.cols + 1)
        p = [0] * (mx.cols + 1)
        minv = [sys.maxsize] * (mx.cols + 1)
        way = [0] * (mx.cols + 1)
        used = [False] * (mx.cols + 1)

        # рассматриваем строки матрицы matrix
        for i in range(1, mx.rows + 1, 1):
            p[0] = i # для удобства реализации 
            j0 = 0 # свободный столбец

            # заполняем массивы minv — Ininity, used — false
            for k in range(0, len(minv), 1):
                minv[k] = sys.maxsize

            for k in range(0, len(used), 1):
                used[k] = False

            count = 0
            while p[j0] != 0: # ищем свободный столбец 
                count += 1
                # помечаем посещенными столбец j0 и строку i0
                used[j0] = True
                i0 = p[j0]
                delta = sys.maxsize
                j1 = 0

                # пересчитываем массив minv, находим в нем минимум delta (изначально Ininity) и столбец j1, в котором он достигнут
                for j in range(1, mx.cols + 1, 1):
                    if not used[j]:
                        cur = mx.get(i0 - 1, j - 1) - u[i0] - v[j]
                        if cur < minv[j]:
                            minv[j] = cur
                            way[j] = j0
                        if minv[j] < delta:
                            delta = minv[j]
                            j1 = j

                for j in range(0, mx.cols + 1, 1):
                    if used[j]:
                        u[p[j]] += delta
                        v[j] -= delta
                    else:
                        minv[j] -= delta
                j0 = j1

            while j0:
                j1 = way[j0]
                p[j0] = p[j1]
                j0 = j1

        result = []
        for i in range(1, mx.cols + 1, 1):
            result.append((i - 1, p[i] - 1, mx.get(i - 1, p[i] - 1)))

        return result


    @staticmethod
    def HungarianAlgorithmV0(matrix: ListMatrix):
        mx = matrix.clone()
        mx_marks = ListMatrix(mx.cols, mx.rows, fill_with=False)
        assigned_columns = [False] * mx.cols
        assigned_rows = [False] * mx.rows

        count = 0
        while True:
            AssignmentProblem._i_substract_minimums(mx)
            AssignmentProblem._ii_get_single_assigned_zeros_marked(mx, mx_marks, assigned_columns, assigned_rows)

            # None was assigned
            # So there are too many zeros
            print('assigned_columns', assigned_columns)
            if not any(assigned_columns):
                if mx.is_zero:
                    return AssignmentProblem._diagonal_as_result(matrix)
                else:
                    print('Too many zeros >>>>>')
                    # TODO: add another way to assign elements

            if AssignmentProblem._iii_test_zeros_marked(mx_marks):
                break

            cols_containing_zeros, rows_containing_zeros = AssignmentProblem._iv_min_stripes_to_cover_all_zeros(mx, mx_marks, assigned_rows)
            AssignmentProblem._v_substract_from_uncovered_and_add_to_crossed(
                AssignmentProblem._v_find_min_on_uncovered(mx, cols_containing_zeros, rows_containing_zeros),
                mx, 
                cols_containing_zeros, 
                rows_containing_zeros
            )

            count += 1

        # Collect result list:
        result = []
        for i in range(0, mx_marks.cols, 1):
            for j in range(0, mx_marks.rows, 1):
                if mx_marks.get(i, j):
                    result.append((i, j, matrix.get(i, j)))

        return result

    def _i_substract_minimums(mx: ListMatrix):
        row_or_col = [0] * mx.rows

        # I.1. Substract minimum from every row
        for j in range(0, mx.rows, 1):
            for i in range(0, mx.cols, 1):
                row_or_col[i] = mx.get(i, j)
            row_min, _ = MathUtils.find_min(row_or_col)

            for i in range(0, mx.cols, 1):
                mx.set(i, j, row_or_col[i] - row_min)

        print('I.1.', mx)

        # I.2. Substract minimum from every column
        for i in range(0, mx.cols, 1):
            for j in range(0, mx.rows, 1):
                row_or_col[j] = mx.get(i, j)
            col_min, _ = MathUtils.find_min(row_or_col)

            for j in range(0, mx.rows, 1):
                mx.set(i, j, row_or_col[j] - col_min)

        print('I.2.', mx)

        return mx
    
    def _ii_get_single_assigned_zeros_marked(mx: ListMatrix, mx_marks: ListMatrix, assigned_columns: list, assigned_rows: list):
        # II. Analyse: 

        # clear mx_marks, assigned_columns, assigned_rows
        for i in range(0, mx_marks.cols, 1):
            assigned_columns[i] = False
            assigned_rows[i] = False
            for j in range(0, mx_marks.rows, 1):
                mx_marks.set(i, j, False)

        # II.1. Mark single unmarked zero in a row to a column (task)
        for j in range(0, mx.rows, 1):
            zero_i = -1
            for i in range(0, mx.cols, 1):
                if mx.get(i, j) == 0 and not mx_marks.get(i, j) and not assigned_columns[i]:
                    if zero_i < 0:
                        zero_i = i
                    else:
                        # when zero is not single
                        zero_i = mx.cols + 1
            if zero_i > -1 and zero_i < mx.cols:
                mx_marks.set(zero_i, j, True)
                assigned_columns[zero_i] = True
                assigned_rows[j] = True

        print('II.1.', mx_marks, assigned_columns)

        # II.2. Mark single unmarked zero in a column to a column (task)
        for i in range(0, mx.cols, 1):
            zero_j = -1
            for j in range(0, mx.rows, 1):
                if mx.get(i, j) == 0 and not mx_marks.get(i, j) and not assigned_columns[i] and not assigned_rows[j]:
                    if zero_j < 0:
                        zero_j = j
                    else:
                        # when zero is not single
                        zero_j = mx.rows + 1
            if zero_j > -1 and zero_j < mx.rows:
                mx_marks.set(i, zero_j, True)
                assigned_columns[i] = True
                assigned_rows[zero_j] = True


        print('II.2.', mx_marks, assigned_columns, assigned_rows)

        return mx_marks, assigned_columns, assigned_rows

    def _iii_test_zeros_marked(mx_marks) -> bool:
        # III. Verify if all the rows and all the columns contain single marked zero
        failed = False
        contains_mark = False
        for j in range(0, mx_marks.rows, 1):
            contains_mark = False
            for i in range(0, mx_marks.cols, 1):
                if mx_marks.get(i, j):
                    contains_mark = True
                    continue

            if not contains_mark:
                failed = True
                break

        if failed:
            return False
        
        for i in range(0, mx_marks.cols, 1):
            contains_mark = False
            for j in range(0, mx_marks.rows, 1):
                if mx_marks.get(i, j):
                    contains_mark = True
                    continue

            if not contains_mark:
                failed = True
                break

        return not failed

    def _iv_min_stripes_to_cover_all_zeros(mx: ListMatrix, mx_marks: ListMatrix, assigned_rows: list):
        marked_columns = [False] * mx.cols
        marked_rows_inverted = [True] * mx.rows

        for j in range(0, mx.rows, 1):
            # IV.1. Unmark not assigned rows
            if not assigned_rows[j]:
                marked_rows_inverted[j] = False

                # IV.2. Mark columns containing zeros on these unmarked rows
                for i in range(0, mx.cols, 1):
                    if mx.get(i, j) == 0:
                        marked_columns[i] = True
        print('IV.1. marked_columns', marked_columns)

        # IV.3. Mark columns containing zeros on these unmarked rows
        for i in range(0, mx.cols, 1):
            if marked_columns[i]:
                for j in range(0, mx.rows, 1):
                    if mx.get(i, j) == 0 and mx_marks.get(i, j): # Mark assigned zeros in that column
                        marked_rows_inverted[j] = False
        print('IV.2. both', marked_columns, marked_rows_inverted)

        return marked_columns, marked_rows_inverted

    def _v_find_min_on_uncovered(mx, cols_covered, rows_covered):
        min = sys.maxsize
        for i in range(0, mx.cols, 1):
            if cols_covered[i]:
                continue
            for j in range(0, mx.rows, 1):
                if rows_covered[j]:
                    continue
                val = mx.get(i, j)
                if val < min:
                    min = val

        print('V. Min:', min)

        return min

    def _v_substract_from_uncovered_and_add_to_crossed(diff, mx, cols_covered, rows_covered):
        for i in range(0, mx.cols, 1):
            for j in range(0, mx.rows, 1):
                # V.1. Substract from uncovered elements
                if not cols_covered[i] and not rows_covered[j]:
                    mx.set(i, j, mx.get(i, j) - diff)
                # V.2. Add to elements at crosses
                elif cols_covered[i] and rows_covered[j]:
                    mx.set(i, j, mx.get(i, j) + diff)

        print('V.', mx)

        return mx

    def _diagonal_as_result(matrix: ListMatrix):
        result = []
        for i in range(0, matrix.cols, 1):
            result.append((i, i, matrix.get(i, i)))

        return result



