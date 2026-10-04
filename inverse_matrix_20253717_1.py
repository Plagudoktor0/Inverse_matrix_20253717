def get_matrix():
    n = int(input("Enter the order of the square matrix: "))
    a = []
    for i in range(n):
        row = list(map(float, input(f"Row {i+1}: ").split()))
        a.append(row)
    return a


def det(a):
    n = len(a)
    if n == 1:
        return a[0][0]
    result = 0
    for j in range(n):
        sub = [row[:j] + row[j+1:] for row in a[1:]]
        result += (-1) ** j * a[0][j] * det(sub)
    return result


def inverse_det(a):
    n = len(a)
    d = det(a)
    if d == 0:
        return None
    if n == 1:
        return [[1 / d]]
    inv = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            sub = [row[:j] + row[j+1:] for k, row in enumerate(a) if k != i]
            inv[j][i] = (-1) ** (i + j) * det(sub) / d
    return inv


def inverse_gj(a):
    n = len(a)
    m = []
    for i in range(n):
        identity = [1.0 if i == j else 0.0 for j in range(n)]
        m.append(a[i] + identity)

    for i in range(n):
        if abs(m[i][i]) < 1e-9:
            found = False
            for k in range(i + 1, n):
                if abs(m[k][i]) > 1e-9:
                    m[i], m[k] = m[k], m[i]
                    found = True
                    break
            if not found:
                return None

        p = m[i][i]
        m[i] = [x / p for x in m[i]]

        for k in range(n):
            if k != i:
                f = m[k][i]
                m[k] = [m[k][c] - f * m[i][c] for c in range(2 * n)]

    return [row[n:] for row in m]


def print_matrix(m):
    for row in m:
        for x in row:
            print(f"{round(x, 4) + 0:10.4f}", end="")
        print()


def same(a, b):
    for i in range(len(a)):
        for j in range(len(a)):
            if abs(a[i][j] - b[i][j]) > 1e-6:
                return False
    return True


def multiply(a, b):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    return result


a = get_matrix()
inv1 = inverse_det(a)
inv2 = inverse_gj(a)

if inv1 is None or inv2 is None:
    print("\nError: determinant is 0, the inverse does not exist.")
else:
    print(f"\nDeterminant: {round(det(a), 4) + 0}")
    print("\nInverse by determinant:")
    print_matrix(inv1)
    print("\nInverse by Gauss-Jordan elimination:")
    print_matrix(inv2)
    if same(inv1, inv2):
        print("\nThe results of both methods are the same.")
    else:
        print("\nThe results of both methods are different.")
    print("\n[Extra] Check: A x inverse of A")
    print_matrix(multiply(a, inv1))
