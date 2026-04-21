"""
Memory Management Simulator
OS PBL Project - Phalguni, Anaya, Bhumi
Algorithms: First Fit, Best Fit, Worst Fit, Next Fit
Run: python memory_simulator.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import copy

# ─────────────────────────────────────────────
#  ALGORITHM LOGIC
# ─────────────────────────────────────────────

def first_fit(blocks, processes):
    blk = copy.deepcopy(blocks)
    allocation = [-1] * len(processes)
    for i, proc in enumerate(processes):
        for j, b in enumerate(blk):
            if b >= proc:
                allocation[i] = j
                blk[j] -= proc
                break
    return allocation, blk

def best_fit(blocks, processes):
    blk = copy.deepcopy(blocks)
    allocation = [-1] * len(processes)
    for i, proc in enumerate(processes):
        best_idx = -1
        for j, b in enumerate(blk):
            if b >= proc:
                if best_idx == -1 or blk[best_idx] > b:
                    best_idx = j
        if best_idx != -1:
            allocation[i] = best_idx
            blk[best_idx] -= proc
    return allocation, blk

def worst_fit(blocks, processes):
    blk = copy.deepcopy(blocks)
    allocation = [-1] * len(processes)
    for i, proc in enumerate(processes):
        worst_idx = -1
        for j, b in enumerate(blk):
            if b >= proc:
                if worst_idx == -1 or blk[worst_idx] < b:
                    worst_idx = j
        if worst_idx != -1:
            allocation[i] = worst_idx
            blk[worst_idx] -= proc
    return allocation, blk

def next_fit(blocks, processes):
    blk = copy.deepcopy(blocks)
    allocation = [-1] * len(processes)
    last = 0
    for i, proc in enumerate(processes):
        count = 0
        j = last
        while count < len(blk):
            if blk[j] >= proc:
                allocation[i] = j
                blk[j] -= proc
                last = j
                break
            j = (j + 1) % len(blk)
            count += 1
    return allocation, blk

ALGORITHMS = {
    "First Fit":  first_fit,
    "Best Fit":   best_fit,
    "Worst Fit":  worst_fit,
    "Next Fit":   next_fit,
}

# Color palette
COLORS = ["#4e9af1","#f97316","#22c55e","#a855f7","#ec4899",
          "#14b8a6","#f59e0b","#ef4444","#8b5cf6","#06b6d4"]
FREE_COLOR   = "#e2e8f0"
BG_COLOR     = "#0f172a"
PANEL_COLOR  = "#1e293b"
CARD_COLOR   = "#273548"
TEXT_COLOR   = "#f1f5f9"
ACCENT      = "#4e9af1"
BORDER      = "#334155"

# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────

class MemSimApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Management Simulator  •  OS PBL")
        self.geometry("1100x720")
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)
        self._build_ui()

    # ── UI LAYOUT ──────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg="#1a2744", pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⚙  Memory Management Simulator",
                 font=("Segoe UI", 18, "bold"), bg="#1a2744",
                 fg=TEXT_COLOR).pack(side="left", padx=20)
        tk.Label(hdr, text="OS PBL  •  First Fit  |  Best Fit  |  Worst Fit  |  Next Fit",
                 font=("Segoe UI", 10), bg="#1a2744", fg="#94a3b8").pack(side="right", padx=20)

        # Main split
        main = tk.Frame(self, bg=BG_COLOR)
        main.pack(fill="both", expand=True, padx=12, pady=10)

        self._build_left(main)
        self._build_right(main)

    # ── LEFT PANEL ─────────────────────────────
    def _build_left(self, parent):
        left = tk.Frame(parent, bg=PANEL_COLOR, bd=0, relief="flat", width=310)
        left.pack(side="left", fill="y", padx=(0,10))
        left.pack_propagate(False)

        def section(title):
            tk.Label(left, text=title, font=("Segoe UI", 11, "bold"),
                     bg=PANEL_COLOR, fg=ACCENT).pack(anchor="w", padx=14, pady=(14,2))
            sep = tk.Frame(left, bg=BORDER, height=1)
            sep.pack(fill="x", padx=14, pady=(0,6))

        # Memory blocks
        section("Memory Blocks (KB)")
        self.blocks_var = tk.StringVar(value="100, 500, 200, 300, 600")
        self._entry(left, self.blocks_var, "e.g. 100, 500, 200")

        section("Process Sizes (KB)")
        self.procs_var = tk.StringVar(value="212, 417, 112, 426")
        self._entry(left, self.procs_var, "e.g. 212, 417, 112")

        section("Algorithm")
        self.algo_var = tk.StringVar(value="First Fit")
        frame = tk.Frame(left, bg=PANEL_COLOR)
        frame.pack(fill="x", padx=14, pady=4)
        for algo in ALGORITHMS:
            rb = tk.Radiobutton(frame, text=algo, variable=self.algo_var,
                                value=algo, bg=PANEL_COLOR, fg=TEXT_COLOR,
                                selectcolor="#334155", activebackground=PANEL_COLOR,
                                activeforeground=TEXT_COLOR,
                                font=("Segoe UI", 10))
            rb.pack(anchor="w", pady=1)

        # Run / Compare / Reset buttons
        btn_f = tk.Frame(left, bg=PANEL_COLOR)
        btn_f.pack(fill="x", padx=14, pady=14)
        self._btn(btn_f, "▶  Run Simulation", self._run, ACCENT)
        self._btn(btn_f, "📊  Compare All",   self._compare, "#7c3aed")
        self._btn(btn_f, "↺  Reset",          self._reset,   "#475569")

        # Result table
        section("Allocation Table")
        cols = ("Process","Size","Block","Status")
        self.tree = ttk.Treeview(left, columns=cols, show="headings",
                                 height=8, style="Custom.Treeview")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=60, anchor="center")
        self.tree.pack(fill="x", padx=14, pady=4)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=CARD_COLOR, foreground=TEXT_COLOR,
                        fieldbackground=CARD_COLOR, rowheight=22,
                        font=("Segoe UI", 9))
        style.configure("Custom.Treeview.Heading",
                        background=BORDER, foreground=TEXT_COLOR,
                        font=("Segoe UI", 9, "bold"))
        style.map("Custom.Treeview", background=[("selected","#334155")])

        # Stats
        self.stats_label = tk.Label(left, text="", bg=PANEL_COLOR,
                                    fg="#94a3b8", font=("Segoe UI", 9),
                                    justify="left")
        self.stats_label.pack(anchor="w", padx=14, pady=4)

    def _entry(self, parent, var, placeholder):
        e = tk.Entry(parent, textvariable=var, bg=CARD_COLOR, fg=TEXT_COLOR,
                     insertbackground=TEXT_COLOR, font=("Segoe UI", 10),
                     relief="flat", bd=4)
        e.pack(fill="x", padx=14, pady=(0,4))

    def _btn(self, parent, text, cmd, color):
        tk.Button(parent, text=text, command=cmd,
                  bg=color, fg="white", activebackground=color,
                  font=("Segoe UI", 10, "bold"), relief="flat",
                  cursor="hand2", pady=6).pack(fill="x", pady=3)

    # ── RIGHT PANEL (Canvas) ─────────────────────
    def _build_right(self, parent):
        right = tk.Frame(parent, bg=PANEL_COLOR)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Memory Visualization",
                 font=("Segoe UI", 12, "bold"),
                 bg=PANEL_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=14, pady=(10,4))

        self.canvas = tk.Canvas(right, bg="#0d1f35", bd=0,
                                highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=14, pady=(0,14))

        # Compare frame (hidden initially)
        self.cmp_frame = tk.Frame(right, bg=PANEL_COLOR)
        self.cmp_canvas = tk.Canvas(self.cmp_frame, bg="#0d1f35",
                                    bd=0, highlightthickness=0, height=220)
        self.cmp_canvas.pack(fill="both", expand=True, padx=14, pady=(0,10))

    # ─────────────────────────────────────────────
    #  ACTIONS
    # ─────────────────────────────────────────────
    def _parse(self):
        try:
            blocks = [int(x.strip()) for x in self.blocks_var.get().split(",") if x.strip()]
            procs  = [int(x.strip()) for x in self.procs_var.get().split(",") if x.strip()]
            if not blocks or not procs:
                raise ValueError
            return blocks, procs
        except ValueError:
            messagebox.showerror("Input Error",
                "Enter comma-separated integers.\nExample: 100, 500, 200")
            return None, None

    def _run(self):
        blocks, procs = self._parse()
        if blocks is None: return
        algo = self.algo_var.get()
        alloc, remaining = ALGORITHMS[algo](blocks, procs)
        self.cmp_frame.pack_forget()
        self._draw_single(blocks, procs, alloc, remaining, algo)
        self._fill_table(blocks, procs, alloc)
        self._update_stats(blocks, procs, alloc, remaining)

    def _compare(self):
        blocks, procs = self._parse()
        if blocks is None: return
        self.cmp_frame.pack(fill="x")
        results = {}
        for name, fn in ALGORITHMS.items():
            alloc, rem = fn(blocks, procs)
            results[name] = (alloc, rem)
        self._draw_compare(blocks, procs, results)
        # Show first algo in main canvas too
        first = list(ALGORITHMS.keys())[0]
        alloc, rem = results[first]
        self._draw_single(blocks, procs, alloc, rem, first)
        self._fill_table(blocks, procs, alloc)
        self._update_stats(blocks, procs, alloc, rem)

    def _reset(self):
        self.blocks_var.set("100, 500, 200, 300, 600")
        self.procs_var.set("212, 417, 112, 426")
        self.algo_var.set("First Fit")
        self.canvas.delete("all")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.stats_label.config(text="")
        self.cmp_frame.pack_forget()

    # ─────────────────────────────────────────────
    #  DRAWING
    # ─────────────────────────────────────────────
    def _draw_single(self, blocks, procs, alloc, remaining, algo):
        c = self.canvas
        c.delete("all")
        self.update_idletasks()
        W = c.winfo_width() or 700
        H = c.winfo_height() or 420

        total = sum(blocks)
        bar_h = min(55, (H - 80) // max(len(blocks), 1))
        start_y = 50

        # Title
        c.create_text(W//2, 18, text=f"Algorithm: {algo}",
                      fill=ACCENT, font=("Segoe UI", 13, "bold"))

        for i, (orig, rem) in enumerate(zip(blocks, remaining)):
            used = orig - rem
            y = start_y + i * (bar_h + 8)

            # Label left
            c.create_text(12, y + bar_h//2,
                          text=f"B{i+1}\n{orig}KB",
                          fill=TEXT_COLOR, font=("Segoe UI", 8, "bold"),
                          anchor="w")

            x0 = 68
            avail_w = W - x0 - 14

            # Used portion
            used_w = int(avail_w * used / orig) if orig > 0 else 0

            # Find which process owns this block
            owner = -1
            for pi, a in enumerate(alloc):
                if a == i:
                    owner = pi
                    break

            col = COLORS[owner % len(COLORS)] if owner != -1 else FREE_COLOR

            # Draw used bar
            if used_w > 0:
                c.create_rectangle(x0, y, x0+used_w, y+bar_h,
                                   fill=col, outline="", width=0)
                if used_w > 40:
                    c.create_text(x0 + used_w//2, y + bar_h//2,
                                  text=f"P{owner+1} ({used}KB)" if owner!=-1 else "",
                                  fill="white", font=("Segoe UI", 8, "bold"))

            # Draw free bar
            if avail_w - used_w > 0:
                c.create_rectangle(x0+used_w, y, x0+avail_w, y+bar_h,
                                   fill=FREE_COLOR, outline="", width=0)
                if avail_w - used_w > 35:
                    c.create_text(x0+used_w + (avail_w-used_w)//2, y + bar_h//2,
                                  text=f"Free {rem}KB",
                                  fill="#64748b", font=("Segoe UI", 8))

            # Border
            c.create_rectangle(x0, y, x0+avail_w, y+bar_h,
                                outline=BORDER, width=1)

        # Legend
        lx = 14
        for pi, proc in enumerate(procs):
            col = COLORS[pi % len(COLORS)]
            lx_end = lx + 10
            ly = H - 28
            c.create_rectangle(lx, ly, lx+12, ly+12, fill=col, outline="")
            c.create_text(lx+15, ly+6,
                          text=f"P{pi+1}={proc}KB",
                          fill=TEXT_COLOR, font=("Segoe UI", 8), anchor="w")
            lx += 80
        c.create_rectangle(lx, H-28, lx+12, H-16, fill=FREE_COLOR, outline="")
        c.create_text(lx+15, H-22, text="Free", fill=TEXT_COLOR,
                      font=("Segoe UI", 8), anchor="w")

    def _draw_compare(self, blocks, procs, results):
        c = self.cmp_canvas
        c.delete("all")
        self.update_idletasks()
        W = c.winfo_width() or 700
        H = c.winfo_height() or 220
        algos = list(results.keys())
        n = len(algos)
        col_w = W // n
        total = sum(blocks)

        for ai, algo in enumerate(algos):
            alloc, remaining = results[algo]
            x_start = ai * col_w + 4
            col_title_y = 14

            # Column title
            c.create_text(x_start + col_w//2, col_title_y,
                          text=algo, fill=ACCENT,
                          font=("Segoe UI", 9, "bold"))

            bar_h = min(28, (H - 50) // max(len(blocks), 1))
            for i, (orig, rem) in enumerate(zip(blocks, remaining)):
                used = orig - rem
                y = 30 + i * (bar_h + 4)
                bw = col_w - 16
                used_w = int(bw * used / orig) if orig > 0 else 0

                owner = next((pi for pi, a in enumerate(alloc) if a == i), -1)
                col = COLORS[owner % len(COLORS)] if owner != -1 else FREE_COLOR

                if used_w > 0:
                    c.create_rectangle(x_start+8, y,
                                       x_start+8+used_w, y+bar_h,
                                       fill=col, outline="")
                if bw - used_w > 0:
                    c.create_rectangle(x_start+8+used_w, y,
                                       x_start+8+bw, y+bar_h,
                                       fill=FREE_COLOR, outline="")
                c.create_rectangle(x_start+8, y, x_start+8+bw, y+bar_h,
                                   outline=BORDER)

                # % used label
                pct = int(used*100/orig) if orig else 0
                c.create_text(x_start+8+bw+2, y+bar_h//2,
                               text=f"{pct}%", fill="#94a3b8",
                               font=("Segoe UI", 7), anchor="w")

            # Allocated count
            allocated = sum(1 for a in alloc if a != -1)
            c.create_text(x_start + col_w//2, H-12,
                          text=f"{allocated}/{len(procs)} allocated",
                          fill="#22c55e" if allocated==len(procs) else "#f97316",
                          font=("Segoe UI", 8, "bold"))

        # Vertical dividers
        for ai in range(1, n):
            x = ai * col_w
            c.create_line(x, 0, x, H, fill=BORDER, width=1)

    # ─────────────────────────────────────────────
    #  TABLE & STATS
    # ─────────────────────────────────────────────
    def _fill_table(self, blocks, procs, alloc):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, (proc, a) in enumerate(zip(procs, alloc)):
            status = "✓ Allocated" if a != -1 else "✗ Failed"
            block  = f"B{a+1} ({blocks[a]}KB)" if a != -1 else "—"
            tag = "ok" if a != -1 else "fail"
            self.tree.insert("", "end",
                             values=(f"P{i+1}", f"{proc}KB", block, status),
                             tags=(tag,))
        self.tree.tag_configure("ok",   foreground="#22c55e")
        self.tree.tag_configure("fail", foreground="#ef4444")

    def _update_stats(self, blocks, procs, alloc, remaining):
        total_mem  = sum(blocks)
        used_mem   = sum(b-r for b,r in zip(blocks,remaining))
        frag_mem   = total_mem - used_mem
        allocated  = sum(1 for a in alloc if a != -1)
        util_pct   = round(used_mem*100/total_mem, 1) if total_mem else 0
        self.stats_label.config(
            text=(f"Total Memory : {total_mem} KB\n"
                  f"Used         : {used_mem} KB  ({util_pct}%)\n"
                  f"Free/Frag    : {frag_mem} KB\n"
                  f"Allocated    : {allocated}/{len(procs)} processes")
        )


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = MemSimApp()
    app.mainloop()
