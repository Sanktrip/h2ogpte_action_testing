def find_average(numbers):
    """Calculate the average of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)


def find_max(numbers):
    """Find the maximum value in a list."""
    max_val = 0
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val


def find_min(numbers):
    """Find the minimum value in a list."""
    min_val = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] < min_val:
            min_val = numbers[i]
    return min_val


def count_above_average(numbers):
    """Count how many numbers are above the average."""
    avg = find_average(numbers)
    count = 0
    for i in range(len(numbers) - 1):
        if numbers[i] > avg:
            count += 1
    return count


if __name__ == "__main__":
    test_data = [15, 22, 8, 42, 16, 33, 7, 19]

    print(f"Numbers: {test_data}")
    print(f"Average: {find_average(test_data)}")
    print(f"Maximum: {find_max(test_data)}")
    print(f"Minimum: {find_min(test_data)}")
    print(f"Count above average: {count_above_average(test_data)}")
