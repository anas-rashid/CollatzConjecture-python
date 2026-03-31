import tkinter as tk
from tkinter import ttk, scrolledtext

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Catppuccin Mocha palette
BG      = "#1e1e2e"
SURFACE = "#313244"
OVERLAY = "#45475a"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"
BLUE    = "#89b4fa"
MAUVE   = "#cba6f7"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
TEAL    = "#94e2d5"


def collatz_sequence(n: int) -> list[int]:
    seq = []
    while n != 1:
        seq.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    seq.append(1)
    return seq


class ValuesDialog(tk.Toplevel):
    def __init__(self, parent, values: list[int] | None):
        super().__init__(parent)
        self.title("Collatz Sequence Values")
        self.configure(bg=BG)
        self.geometry("560x320")
        self.resizable(True, True)

        text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, bg=SURFACE, fg=TEXT,
            font=("Consolas", 11), insertbackground=TEXT,
            bd=0, padx=12, pady=10,
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if values:
            content = ", ".join(str(v) for v in values)
        else:
            content = "Give some value of 'x'"
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)
        self.focus_set()


class CollatzApp(tk.Tk):
    CHART_TYPES = ["Line", "Scatter", "Bar", "Step"]

    def __init__(self):
        super().__init__()
        self.title("Collatz Paradox")
        self.configure(bg=BG)
        self.state("zoomed")

        self.x: int = 10
        self.values: list[int] = []
        self.chart_type = tk.StringVar(value="Line")

        self._configure_ttk_style()
        self._build_ui()
        self._plot()

    # ------------------------------------------------------------------ UI --

    def _configure_ttk_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dark.TCombobox",
            fieldbackground=OVERLAY,
            background=OVERLAY,
            foreground=TEXT,
            selectbackground=MAUVE,
            selectforeground=BG,
            arrowcolor=TEXT,
            bordercolor=OVERLAY,
            lightcolor=OVERLAY,
            darkcolor=OVERLAY,
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", OVERLAY)],
            background=[("readonly", OVERLAY)],
        )

    def _build_ui(self):
        # ── top control bar ────────────────────────────────────────────────
        ctrl = tk.Frame(self, bg=SURFACE, pady=8)
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=0)

        # x = label + entry
        tk.Label(ctrl, text="x =", bg=SURFACE, fg=TEXT,
                 font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=(14, 4))

        self.entry = tk.Entry(
            ctrl, bg=OVERLAY, fg=TEXT, insertbackground=TEXT,
            font=("Segoe UI", 12), relief=tk.FLAT, width=14,
            disabledbackground=OVERLAY,
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 6), ipady=4)
        self.entry.insert(0, str(self.x))
        self.entry.bind("<Return>", lambda _e: self._plot())

        # Plot button
        tk.Button(
            ctrl, text="Plot", command=self._plot,
            bg=GREEN, fg=BG, font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT, bd=0, padx=14, pady=4, cursor="hand2",
            activebackground=TEAL, activeforeground=BG,
        ).pack(side=tk.LEFT, padx=(0, 20))

        # Graph type label + combobox
        tk.Label(ctrl, text="Graph Type:", bg=SURFACE, fg=TEXT,
                 font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=(0, 6))

        combo = ttk.Combobox(
            ctrl, textvariable=self.chart_type, values=self.CHART_TYPES,
            state="readonly", width=10, style="Dark.TCombobox",
            font=("Segoe UI", 11),
        )
        combo.pack(side=tk.LEFT, padx=(0, 20), ipady=3)
        combo.bind("<<ComboboxSelected>>", lambda _e: self._plot())

        # Right-side buttons
        for label, cmd, color in [
            ("Clean Graph", self._clean,       MAUVE),
            ("Get Values",  self._show_values, BLUE),
        ]:
            tk.Button(
                ctrl, text=label, command=cmd,
                bg=color, fg=BG, font=("Segoe UI", 11, "bold"),
                relief=tk.FLAT, bd=0, padx=14, pady=4, cursor="hand2",
                activebackground=TEXT, activeforeground=BG,
            ).pack(side=tk.RIGHT, padx=(4, 12))

        # ── matplotlib canvas ──────────────────────────────────────────────
        self.fig = Figure(facecolor=BG, tight_layout=True)
        self.ax  = self.fig.add_subplot(111)
        self._style_axes()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Navigation toolbar (zoom / pan / save)
        tb_frame = tk.Frame(self, bg=SURFACE)
        tb_frame.pack(side=tk.BOTTOM, fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, tb_frame)
        toolbar.config(bg=SURFACE)
        for child in toolbar.winfo_children():
            try:
                child.config(bg=SURFACE, fg=TEXT, activebackground=OVERLAY)
            except tk.TclError:
                pass
        toolbar.update()

    # --------------------------------------------------------------- axes --

    def _style_axes(self):
        self.ax.set_facecolor(SURFACE)
        self.ax.tick_params(colors=SUBTEXT, labelsize=10)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(OVERLAY)
        self.ax.set_xlabel("Step",  color=SUBTEXT, fontsize=11)
        self.ax.set_ylabel("Value", color=SUBTEXT, fontsize=11)
        self.ax.grid(True, color=OVERLAY, linewidth=0.6, linestyle="--")
        self.fig.patch.set_facecolor(BG)

    # -------------------------------------------------------------- logic --

    def _plot(self):
        raw = self.entry.get().strip()
        try:
            val = int(raw)
            if val < 2:
                raise ValueError
        except ValueError:
            self.entry.config(bg=RED)
            return

        self.entry.config(bg=OVERLAY)
        self.x      = val
        self.values = collatz_sequence(self.x)
        steps       = len(self.values) - 1

        self.ax.clear()
        self._style_axes()

        xs    = list(range(len(self.values)))
        ys    = self.values
        label = f"Collatz Paradox for x = {self.x}\nNo. of steps to converge at 1: {steps}"

        chart = self.chart_type.get()
        if chart == "Line":
            self.ax.plot(xs, ys, color=BLUE, linewidth=2.5,
                         marker="o", markersize=3, label=label)
        elif chart == "Scatter":
            self.ax.scatter(xs, ys, color=BLUE, s=22, label=label)
        elif chart == "Bar":
            self.ax.bar(xs, ys, color=BLUE, width=0.7, label=label)
        elif chart == "Step":
            self.ax.step(xs, ys, color=BLUE, linewidth=2.5,
                         where="mid", label=label)

        self.ax.set_title(
            f"Collatz Paradox — x = {self.x}", color=TEXT, fontsize=13, pad=10,
        )

        legend = self.ax.legend(
            facecolor=SURFACE, edgecolor=OVERLAY,
            labelcolor=TEXT, fontsize=10,
        )

        self.canvas.draw()

    def _clean(self):
        self.values = []
        self.ax.clear()
        self._style_axes()
        self.canvas.draw()

    def _show_values(self):
        ValuesDialog(self, self.values if self.values else None)


if __name__ == "__main__":
    app = CollatzApp()
    app.mainloop()
