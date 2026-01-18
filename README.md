<img width="1920" height="1080" alt="Screenshot 2026-01-18 065727" src="https://github.com/user-attachments/assets/241e5a75-8f93-428b-84e3-a489a5e043d7" /># BarPlanCE 🏗️

**Bar Cutting & Optimization Tool for Civil Engineers**

## Why BarPlanCE exists (and why it matters)

Reinforcement steel typically accounts for 15–25% of total RCC construction cost, which can be ₹7–12 lakh for a mid-sized building.
Industry studies and site audits consistently show that 3–7% of reinforcement steel is lost as cutting waste, translating to ₹30,000–70,000 due to poor planning, manual estimation, or ad-hoc bar cutting on site.
On a mid-sized project, that wastage alone can mean:

* several tonnes of steel lost
* cost overruns running into lakhs
* re-order delays and site inefficiencies

Most sites still rely on **Excel sheets and manual judgment** to decide how bars are cut from standard lengths. Excel is excellent for quantities, but **terrible at combinatorial optimization**.

**BarPlanCE solves exactly this gap.**


<img width="1920" height="1080" alt="Screenshot 2026-01-18 065727" src="https://github.com/user-attachments/assets/f72dccd2-3af9-40e3-aa34-ce5b731cffdc" />


It takes raw cut requirements and produces an **optimized bar cutting plan** that:

* minimizes wastage
* shows exactly how each bar is cut
* gives visual clarity suitable for site execution

This is not academic optimization.
This is **construction-grade practicality**.

---

## What BarPlanCE does

BarPlanCE is a desktop application for:

* reinforcement bar cutting optimization
* BBS-support planning
* fabrication and site execution clarity

It converts cut requirements into:

* optimized bar usage
* per-bar cut breakdown
* per-bar wasted length
* visual bar diagrams for quick understanding

---

## ✨ Key Features

* 📐 **Bar Cut Optimization**
  Uses exact combinations for small datasets and fast heuristics for large datasets.

* 📊 **Visual Bar Representation**
  Color-coded graphical bars showing individual cuts.

* 📉 **Automatic Wastage Calculation**
  Unused length per bar is calculated and displayed.

* 📂 **Flexible Input**

<img width="1875" height="115" alt="Screenshot 2026-01-18 065646" src="https://github.com/user-attachments/assets/56969781-b75a-471e-83aa-a8d25cece531" />
* Also the size of sourced BAR can be change, usually which is 6000/1200 depending on type od REBAR

  * Manual entry
    <img width="634" height="500" alt="Screenshot 2026-01-18 070845" src="https://github.com/user-attachments/assets/c8f88ee5-b130-4834-949a-5a184f0038d3" />

  * CSV import
  * Excel (.xlsx) import

* 📤 **Export Ready**

  * CSV
  * Excel (.xlsx)

* ⏳ **Progress Feedback**
  Clear progress indication during optimization.

* 🧠 **Fail-Safe Logic**
  Large inputs automatically switch to efficient heuristic mode to avoid freezes.

**Also, equipped with real-time feedback through dialog boxes, confirming successful data loads or alerting users to errors. This ensures engineers always know the status of their input, optimization, and exports.**

<img width="411" height="198" alt="Screenshot 2026-01-18 072659" src="https://github.com/user-attachments/assets/29c0a877-4849-4084-9d08-5191d50ee4d8" />
<img width="249" height="197" alt="Screenshot 2026-01-18 065914" src="https://github.com/user-attachments/assets/e6baa0c9-9c2b-4643-a62d-718399ccac3d" />
<img width="349" height="198" alt="Screenshot 2026-01-18 070408" src="https://github.com/user-attachments/assets/a7bd37a0-3407-49b6-bc4c-acc17262bccc" />
<img width="264" height="225" alt="Screenshot 2026-01-18 073245" src="https://github.com/user-attachments/assets/2d01eef8-b224-4bd2-91c3-0b31a920244e" />
<img width="322" height="196" alt="Screenshot 2026-01-18 071133" src="https://github.com/user-attachments/assets/29fddacf-7579-4aa1-a249-1aabe9946fb9" />

---

## 🧩 Typical Use Cases

* Reinforcement planning on site
* Bar Bending Schedule (BBS) preparation
* Steel wastage reduction
* Fabrication yard cutting plans
* Cross-checking contractor cutting logic

Designed specifically for **civil engineers, site engineers, and planning engineers**.

---

## 🖥️ Technology Stack

* **Python 3**
* **PySide6** – Desktop GUI
* **pandas** – Data handling
* **openpyxl** – Excel file support

All dependencies are **free and open-source**.

---

## 📥 Installation (using `uv`)

This project uses **uv**, a fast modern Python package manager.

### 1. Install uv (once)

```bash
pip install uv
```

### 2. Clone the repository

```bash
git clone https://github.com/your-username/BarPlanCE.git
cd BarPlanCE
```

### 3. Create environment & install dependencies

```bash
uv venv
uv pip install pyside6 pandas openpyxl
```

### 4. Run the application

```bash
python gui.py
```

---

## 📄 Input Format

### Manual Input

```
1200, 3
800
450, 2
```

### CSV / Excel Format

| Length | Quantity |
| ------ | -------- |
| 1200   | 3        |
| 800    | 1        |
| 450    | 2        |

Notes:

* Lengths are automatically rounded up
* Quantity defaults to 1 if omitted
---

## 📊 Output

For each standard bar:

* list of cut lengths
* graphical bar visualization
* wasted (unused) length

Exports are Excel-friendly and suitable for:

* site sharing
* contractor instructions
* records and audits

---

## 🚧 Known Constraints

* Large datasets use heuristic optimization for speed
* Cutting loss (kerf) not yet included
* Metric units assumed

---

## 🔮 Planned Enhancements

* Cutting loss allowance
* Steel weight calculations
* BBS summary tables
* PDF export
* IS / ASTM bar presets

---

## 📜 License

MIT License
Free for **personal, academic, and commercial** use.

---

## 👷 Philosophy

BarPlanCE is built on a simple belief:

> *Steel is expensive. Wastage is preventable. Planning should be visual and precise.*

If this tool saves even **1% steel on one project**, it has already paid for itself many times over.
