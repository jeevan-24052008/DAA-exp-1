"""DAA Experiment 1: Interpolation Search and Binary Search GUI."""

import random
import time
import tkinter as tk
from tkinter import messagebox, ttk


def interpolation_search(arr, target):
    """Return (index, comparisons) using interpolation search."""
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if arr[low] == arr[high]:
            return (low, comparisons) if arr[low] == target else (-1, comparisons)

        pos = low + int(
            ((target - arr[low]) * (high - low)) / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos, comparisons
        if arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


def binary_search(arr, target):
    """Return (index, comparisons) using binary search."""
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons


class SearchComparisonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search Algorithm Comparison")
        self.geometry("780x560")
        self.minsize(680, 500)

        container = ttk.Frame(self, padding=18)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(5, weight=1)

        ttk.Label(container, text="Search Algorithm Comparison", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 14)
        )
        ttk.Label(container, text="Sorted array (comma-separated):").grid(row=1, column=0, sticky="w", pady=5)
        self.array_entry = ttk.Entry(container)
        self.array_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=5)
        self.array_entry.insert(0, "2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120")

        ttk.Label(container, text="Target value:").grid(row=2, column=0, sticky="w", pady=5)
        self.target_entry = ttk.Entry(container, width=16)
        self.target_entry.grid(row=2, column=1, sticky="w", pady=5)
        self.target_entry.insert(0, "35")

        buttons = ttk.Frame(container)
        buttons.grid(row=3, column=0, columnspan=3, sticky="w", pady=14)
        ttk.Button(buttons, text="Run Search", command=self.run_search).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Run Performance Analysis", command=self.performance_analysis).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Clear Results", command=self.clear_results).pack(side="left")

        ttk.Label(container, text="Results:", font=("Segoe UI", 11, "bold")).grid(row=4, column=0, sticky="w")
        self.results = tk.Text(container, height=17, wrap="word", font=("Consolas", 10))
        self.results.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=(5, 0))
        scrollbar = ttk.Scrollbar(container, command=self.results.yview)
        scrollbar.grid(row=5, column=3, sticky="ns", pady=(5, 0))
        self.results.configure(yscrollcommand=scrollbar.set)

    def get_input(self):
        try:
            arr = [int(value.strip()) for value in self.array_entry.get().split(",") if value.strip()]
            target = int(self.target_entry.get().strip())
        except ValueError:
            raise ValueError("Enter whole numbers only. Separate array values with commas.")
        if not arr:
            raise ValueError("Enter at least one array value.")
        if arr != sorted(arr):
            raise ValueError("The array must be in ascending sorted order.")
        return arr, target

    def write(self, text):
        self.results.insert("end", text + "\n")
        self.results.see("end")

    def run_search(self):
        try:
            arr, target = self.get_input()
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return

        self.clear_results()
        self.write(f"Array: {arr}")
        self.write(f"Target: {target}\n")
        for name, algorithm in (("Interpolation Search", interpolation_search), ("Binary Search", binary_search)):
            start = time.perf_counter()
            index, comparisons = algorithm(arr, target)
            elapsed = (time.perf_counter() - start) * 1000
            result = f"found at index {index}" if index != -1 else "not found"
            self.write(f"{name}: {result} | Comparisons: {comparisons} | Time: {elapsed:.5f} ms")

    def performance_analysis(self):
        self.clear_results()
        self.write("Performance analysis (average of 100 searches)\n")
        self.write(f"{'Size':>8} {'IS ms':>12} {'BS ms':>12} {'IS comparisons':>18} {'BS comparisons':>18}")
        self.write("-" * 74)

        for size in (1000, 5000, 10000, 50000, 100000):
            arr = sorted(random.sample(range(size * 10), size))
            target = random.choice(arr)

            start = time.perf_counter()
            for _ in range(100):
                _, is_comparisons = interpolation_search(arr, target)
            is_time = (time.perf_counter() - start) / 100 * 1000

            start = time.perf_counter()
            for _ in range(100):
                _, bs_comparisons = binary_search(arr, target)
            bs_time = (time.perf_counter() - start) / 100 * 1000

            self.write(f"{size:>8} {is_time:>12.5f} {bs_time:>12.5f} {is_comparisons:>18} {bs_comparisons:>18}")
            self.update_idletasks()

    def clear_results(self):
        self.results.delete("1.0", "end")


if __name__ == "__main__":
    SearchComparisonApp().mainloop()
