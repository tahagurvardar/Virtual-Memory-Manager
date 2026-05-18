import tkinter as tk
from tkinter import messagebox


def fifo_algorithm(pages, frame_count):
    frames = []
    queue = []
    faults = 0
    hits = 0
    steps = []

    for page in pages:
        if page in frames:
            hits += 1
            status = "Hit"
        else:
            faults += 1
            status = "Fault"

            if len(frames) < frame_count:
                frames.append(page)
                queue.append(page)
            else:
                old_page = queue.pop(0)
                index = frames.index(old_page)
                frames[index] = page
                queue.append(page)

        steps.append((page, frames.copy(), status))

    return faults, hits, steps


def lru_algorithm(pages, frame_count):
    frames = []
    recent = []
    faults = 0
    hits = 0
    steps = []

    for page in pages:
        if page in frames:
            hits += 1
            status = "Hit"
            recent.remove(page)
            recent.append(page)
        else:
            faults += 1
            status = "Fault"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                old_page = recent.pop(0)
                index = frames.index(old_page)
                frames[index] = page

            recent.append(page)

        steps.append((page, frames.copy(), status))

    return faults, hits, steps


def optimal_algorithm(pages, frame_count):
    frames = []
    faults = 0
    hits = 0
    steps = []

    for i in range(len(pages)):
        page = pages[i]

        if page in frames:
            hits += 1
            status = "Hit"
        else:
            faults += 1
            status = "Fault"

            if len(frames) < frame_count:
                frames.append(page)
            else:
                future_pages = pages[i + 1:]
                farthest_index = -1
                page_to_remove = None

                for frame_page in frames:
                    if frame_page not in future_pages:
                        page_to_remove = frame_page
                        break
                    else:
                        next_use = future_pages.index(frame_page)
                        if next_use > farthest_index:
                            farthest_index = next_use
                            page_to_remove = frame_page

                index = frames.index(page_to_remove)
                frames[index] = page

        steps.append((page, frames.copy(), status))

    return faults, hits, steps


def show_steps(name, steps):
    output.insert(tk.END, "\n" + name + "\n")
    output.insert(tk.END, "-" * 55 + "\n")

    for page, frames, status in steps:
        output.insert(
            tk.END,
            "Page " + str(page) + " -> Frames: " + str(frames) + " -> " + status + "\n"
        )


def draw_chart(fifo_faults, lru_faults, optimal_faults):
    chart.delete("all")

    values = {
        "FIFO": fifo_faults,
        "LRU": lru_faults,
        "Optimal": optimal_faults
    }

    colors = {
        "FIFO": "orange",
        "LRU": "skyblue",
        "Optimal": "lightgreen"
    }

    max_value = max(values.values())
    x = 40
    y = 20
    bar_height = 35
    gap = 25

    chart.create_text(215, 10, text="Page Fault Comparison", font=("Arial", 12, "bold"))

    for name, value in values.items():
        bar_width = int((value / max_value) * 260)

        chart.create_text(x, y + 15, text=name, anchor="w", font=("Arial", 10, "bold"))

        chart.create_rectangle(
            x + 70,
            y,
            x + 70 + bar_width,
            y + bar_height,
            fill=colors[name]
        )

        chart.create_text(x + 80 + bar_width, y + 17, text=str(value), anchor="w")

        y += bar_height + gap


def start_simulation():
    output.delete("1.0", tk.END)

    try:
        pages = [int(x) for x in page_input.get().split()]
        frame_count = int(frame_input.get())

        if frame_count <= 0:
            messagebox.showerror("Error", "Frame count must be greater than 0.")
            return

        if len(pages) == 0:
            messagebox.showerror("Error", "Page list cannot be empty.")
            return

    except:
        messagebox.showerror("Error", "Please enter valid page numbers and frame count.")
        return

    total = len(pages)

    fifo_faults, fifo_hits, fifo_steps = fifo_algorithm(pages, frame_count)
    lru_faults, lru_hits, lru_steps = lru_algorithm(pages, frame_count)
    optimal_faults, optimal_hits, optimal_steps = optimal_algorithm(pages, frame_count)

    output.insert(tk.END, "Virtual Memory Manager Simulation\n")
    output.insert(tk.END, "=" * 55 + "\n")
    output.insert(tk.END, "Pages: " + str(pages) + "\n")
    output.insert(tk.END, "Frames: " + str(frame_count) + "\n")

    show_steps("FIFO Algorithm", fifo_steps)
    output.insert(tk.END, "FIFO Faults: " + str(fifo_faults) + "\n")
    output.insert(tk.END, "FIFO Hits: " + str(fifo_hits) + "\n")
    output.insert(tk.END, "FIFO Fault Ratio: " + str(round(fifo_faults / total, 2)) + "\n")

    show_steps("LRU Algorithm", lru_steps)
    output.insert(tk.END, "LRU Faults: " + str(lru_faults) + "\n")
    output.insert(tk.END, "LRU Hits: " + str(lru_hits) + "\n")
    output.insert(tk.END, "LRU Fault Ratio: " + str(round(lru_faults / total, 2)) + "\n")

    show_steps("Optimal Algorithm", optimal_steps)
    output.insert(tk.END, "Optimal Faults: " + str(optimal_faults) + "\n")
    output.insert(tk.END, "Optimal Hits: " + str(optimal_hits) + "\n")
    output.insert(tk.END, "Optimal Fault Ratio: " + str(round(optimal_faults / total, 2)) + "\n")

    output.insert(tk.END, "\nFinal Comparison\n")
    output.insert(tk.END, "-" * 55 + "\n")
    output.insert(tk.END, "FIFO Faults: " + str(fifo_faults) + "\n")
    output.insert(tk.END, "LRU Faults: " + str(lru_faults) + "\n")
    output.insert(tk.END, "Optimal Faults: " + str(optimal_faults) + "\n")

    output.insert(
        tk.END,
        "\nOptimal algorithm usually produces the minimum number of page faults.\n"
    )

    best = min(fifo_faults, lru_faults, optimal_faults)

    if optimal_faults == best:
        output.insert(tk.END, "Best result: Optimal Algorithm\n")
    elif lru_faults == best:
        output.insert(tk.END, "Best result: LRU Algorithm\n")
    else:
        output.insert(tk.END, "Best result: FIFO Algorithm\n")

    draw_chart(fifo_faults, lru_faults, optimal_faults)


def clear_all():
    output.delete("1.0", tk.END)
    chart.delete("all")


def exit_program():
    window.destroy()


window = tk.Tk()
window.title("Virtual Memory Manager")
window.geometry("900x700")

title = tk.Label(
    window,
    text="Virtual Memory Manager",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

subtitle = tk.Label(
    window,
    text="FIFO, LRU and Optimal Page Replacement Algorithms",
    font=("Arial", 11)
)
subtitle.pack()

input_area = tk.Frame(window)
input_area.pack(pady=10)

tk.Label(input_area, text="Page Reference String:").grid(row=0, column=0, padx=5, pady=5)
page_input = tk.Entry(input_area, width=50)
page_input.grid(row=0, column=1, padx=5, pady=5)
page_input.insert(0, "1 2 3 4 1 2 5 1 2 3 4 5")

tk.Label(input_area, text="Number of Frames:").grid(row=1, column=0, padx=5, pady=5)
frame_input = tk.Entry(input_area, width=10)
frame_input.grid(row=1, column=1, sticky="w", padx=5, pady=5)
frame_input.insert(0, "3")

button_area = tk.Frame(window)
button_area.pack(pady=5)

tk.Button(button_area, text="Run Simulation", width=15, command=start_simulation).grid(row=0, column=0, padx=5)
tk.Button(button_area, text="Clear", width=15, command=clear_all).grid(row=0, column=1, padx=5)
tk.Button(button_area, text="Exit", width=15, command=exit_program).grid(row=0, column=2, padx=5)

chart = tk.Canvas(window, width=430, height=220, bg="white")
chart.pack(pady=10)

output = tk.Text(window, width=110, height=25)
output.pack(padx=10, pady=10)

window.mainloop()