def poly_add(A, B):
    # Add two polynomials represented as coefficient lists
    n = max(len(A), len(B))
    result = [0] * n
    for i in range(len(A)):
        result[i] += A[i]
    for i in range(len(B)):
        result[i] += B[i]
    return result

def poly_sub(A, B):
    # Subtract polynomial B from A
    n = max(len(A), len(B))
    result = [0] * n
    for i in range(len(A)):
        result[i] += A[i]
    for i in range(len(B)):
        result[i] -= B[i]
    return result

def next_power_of_two(n):
    # Find the next power of two greater than or equal to n
    m = 1
    while m < n:
        m <<= 1
    return m

def poly_mul(A, B):
    """
    Multiply two polynomials A and B using the Karatsuba algorithm.
    A and B are lists of coefficients, where the index corresponds to the power of x.
    """
    n = max(len(A), len(B))
    # Base case: when polynomials are small, use the naive multiplication
    if n <= 1:
        return [A[0] * B[0]] if A and B else []

    # Adjust the length of the polynomials to the next power of two
    m = next_power_of_two(n)
    A += [0] * (m - len(A))
    B += [0] * (m - len(B))
    n = m
    k = n // 2

    # Split the polynomials into lower and higher degree parts
    A0 = A[:k]
    A1 = A[k:]
    B0 = B[:k]
    B1 = B[k:]

    # Recursive calls
    z0 = poly_mul(A0, B0)
    z2 = poly_mul(A1, B1)
    A0A1 = poly_add(A0, A1)
    B0B1 = poly_add(B0, B1)
    z1 = poly_mul(A0A1, B0B1)
    z1 = poly_sub(poly_sub(z1, z0), z2)

    # Combine the results
    result = [0] * (2 * n - 1)
    for i in range(len(z0)):
        result[i] += z0[i]
    for i in range(len(z1)):
        result[i + k] += z1[i]
    for i in range(len(z2)):
        result[i + 2 * k] += z2[i]

    # Remove trailing zeros
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result

def poly_mul_naive(A, B):
    # Naive polynomial multiplication for verification
    n = len(A)
    m = len(B)
    result = [0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            result[i + j] += A[i] * B[j]
    return result

def poly_str(X):
    poly_string = str(X[0]) + " + "
    for i in range(1, len(X) - 1):
        poly_string += (str(X[i]) + "x^" + str(i) + " + ")
    poly_string += ( str(X[-1]) + "x^" + str(len(X) - 1) )
    return poly_string

# Example usage:
if __name__ == "__main__":
    A = [1, 2, 3]  # Represents polynomial 1 + 2x + 3x^2
    B = [4, 5, 6]  # Represents polynomial 4 + 5x + 6x^2

    result_naive = poly_mul_naive(A, B)
    result_karatsuba = poly_mul(A, B)

    print("Naive multiplication result:", result_naive)
    print("Karatsuba multiplication result:", result_karatsuba)
    assert result_naive == result_karatsuba, "The results do not match!"

    print("( " + poly_str(A) + " ) * ( " + poly_str(B) + " ) = " +\
          poly_str(result_karatsuba))

    C = [1, 2, 3, 4, 5, 6]
    D = [7, 8, 9, 10, 11, 12]
    CD = poly_mul(C, D)
    print(poly_str(CD))
