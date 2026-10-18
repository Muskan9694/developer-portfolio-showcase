import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

# ==================== COLORS ====================

BG = "#F3F6FC"
NAVY = "#173B72"
BLUE = "#2563EB"
WHITE = "#FFFFFF"
TEXT = "#1E293B"
MUTED = "#64748B"
GREEN = "#10B981"
RED = "#EF4444"
PURPLE = "#8B5CF6"
ORANGE = "#F59E0B"


# ==================== DATA MANAGEMENT ====================

def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default
    return default


def save_data(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except OSError as error:
        messagebox.showerror("Save Error", str(error))


def get_stars(rating):
    try:
        rating = max(0, min(5, int(rating)))
    except (ValueError, TypeError):
        rating = 0
    return "★" * rating + "☆" * (5 - rating)


profile = load_data(
    "profile.json",
    {"name": "", "email": "", "skills": [], "about": ""}
)
projects = load_data("projects.json", [])
reviews = load_data("reviews.json", [])

# Keep older saved project data compatible.
for project in projects:
    project.setdefault("name", "Untitled")
    project.setdefault("description", "")
    project.setdefault("category", "Other")
    project.setdefault("date", str(datetime.date.today()))


# ==================== MAIN WINDOW ====================

root = tk.Tk()
root.title("Developer Portfolio & Project Showcase")
root.geometry("1150x800")
root.minsize(750, 550)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure(
    "TNotebook.Tab",
    padding=(18, 11),
    font=("Arial", 10, "bold")
)
style.configure(
    "Horizontal.TProgressbar",
    troughcolor="#E2E8F0",
    background=BLUE,
    thickness=10
)

header = tk.Frame(root, bg=NAVY, height=78)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="DEVELOPER PORTFOLIO",
    font=("Arial", 21, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(side="left", padx=25, pady=18)

tk.Label(
    header,
    text="Build  •  Learn  •  Grow",
    font=("Arial", 10),
    bg=NAVY,
    fg="#DBEAFE"
).pack(side="left", padx=12)

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=15, pady=10)

dashboard_tab = tk.Frame(tabs, bg=BG)
profile_tab = tk.Frame(tabs, bg=BG)
project_tab = tk.Frame(tabs, bg=BG)
review_tab = tk.Frame(tabs, bg=BG)
timeline_tab = tk.Frame(tabs, bg=BG)

tabs.add(dashboard_tab, text="  Dashboard  ")
tabs.add(profile_tab, text="  My Profile  ")
tabs.add(project_tab, text="  Projects  ")
tabs.add(review_tab, text="  Reviews ★  ")
tabs.add(timeline_tab, text="  Timeline  ")


# ==================== SCROLLABLE TABS ====================

def make_scrollable(parent):
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        outer, orient="vertical", command=canvas.yview
    )
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg=BG)
    window_id = canvas.create_window(
        (0, 0), window=inner, anchor="nw"
    )

    inner.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(
            window_id, width=event.width
        )
    )

    return inner, canvas


dashboard, dashboard_canvas = make_scrollable(dashboard_tab)
profile_content, profile_canvas = make_scrollable(profile_tab)
project_content, project_canvas = make_scrollable(project_tab)
review_content, review_canvas = make_scrollable(review_tab)
timeline_content, timeline_canvas = make_scrollable(timeline_tab)

scroll_canvases = {
    0: dashboard_canvas,
    1: profile_canvas,
    2: project_canvas,
    3: review_canvas,
    4: timeline_canvas
}


def make_button(parent, text, command, color=BLUE):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=13,
        pady=8,
        bd=0
    )


def make_card(parent, padding=16):
    return tk.Frame(
        parent,
        bg=WHITE,
        padx=padding,
        pady=padding,
        highlightbackground="#DCE5F2",
        highlightthickness=1
    )


# ==================== DASHBOARD UI ====================

hero = tk.Frame(dashboard, bg=NAVY, padx=24, pady=22)
hero.pack(fill="x", padx=22, pady=(20, 14))

hero_text = tk.Frame(hero, bg=NAVY)
hero_text.pack(side="left", fill="x", expand=True)

welcome_label = tk.Label(
    hero_text,
    text="Welcome back, Developer!",
    font=("Arial", 22, "bold"),
    bg=NAVY,
    fg=WHITE
)
welcome_label.pack(anchor="w")

tk.Label(
    hero_text,
    text="Your skills, projects and progress in one place.",
    font=("Arial", 10),
    bg=NAVY,
    fg="#DBEAFE"
).pack(anchor="w", pady=(7, 0))

tk.Label(
    hero,
    text="</>\nCREATE YOUR FUTURE",
    font=("Arial", 12, "bold"),
    bg="#244B82",
    fg=WHITE,
    padx=15,
    pady=12
).pack(side="right", padx=(10, 0))

tk.Label(
    dashboard,
    text="YOUR PORTFOLIO AT A GLANCE",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=MUTED
).pack(anchor="w", padx=26)

stats_frame = tk.Frame(dashboard, bg=BG)
stats_frame.pack(fill="x", padx=20, pady=10)


def create_stat_card(parent, title, emoji, color, hint):
    card = tk.Frame(
        parent,
        bg=WHITE,
        padx=15,
        pady=13,
        highlightbackground="#DCE5F2",
        highlightthickness=1
    )

    tk.Frame(card, bg=color, height=4).pack(fill="x", pady=(0, 12))

    tk.Label(
        card,
        text=f"{emoji}  {title}",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")

    value_label = tk.Label(
        card,
        text="0",
        font=("Arial", 27, "bold"),
        bg=WHITE,
        fg=color
    )
    value_label.pack(anchor="w", pady=4)

    tk.Label(
        card,
        text=hint,
        font=("Arial", 8),
        bg=WHITE,
        fg=MUTED
    ).pack(anchor="w")

    return card, value_label


card1, project_count_label = create_stat_card(
    stats_frame, "Projects", "📁", BLUE, "Projects saved"
)
card1.pack(side="left", fill="both", expand=True, padx=5)

card2, review_count_label = create_stat_card(
    stats_frame, "Reviews", "⭐", GREEN, "Feedback received"
)
card2.pack(side="left", fill="both", expand=True, padx=5)

card3, skills_count_label = create_stat_card(
    stats_frame, "Skills", "💡", PURPLE, "Profile skills"
)
card3.pack(side="left", fill="both", expand=True, padx=5)

overview_card = make_card(dashboard)
overview_card.pack(fill="x", padx=26, pady=(0, 10))

tk.Label(
    overview_card,
    text="📌 Portfolio Overview",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

latest_project_label = tk.Label(
    overview_card,
    text="Latest project: No projects yet",
    font=("Arial", 10),
    bg=WHITE,
    fg=TEXT,
    wraplength=850,
    justify="left"
)
latest_project_label.pack(anchor="w", pady=(8, 0))

recent_card = make_card(dashboard)
recent_card.pack(fill="x", padx=26, pady=(0, 10))

tk.Label(
    recent_card,
    text="🧩 Recent Projects",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

recent_projects_frame = tk.Frame(recent_card, bg=WHITE)
recent_projects_frame.pack(fill="x", pady=(8, 0))

graph_card = make_card(dashboard)
graph_card.pack(fill="x", padx=26, pady=(0, 10))

tk.Label(
    graph_card,
    text="📊 Project Category Analytics",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    graph_card,
    text="See how your projects are distributed by category.",
    font=("Arial", 9),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(3, 0))

graph_canvas = tk.Canvas(
    graph_card, height=245, bg=WHITE, highlightthickness=0
)
graph_canvas.pack(fill="x", pady=(8, 0))

breakdown_card = make_card(dashboard)
breakdown_card.pack(fill="x", padx=26, pady=(0, 20))

tk.Label(
    breakdown_card,
    text="📈 Category Breakdown",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

progress_frame = tk.Frame(breakdown_card, bg=WHITE)
progress_frame.pack(fill="x", pady=(8, 0))


def draw_graph(categories):
    graph_canvas.delete("all")
    width = max(graph_canvas.winfo_width(), 650)

    if not categories:
        graph_canvas.create_text(
            width // 2, 100,
            text="Add projects to see your analytics.",
            fill=MUTED,
            font=("Arial", 11)
        )
        return

    colors = [BLUE, GREEN, PURPLE, ORANGE, RED, "#0891B2"]
    maximum = max(categories.values())
    items = list(categories.items())

    graph_canvas.create_line(
        30, 195, width - 25, 195, fill="#CBD5E1"
    )

    available_width = width - 80
    gap = 22
    bar_width = min(
        75,
        max(30, (available_width - gap * len(items)) // len(items))
    )
    total_width = len(items) * (bar_width + gap) - gap
    x = max(40, (width - total_width) // 2)

    for i, (category, count) in enumerate(items):
        bar_height = int((count / maximum) * 135)
        y = 195 - bar_height
        color = colors[i % len(colors)]

        graph_canvas.create_rectangle(
            x, y, x + bar_width, 195,
            fill=color, outline=""
        )
        graph_canvas.create_text(
            x + bar_width // 2, y - 12,
            text=str(count),
            fill=TEXT,
            font=("Arial", 10, "bold")
        )
        graph_canvas.create_text(
            x + bar_width // 2, 218,
            text=category,
            fill=TEXT,
            font=("Arial", 9, "bold"),
            width=bar_width + 25
        )
        x += bar_width + gap


# ==================== PROFILE TAB ====================

profile_left = tk.Frame(
    profile_content,
    bg=NAVY,
    padx=22,
    pady=24
)
profile_left.pack(side="left", fill="y", padx=15, pady=15)

tk.Label(
    profile_left,
    text="👩‍💻",
    font=("Arial", 48),
    bg=NAVY,
    fg=WHITE
).pack(pady=(0, 8))

profile_name_label = tk.Label(
    profile_left,
    text=profile.get("name", "").title() or "Your Name",
    font=("Arial", 15, "bold"),
    bg=NAVY,
    fg=WHITE,
    wraplength=190
)
profile_name_label.pack(pady=5)

profile_email_label = tk.Label(
    profile_left,
    text=profile.get("email", "") or "Your email",
    font=("Arial", 9),
    bg=NAVY,
    fg="#DBEAFE",
    wraplength=190
)
profile_email_label.pack(pady=(0, 15))

tk.Label(
    profile_left,
    text="MY SKILLS",
    font=("Arial", 10, "bold"),
    bg=NAVY,
    fg="#BFDBFE"
).pack(anchor="w", pady=(5, 8))

skills_box = tk.Frame(profile_left, bg=NAVY)
skills_box.pack(fill="x")

profile_right = tk.Frame(
    profile_content,
    bg=WHITE,
    padx=22,
    pady=20,
    highlightbackground="#DCE5F2",
    highlightthickness=1
)
profile_right.pack(
    side="left", fill="both", expand=True,
    padx=(0, 15), pady=15
)

tk.Label(
    profile_right,
    text="My Developer Profile",
    font=("Arial", 19, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    profile_right,
    text="Keep your professional information up to date.",
    font=("Arial", 10),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(3, 16))


def profile_field(label_text, value=""):
    tk.Label(
        profile_right,
        text=label_text,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(anchor="w", pady=(8, 4))

    entry = tk.Entry(
        profile_right,
        font=("Arial", 11),
        relief="solid",
        bd=1,
        bg="#F8FAFC",
        fg=TEXT
    )
    entry.pack(fill="x", ipady=7)
    entry.insert(0, value)
    return entry


name_entry = profile_field("Full Name", profile.get("name", ""))
email_entry = profile_field("Email Address", profile.get("email", ""))
skills_entry = profile_field(
    "Skills (separate with commas)",
    ", ".join(profile.get("skills", []))
)

tk.Label(
    profile_right,
    text="About Me",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).pack(anchor="w", pady=(12, 4))

about_entry = tk.Text(
    profile_right,
    height=5,
    font=("Arial", 10),
    relief="solid",
    bd=1,
    bg="#F8FAFC",
    fg=TEXT,
    wrap="word"
)
about_entry.pack(fill="x")
about_entry.insert("1.0", profile.get("about", ""))


def refresh_profile_card():
    profile_name_label.config(
        text=profile.get("name", "").title() or "Your Name"
    )
    profile_email_label.config(
        text=profile.get("email", "") or "Your email"
    )

    for widget in skills_box.winfo_children():
        widget.destroy()

    skills = profile.get("skills", [])

    if not skills:
        tk.Label(
            skills_box,
            text="Add your skills in the form.",
            bg=NAVY,
            fg="#DBEAFE",
            font=("Arial", 9),
            wraplength=190
        ).pack(anchor="w")

    for skill in skills:
        tk.Label(
            skills_box,
            text=f"  {skill}  ",
            bg="#E0E7FF",
            fg="#1D4ED8",
            font=("Arial", 9, "bold"),
            padx=5,
            pady=4
        ).pack(anchor="w", pady=3)


def save_profile():
    global profile

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    skills_text = skills_entry.get().strip()
    about = about_entry.get("1.0", "end-1c").strip()

    if not name:
        messagebox.showwarning(
            "Missing Information", "Please enter your name."
        )
        return

    profile = {
        "name": name,
        "email": email,
        "skills": [
            skill.strip()
            for skill in skills_text.split(",")
            if skill.strip()
        ],
        "about": about
    }

    save_data("profile.json", profile)
    refresh_profile_card()
    update_dashboard()

    messagebox.showinfo("Saved", "Profile saved successfully!")


make_button(
    profile_right, "💾  Save Profile", save_profile
).pack(anchor="w", pady=16)


# ==================== PROJECTS TAB ====================

project_header = make_card(project_content, 20)
project_header.pack(fill="x", padx=15, pady=(15, 10))

tk.Label(
    project_header,
    text="🚀 Project Showcase",
    font=("Arial", 19, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    project_header,
    text="Add, search, organize and manage your development projects.",
    font=("Arial", 10),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(4, 0))

form = make_card(project_content, 18)
form.pack(fill="x", padx=15, pady=5)

tk.Label(
    form,
    text="Project Information",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))


def project_field(parent, label_text, row, column, width=25):
    tk.Label(
        parent,
        text=label_text,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT
    ).grid(row=row, column=column, sticky="w", padx=5, pady=4)

    entry = tk.Entry(
        parent,
        width=width,
        font=("Arial", 10),
        bg="#F8FAFC",
        fg=TEXT,
        relief="solid",
        bd=1
    )
    entry.grid(
        row=row + 1,
        column=column,
        padx=5,
        pady=(0, 8),
        ipady=6,
        sticky="ew"
    )
    return entry


project_name_entry = project_field(
    form, "Project Name", 1, 0, 25
)
project_desc_entry = project_field(
    form, "Project Description", 1, 1, 32
)

tk.Label(
    form,
    text="Category",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
).grid(row=1, column=2, sticky="w", padx=5, pady=4)

category_combo = ttk.Combobox(
    form,
    values=[
        "Python", "Web Development", "C++",
        "Java", "Database", "Other"
    ],
    state="readonly",
    width=17
)
category_combo.grid(
    row=2, column=2, padx=5, pady=(0, 8), sticky="ew"
)
category_combo.set("Python")

for column in range(3):
    form.grid_columnconfigure(column, weight=1)

search_frame = tk.Frame(
    project_content, bg=WHITE, padx=15, pady=12
)
search_frame.pack(fill="x", padx=15, pady=(8, 5))

tk.Label(
    search_frame,
    text="🔍 Search",
    bg=WHITE,
    fg=NAVY,
    font=("Arial", 10, "bold")
).pack(side="left")

search_entry = tk.Entry(
    search_frame,
    width=25,
    font=("Arial", 10),
    relief="solid",
    bd=1,
    bg="#F8FAFC"
)
search_entry.pack(side="left", padx=(8, 15), ipady=5)

tk.Label(
    search_frame,
    text="Category",
    bg=WHITE,
    fg=NAVY,
    font=("Arial", 10, "bold")
).pack(side="left", padx=(0, 8))

filter_combo = ttk.Combobox(
    search_frame,
    values=[
        "All", "Python", "Web Development",
        "C++", "Java", "Database", "Other"
    ],
    state="readonly",
    width=18
)
filter_combo.pack(side="left")
filter_combo.set("All")

list_frame = make_card(project_content, 12)
list_frame.pack(fill="both", expand=True, padx=15, pady=5)

tk.Label(
    list_frame,
    text="📂 Your Projects",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", pady=(0, 8))

project_list = tk.Listbox(
    list_frame,
    font=("Arial", 10),
    bg="#F8FAFC",
    fg=TEXT,
    selectbackground="#DBEAFE",
    selectforeground="#1D4ED8",
    relief="flat",
    bd=0,
    height=12,
    activestyle="none",
    selectmode="browse"
)
project_list.pack(side="left", fill="both", expand=True)

project_scrollbar = ttk.Scrollbar(
    list_frame,
    orient="vertical",
    command=project_list.yview
)
project_scrollbar.pack(side="right", fill="y")
project_list.config(yscrollcommand=project_scrollbar.set)

visible_projects = []
editing_index = None


def refresh_projects():
    global visible_projects

    project_list.delete(0, tk.END)
    visible_projects = []

    query = search_entry.get().strip().lower()
    category = filter_combo.get()

    for index, project in enumerate(projects):
        if category != "All" and project.get("category") != category:
            continue

        searchable = (
            project.get("name", "") + " " +
            project.get("description", "") + " " +
            project.get("category", "")
        ).lower()

        if query and query not in searchable:
            continue

        visible_projects.append(index)
        project_list.insert(
            tk.END,
            f"  {project.get('name', 'Untitled')}   |   "
            f"{project.get('category', 'Other')}   |   "
            f"{project.get('description', '')}"
        )


def clear_project_form():
    global editing_index

    editing_index = None
    project_name_entry.delete(0, tk.END)
    project_desc_entry.delete(0, tk.END)
    category_combo.set("Python")
    add_project_button.config(text="➕ Add Project")


def add_or_update_project():
    global editing_index

    name = project_name_entry.get().strip()
    description = project_desc_entry.get().strip()
    category = category_combo.get().strip() or "Other"

    if not name or not description:
        messagebox.showwarning(
            "Missing Information",
            "Please enter both project name and description."
        )
        return

    data = {
        "name": name,
        "description": description,
        "category": category,
        "date": str(datetime.date.today())
    }

    if editing_index is None:
        projects.append(data)
    else:
        projects[editing_index].update(data)

    save_data("projects.json", projects)
    clear_project_form()
    refresh_projects()
    refresh_review_projects()
    update_dashboard()
    refresh_timeline()


def get_selected_project_index():
    selection = project_list.curselection()

    if not selection:
        messagebox.showwarning(
            "Select Project", "Please select a project first."
        )
        return None

    return visible_projects[selection[0]]


def edit_project():
    global editing_index

    index = get_selected_project_index()
    if index is None:
        return

    project = projects[index]
    editing_index = index

    project_name_entry.delete(0, tk.END)
    project_name_entry.insert(0, project.get("name", ""))

    project_desc_entry.delete(0, tk.END)
    project_desc_entry.insert(0, project.get("description", ""))

    category_combo.set(project.get("category", "Other"))
    add_project_button.config(text="💾 Save Changes")


def delete_project():
    index = get_selected_project_index()
    if index is None:
        return

    name = projects[index].get("name", "this project")

    if not messagebox.askyesno(
        "Confirm Delete", f"Delete '{name}'?"
    ):
        return

    del projects[index]
    save_data("projects.json", projects)
    clear_project_form()
    refresh_projects()
    refresh_review_projects()
    update_dashboard()
    refresh_timeline()


def show_project_details(event=None):
    index = get_selected_project_index()
    if index is None:
        return

    project = projects[index]

    window = tk.Toplevel(root)
    window.title(project.get("name", "Project Details"))
    window.geometry("460x330")
    window.configure(bg=WHITE)

    tk.Label(
        window,
        text=project.get("name", ""),
        font=("Arial", 17, "bold"),
        bg=WHITE,
        fg=NAVY,
        wraplength=400
    ).pack(pady=(18, 8))

    tk.Label(
        window,
        text=f"Category: {project.get('category', 'Other')}\n"
             f"Created: {project.get('date', '')}",
        bg=WHITE,
        fg=MUTED,
        font=("Arial", 10)
    ).pack()

    tk.Label(
        window,
        text=project.get("description", ""),
        bg=WHITE,
        fg=TEXT,
        font=("Arial", 11),
        wraplength=400,
        justify="left"
    ).pack(padx=20, pady=18, anchor="w")

    make_button(
        window, "Close", window.destroy, MUTED
    ).pack(pady=8)


buttons_frame = tk.Frame(project_content, bg=BG)
buttons_frame.pack(fill="x", padx=15, pady=10)

add_project_button = make_button(
    buttons_frame,
    "➕ Add Project",
    add_or_update_project,
    BLUE
)
add_project_button.pack(side="left", padx=3)

make_button(
    buttons_frame, "✏️ Edit", edit_project, PURPLE
).pack(side="left", padx=3)

make_button(
    buttons_frame, "🗑️ Delete", delete_project, RED
).pack(side="left", padx=3)

make_button(
    buttons_frame, "Clear", clear_project_form, MUTED
).pack(side="left", padx=3)

search_entry.bind("<KeyRelease>", lambda event: refresh_projects())
filter_combo.bind(
    "<<ComboboxSelected>>", lambda event: refresh_projects()
)
project_list.bind("<Double-Button-1>", show_project_details)


# ==================== REVIEWS TAB ====================

review_header = make_card(review_content, 18)
review_header.pack(fill="x", padx=15, pady=(15, 8))

tk.Label(
    review_header,
    text="⭐ Project Reviews",
    font=("Arial", 18, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    review_header,
    text="Collect and manage feedback about your projects.",
    font=("Arial", 10),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(4, 0))

review_form = make_card(review_content, 15)
review_form.pack(fill="x", padx=15, pady=5)

tk.Label(
    review_form,
    text="Project",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10, "bold")
).grid(row=0, column=0, sticky="w", padx=5)

review_project_combo = ttk.Combobox(
    review_form, state="readonly", width=25
)
review_project_combo.grid(row=1, column=0, padx=5, pady=5)

tk.Label(
    review_form,
    text="Reviewer Name",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10, "bold")
).grid(row=0, column=1, sticky="w", padx=5)

reviewer_entry = tk.Entry(
    review_form, width=25, font=("Arial", 10)
)
reviewer_entry.grid(row=1, column=1, padx=5, pady=5, ipady=5)

tk.Label(
    review_form,
    text="Rating (1 to 5)",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10, "bold")
).grid(row=0, column=2, sticky="w", padx=5)

rating_combo = ttk.Combobox(
    review_form,
    values=["1", "2", "3", "4", "5"],
    state="readonly",
    width=8
)
rating_combo.grid(row=1, column=2, padx=5, pady=5)
rating_combo.set("5")

tk.Label(
    review_form,
    text="Comment",
    bg=WHITE,
    fg=TEXT,
    font=("Arial", 10, "bold")
).grid(row=2, column=0, sticky="w", padx=5, pady=(8, 0))

comment_entry = tk.Entry(
    review_form, width=55, font=("Arial", 10)
)
comment_entry.grid(
    row=3, column=0, columnspan=3,
    padx=5, pady=5, sticky="ew", ipady=5
)

review_form.grid_columnconfigure(0, weight=1)
review_form.grid_columnconfigure(1, weight=1)


review_list_card = make_card(review_content, 12)
review_list_card.pack(fill="both", expand=True, padx=15, pady=8)

tk.Label(
    review_list_card,
    text="📝 Saved Reviews",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w", pady=(0, 8))

review_list_frame = tk.Frame(review_list_card, bg=WHITE)
review_list_frame.pack(fill="both", expand=True)

review_list = tk.Listbox(
    review_list_frame,
    font=("Arial", 10),
    bg="#FFFBEB",
    fg=TEXT,
    relief="flat",
    bd=0,
    height=10,
    selectbackground="#FEF3C7",
    selectforeground="#92400E"
)
review_list.pack(side="left", fill="both", expand=True)

review_scrollbar = ttk.Scrollbar(
    review_list_frame,
    orient="vertical",
    command=review_list.yview
)
review_scrollbar.pack(side="right", fill="y")
review_list.config(yscrollcommand=review_scrollbar.set)


def refresh_review_projects():
    names = [p.get("name", "") for p in projects]
    review_project_combo["values"] = names

    if names:
        current = review_project_combo.get()
        if current in names:
            review_project_combo.set(current)
        else:
            review_project_combo.current(0)
    else:
        review_project_combo.set("")


def refresh_reviews():
    review_list.delete(0, tk.END)

    for index, review in enumerate(reviews):
        review_list.insert(
            tk.END,
            f"{index + 1}. {review.get('project_name', '')}  |  "
            f"{get_stars(review.get('rating', 0))}  |  "
            f"{review.get('reviewer', '')}: "
            f"{review.get('comment', '')}"
        )


def add_review():
    project_name = review_project_combo.get().strip()
    reviewer = reviewer_entry.get().strip()
    comment = comment_entry.get().strip()

    if not project_name:
        messagebox.showwarning(
            "No Project", "Please add a project first."
        )
        return

    if not reviewer or not comment:
        messagebox.showwarning(
            "Missing Information",
            "Please enter reviewer name and comment."
        )
        return

    reviews.append({
        "project_name": project_name,
        "reviewer": reviewer,
        "comment": comment,
        "rating": int(rating_combo.get()),
        "date": str(datetime.date.today())
    })

    save_data("reviews.json", reviews)
    refresh_reviews()
    update_dashboard()

    reviewer_entry.delete(0, tk.END)
    comment_entry.delete(0, tk.END)
    rating_combo.set("5")

    messagebox.showinfo("Success", "Review added successfully!")


def delete_review():
    selection = review_list.curselection()

    if not selection:
        messagebox.showwarning(
            "Select Review", "Please select a review first."
        )
        return

    if not messagebox.askyesno(
        "Confirm Delete", "Delete selected review?"
    ):
        return

    del reviews[selection[0]]
    save_data("reviews.json", reviews)
    refresh_reviews()
    update_dashboard()


review_buttons = tk.Frame(review_content, bg=BG)
review_buttons.pack(fill="x", padx=15, pady=8)

make_button(
    review_buttons, "⭐ Add Review", add_review, GREEN
).pack(side="left", padx=3)

make_button(
    review_buttons, "🗑️ Delete Review", delete_review, RED
).pack(side="left", padx=3)


# ==================== TIMELINE TAB ====================

timeline_header = make_card(timeline_content, 18)
timeline_header.pack(fill="x", padx=15, pady=(15, 8))

tk.Label(
    timeline_header,
    text="🚀 Project Journey",
    font=("Arial", 18, "bold"),
    bg=WHITE,
    fg=NAVY
).pack(anchor="w")

tk.Label(
    timeline_header,
    text="View your saved projects in date order.",
    font=("Arial", 10),
    bg=WHITE,
    fg=MUTED
).pack(anchor="w", pady=(4, 0))

timeline_items = tk.Frame(timeline_content, bg=BG)
timeline_items.pack(fill="both", expand=True, padx=15, pady=5)


def refresh_timeline():
    for widget in timeline_items.winfo_children():
        widget.destroy()

    if not projects:
        empty = make_card(timeline_items)
        empty.pack(fill="x", pady=8)

        tk.Label(
            empty,
            text="No projects yet. Add your first project!",
            bg=WHITE,
            fg=MUTED,
            font=("Arial", 11)
        ).pack(anchor="w")
        return

    sorted_projects = sorted(
        projects,
        key=lambda p: p.get("date", ""),
        reverse=True
    )
    colors = [BLUE, GREEN, PURPLE, ORANGE, RED]

    for index, project in enumerate(sorted_projects):
        row = tk.Frame(timeline_items, bg=BG)
        row.pack(fill="x", pady=5)

        tk.Label(
            row,
            text="●",
            bg=BG,
            fg=colors[index % len(colors)],
            font=("Arial", 23, "bold")
        ).pack(side="left", padx=(5, 10))

        card = make_card(row, 12)
        card.pack(side="left", fill="x", expand=True)

        tk.Label(
            card,
            text=f"{project.get('date', '')}  •  "
                 f"{project.get('category', 'Other')}",
            bg=WHITE,
            fg=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text=project.get("name", ""),
            bg=WHITE,
            fg=NAVY,
            font=("Arial", 12, "bold"),
            wraplength=800
        ).pack(anchor="w", pady=3)

        tk.Label(
            card,
            text=project.get("description", ""),
            bg=WHITE,
            fg=TEXT,
            font=("Arial", 10),
            wraplength=800,
            justify="left"
        ).pack(anchor="w")


# ==================== DASHBOARD UPDATE ====================

def update_dashboard():
    project_count_label.config(text=str(len(projects)))
    review_count_label.config(text=str(len(reviews)))
    skills_count_label.config(
        text=str(len(profile.get("skills", [])))
    )

    name = profile.get("name", "").strip() or "Developer"
    welcome_label.config(text=f"Welcome back, {name}!")

    if projects:
        latest = projects[-1]
        latest_project_label.config(
            text=f"Latest project: {latest.get('name', 'Untitled')}"
        )
    else:
        latest_project_label.config(
            text="No projects yet — add your first project!"
        )

    for widget in recent_projects_frame.winfo_children():
        widget.destroy()

    if not projects:
        tk.Label(
            recent_projects_frame,
            text="Your recent projects will appear here.",
            bg=WHITE,
            fg=MUTED,
            font=("Arial", 10)
        ).pack(anchor="w", pady=8)
    else:
        for project in reversed(projects[-3:]):
            item = tk.Frame(
                recent_projects_frame,
                bg="#F8FAFF",
                padx=12,
                pady=9,
                highlightbackground="#E2E8F0",
                highlightthickness=1
            )
            item.pack(fill="x", pady=4)

            left = tk.Frame(item, bg="#F8FAFF")
            left.pack(side="left", fill="x", expand=True)

            tk.Label(
                left,
                text=project.get("name", "Untitled"),
                bg="#F8FAFF",
                fg=NAVY,
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

            description = project.get("description", "")
            if len(description) > 100:
                description = description[:97] + "..."

            tk.Label(
                left,
                text=description,
                bg="#F8FAFF",
                fg=MUTED,
                font=("Arial", 9),
                wraplength=700,
                justify="left"
            ).pack(anchor="w", pady=(3, 0))

            tk.Label(
                item,
                text=project.get("category", "Other"),
                bg="#EDE9FE",
                fg="#6D28D9",
                font=("Arial", 9, "bold"),
                padx=8,
                pady=4
            ).pack(side="right", padx=(8, 0))

    categories = {}
    for project in projects:
        category = project.get("category", "Other")
        categories[category] = categories.get(category, 0) + 1

    for widget in progress_frame.winfo_children():
        widget.destroy()

    if not categories:
        tk.Label(
            progress_frame,
            text="Add projects to see category breakdown.",
            bg=WHITE,
            fg=MUTED,
            font=("Arial", 10)
        ).pack(anchor="w")
    else:
        total = len(projects)
        colors = [BLUE, GREEN, PURPLE, ORANGE, RED]

        for index, (category, count) in enumerate(categories.items()):
            row = tk.Frame(progress_frame, bg=WHITE)
            row.pack(fill="x", pady=5)

            percentage = int(count / total * 100)

            tk.Label(
                row,
                text=category,
                width=18,
                anchor="w",
                bg=WHITE,
                fg=colors[index % len(colors)],
                font=("Arial", 10, "bold")
            ).pack(side="left")

            ttk.Progressbar(
                row,
                maximum=100,
                value=percentage,
                length=240
            ).pack(side="left", padx=8)

            tk.Label(
                row,
                text=f"{count} project(s) • {percentage}%",
                bg=WHITE,
                fg=MUTED,
                font=("Arial", 9)
            ).pack(side="left")

    draw_graph(categories)
    root.after_idle(lambda: draw_graph(categories))


# ==================== MOUSE WHEEL SCROLLING ====================

def scroll_active_tab(event):
    try:
        selected = tabs.index(tabs.select())
        canvas = scroll_canvases.get(selected)

        if canvas is None:
            return "break"

        if event.delta:
            canvas.yview_scroll(
                -3 if event.delta > 0 else 3,
                "units"
            )
    except (tk.TclError, ValueError):
        pass

    return "break"


def scroll_linux_up(event):
    canvas = scroll_canvases.get(tabs.index(tabs.select()))
    if canvas:
        canvas.yview_scroll(-3, "units")
    return "break"


def scroll_linux_down(event):
    canvas = scroll_canvases.get(tabs.index(tabs.select()))
    if canvas:
        canvas.yview_scroll(3, "units")
    return "break"


root.bind_all("<MouseWheel>", scroll_active_tab)
root.bind_all("<Button-4>", scroll_linux_up)
root.bind_all("<Button-5>", scroll_linux_down)


# ==================== START APPLICATION ====================

refresh_profile_card()
refresh_projects()
refresh_review_projects()
refresh_reviews()
refresh_timeline()
update_dashboard()

root.mainloop()