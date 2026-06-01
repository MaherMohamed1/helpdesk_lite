import functools
import os
import sqlite3

from flask import Flask, request, redirect, url_for, render_template, abort, session
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),
)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


@app.context_processor
def inject_user():
    return {
        "logged_in": "user" in session,
        "current_user": session.get("user"),
        "current_role": session.get("role"),
    }


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "helpdesk.db")

STATUS_FLOW = {"To Do": "In Progress", "In Progress": "In Review", "In Review": "Done", "Done": None}
CATEGORIES = ["IT", "Development", "HR", "Finance", "Other"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUS_ORDER = ["To Do", "In Progress", "In Review", "Done"]

# Semantic color mapping for statuses, priorities, and categories
STATUS_COLORS = {
    "To Do": {"bg": "#e9f0ff", "color": "#0052cc", "border": "#0052cc"},
    "In Progress": {"bg": "#fff7e6", "color": "#974f0c", "border": "#ff991f"},
    "In Review": {"bg": "#f3f0ff", "color": "#5e4db2", "border": "#5e4db2"},
    "Done": {"bg": "#e3fcef", "color": "#006644", "border": "#36b37e"}
}

PRIORITY_COLORS = {
    "Low": {"bg": "#e3fcef", "color": "#216e4e", "icon": "▼"},
    "Medium": {"bg": "#fff7e6", "color": "#974f0c", "icon": "→"},
    "High": {"bg": "#ffd7d0", "color": "#ef3b20", "icon": "▲"},
    "Critical": {"bg": "#ffeceb", "color": "#ae2a19", "icon": "🔴"}
}

CATEGORY_COLORS = {
    "IT": {"bg": "#deebff", "color": "#0052cc"},
    "Development": {"bg": "#f3f0ff", "color": "#5e4db2"},
    "HR": {"bg": "#dffcf0", "color": "#216e4e"},
    "Finance": {"bg": "#fff7e6", "color": "#974f0c"},
    "Other": {"bg": "#f1f2f4", "color": "#626f86"}
}

# ── DB helpers ────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                description TEXT    NOT NULL,
                status      TEXT    NOT NULL DEFAULT 'To Do',
                assigned_to TEXT,
                submitter   TEXT,
                category    TEXT    NOT NULL DEFAULT 'Other',
                priority    TEXT    NOT NULL DEFAULT 'Medium',
                blocked     INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                password_hash TEXT    NOT NULL,
                role          TEXT    NOT NULL DEFAULT 'employee',
                created_at    TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migrate existing tables: add columns if missing
        ticket_columns = [row[1] for row in conn.execute("PRAGMA table_info(tickets)")]
        if "submitter" not in ticket_columns:
            conn.execute("ALTER TABLE tickets ADD COLUMN submitter TEXT")
        if "category" not in ticket_columns:
            conn.execute("ALTER TABLE tickets ADD COLUMN category TEXT NOT NULL DEFAULT 'Other'")
        if "priority" not in ticket_columns:
            conn.execute("ALTER TABLE tickets ADD COLUMN priority TEXT NOT NULL DEFAULT 'Medium'")
        if "blocked" not in ticket_columns:
            conn.execute("ALTER TABLE tickets ADD COLUMN blocked INTEGER NOT NULL DEFAULT 0")
        if "start_date" not in ticket_columns:
            conn.execute("ALTER TABLE tickets ADD COLUMN start_date TEXT")
        if "due_date" not in ticket_columns:
            conn.execute("ALTER TABLE tickets ADD COLUMN due_date TEXT")

        user_columns = [row[1] for row in conn.execute("PRAGMA table_info(users)")]
        if "role" not in user_columns:
            conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'employee'")

        conn.commit()

init_db()

# ── Routes ────────────────────────────────────────────────────────────────────

def get_user_by_username(username):
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()


def create_user(username, password, role="employee"):
    password_hash = generate_password_hash(password)
    with get_db() as conn:
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )
        conn.commit()


def seed_default_users():
    if not get_user_by_username("manager"):
        create_user("manager", "Manager123!", role="manager")
    if not get_user_by_username("agent"):
        create_user("agent", "Agent123!", role="agent")

seed_default_users()


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("list_tickets"))

    error = None
    message = request.args.get("message")
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_user_by_username(username)
        if user and check_password_hash(user["password_hash"], password):
            session["user"] = username
            session["role"] = user["role"]
            return redirect(url_for("list_tickets"))
        error = "Invalid username or password."

    return render_template("login.html", error=error, message=message)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("user"):
        return redirect(url_for("list_tickets"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not password:
            error = "Username and password are required."
        elif password != confirm:
            error = "Passwords do not match."
        elif get_user_by_username(username):
            error = "That username is already taken."
        else:
            create_user(username, password)
            return redirect(url_for("login", message="Account created successfully. Please sign in."))

    return render_template("signup.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return redirect("/tickets")


@app.route("/tickets/<int:ticket_id>/set_status", methods=["POST"])
@login_required
def set_status(ticket_id):
    role = session.get("role")
    if role != "manager":
        abort(403)
    new_status = request.form.get("status", "").strip()
    if new_status not in STATUS_ORDER:
        abort(400, "Invalid status")
    start_date = request.form.get("start_date", "").strip() or None
    due_date = request.form.get("due_date", "").strip() or None
    with get_db() as conn:
        row = conn.execute("SELECT status, blocked FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            abort(404, "Ticket not found.")
        if row["blocked"]:
            abort(400, "Ticket is blocked. Unblock to change status.")
        current = row["status"]
        def allowed_transition(curr, target, role_param):
            # Manager may set any status
            if role_param == 'manager':
                return True
            if target not in STATUS_ORDER:
                return False
            try:
                idx_curr = STATUS_ORDER.index(curr)
                idx_targ = STATUS_ORDER.index(target)
            except ValueError:
                return False
            # Normal forward by one
            if idx_targ - idx_curr == 1:
                return True
            # Allow skipping In Review from In Progress -> Done (optional step)
            if curr == "In Progress" and target == "Done":
                return True
            return False
        if not allowed_transition(current, new_status, role):
            abort(400, "Cannot skip status steps")
        sql_sets = "status = ?"
        params = [new_status]
        if start_date:
            sql_sets += ", start_date = ?"
            params.append(start_date)
        if due_date:
            sql_sets += ", due_date = ?"
            params.append(due_date)
        params.append(ticket_id)
        conn.execute(f"UPDATE tickets SET {sql_sets} WHERE id = ?", params)
        conn.commit()
    next_url = request.form.get('next') or request.args.get('next') or "/tickets"
    if not str(next_url).startswith('/'):
        next_url = '/tickets'
    return redirect(next_url)


@app.route("/tickets/<int:ticket_id>/block", methods=["POST"])
@login_required
def block_ticket(ticket_id):
    role = session.get("role")
    if role != "manager":
        abort(403)
    with get_db() as conn:
        row = conn.execute("SELECT blocked FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            abort(404, "Ticket not found.")
        blocked = bool(row["blocked"])
        if blocked:
            # Unblock
            conn.execute("UPDATE tickets SET blocked = 0 WHERE id = ?", (ticket_id,))
        else:
            # Mark blocked and return to To Do
            conn.execute("UPDATE tickets SET blocked = 1, status = 'To Do' WHERE id = ?", (ticket_id,))
        conn.commit()
    next_url = request.form.get('next') or request.args.get('next') or "/tickets"
    if not str(next_url).startswith('/'):
        next_url = '/tickets'
    return redirect(next_url)


@app.route("/tickets/<int:ticket_id>/classify", methods=["POST"])
@login_required
def classify_ticket(ticket_id):
    category = request.form.get("category", "").strip()
    if category not in CATEGORIES:
        abort(400, "Invalid category.")
    user = session.get("user")
    role = session.get("role")
    with get_db() as conn:
        row = conn.execute("SELECT submitter FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            abort(404, "Ticket not found.")
        if role not in ("manager", "agent") and row["submitter"] != user:
            abort(403)
        conn.execute(
            "UPDATE tickets SET category = ? WHERE id = ?",
            (category, ticket_id),
        )
        conn.commit()
    next_url = request.form.get('next') or request.args.get('next') or "/tickets"
    if not str(next_url).startswith('/'):
        next_url = '/tickets'
    return redirect(next_url)

@app.route("/tickets/<int:ticket_id>/priority", methods=["POST"])
@login_required
def set_priority(ticket_id):
    priority = request.form.get("priority", "").strip()
    if priority not in PRIORITIES:
        abort(400, "Invalid priority.")
    role = session.get("role")
    if role != "manager":
        abort(403)
    with get_db() as conn:
        row = conn.execute("SELECT id FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            abort(404, "Ticket not found.")
        conn.execute(
            "UPDATE tickets SET priority = ? WHERE id = ?",
            (priority, ticket_id),
        )
        conn.commit()
    next_url = request.form.get('next') or request.args.get('next') or "/tickets"
    if not str(next_url).startswith('/'):
        next_url = '/tickets'
    return redirect(next_url)

@app.route("/tickets")
@login_required
def list_tickets():
    user = session.get("user")
    role = session.get("role")
    with get_db() as conn:
        if role == "manager":
            rows = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()
        elif role == "agent":
            rows = conn.execute("SELECT * FROM tickets WHERE assigned_to = ? OR submitter = ? ORDER BY id DESC", (user, user)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM tickets WHERE submitter = ? ORDER BY id DESC", (user,)).fetchall()
    
    tickets = [dict(r) for r in rows]
    
    # Organize tickets by category and status
    organized_tickets = {}
    for category in CATEGORIES:
        organized_tickets[category] = {}
        for status in STATUS_ORDER:
            organized_tickets[category][status] = []
    
    # Categorize tickets
    for ticket in tickets:
        cat = ticket.get("category", "Other") or "Other"
        if cat not in organized_tickets:
            cat = "Other"
        status = ticket.get("status", "To Do") or "To Do"
        if status not in organized_tickets[cat]:
            organized_tickets[cat]["To Do"] = []
            status = "To Do"
        organized_tickets[cat][status].append(ticket)
    
    # Calculate stats
    stats = {
        "total":       len(tickets),
        "todo":        sum(1 for t in tickets if t["status"] == "To Do"),
        "in_progress": sum(1 for t in tickets if t["status"] == "In Progress"),
        "done":        sum(1 for t in tickets if t["status"] == "Done"),
    }
    
    return render_template(
        "tickets.html",
        tickets=tickets,
        organized_tickets=organized_tickets,
        stats=stats,
        status_flow=STATUS_FLOW,
        categories=CATEGORIES,
        priorities=PRIORITIES,
        status_colors=STATUS_COLORS,
        priority_colors=PRIORITY_COLORS,
        category_colors=CATEGORY_COLORS
    )

@app.route("/submit")
@login_required
def submit_page():
    return render_template("submit.html")

@app.route("/tickets", methods=["POST"])
@login_required
def create_ticket():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    category = request.form.get("category", "Other").strip()
    priority = request.form.get("priority", "Medium").strip()
    
    if category not in CATEGORIES:
        category = "Other"
    if priority not in PRIORITIES:
        priority = "Medium"
    if not title or not description:
        abort(400, "Title and description are required.")
    
    submitter = session.get("user")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO tickets (title, description, status, submitter, category, priority) VALUES (?, ?, 'To Do', ?, ?, ?)",
            (title, description, submitter, category, priority)
        )
        conn.commit()
    return redirect("/tickets")

@app.route("/tickets/<int:ticket_id>/assign", methods=["POST"])
@login_required
def assign_ticket(ticket_id):
    role = session.get("role")
    if role != "manager":
        abort(403)
    assigned_to = request.form.get("assigned_to", "").strip()
    start_date = request.form.get("start_date", "").strip() or None
    due_date = request.form.get("due_date", "").strip() or None
    with get_db() as conn:
        row = conn.execute("SELECT id FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            abort(404, "Ticket not found.")
        conn.execute(
            "UPDATE tickets SET assigned_to = ?, start_date = ?, due_date = ? WHERE id = ?",
            (assigned_to, start_date, due_date, ticket_id)
        )
        conn.commit()
    next_url = request.form.get('next') or request.args.get('next') or "/tickets"
    if not str(next_url).startswith('/'):
        next_url = '/tickets'
    return redirect(next_url)

@app.route("/tickets/<int:ticket_id>/status", methods=["POST"])
@login_required
def advance_status(ticket_id):
    role = session.get("role")
    if role != "manager":
        abort(403)
    with get_db() as conn:
        row = conn.execute("SELECT status, blocked FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            abort(404, "Ticket not found.")
        if row["blocked"]:
            abort(400, "Ticket is blocked. Unblock to change status.")
        current = row["status"]
        # Allow an explicit status from the form (radio selection), otherwise use default next
        target = request.form.get("status", "").strip()
        if not target:
            target = STATUS_FLOW.get(current)
            if not target:
                abort(400, "Ticket is already Done.")

        def allowed_transition(curr, target, role_param):
            if role_param == 'manager':
                return True
            if target not in STATUS_ORDER:
                return False
            try:
                idx_curr = STATUS_ORDER.index(curr)
                idx_targ = STATUS_ORDER.index(target)
            except ValueError:
                return False
            if idx_targ - idx_curr == 1:
                return True
            if curr == "In Progress" and target == "Done":
                return True
            return False

        if not allowed_transition(current, target, role):
            abort(400, "Invalid status transition")

        start_date = request.form.get("start_date", "").strip() or None
        due_date = request.form.get("due_date", "").strip() or None

        sql_sets = "status = ?"
        params = [target]
        if start_date:
            sql_sets += ", start_date = ?"
            params.append(start_date)
        if due_date:
            sql_sets += ", due_date = ?"
            params.append(due_date)
        params.append(ticket_id)
        conn.execute(f"UPDATE tickets SET {sql_sets} WHERE id = ?", params)
        conn.commit()
    next_url = request.form.get('next') or request.args.get('next') or "/tickets"
    if not str(next_url).startswith('/'):
        next_url = '/tickets'
    return redirect(next_url)


@app.route("/tickets/<int:ticket_id>/reopen", methods=["POST"])
@login_required
def reopen_ticket(ticket_id):
    user = session.get("user")
    role = session.get("role")
    with get_db() as conn:
        row = conn.execute("SELECT status, submitter FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
        if not row:
            abort(404, "Ticket not found.")
        if row["status"] != "Done":
            abort(400, "Ticket is not Done.")
        # allow manager or the original submitter to reopen
        if role != "manager" and row["submitter"] != user:
            abort(403)
        conn.execute("UPDATE tickets SET status = 'In Review', blocked = 0 WHERE id = ?", (ticket_id,))
        conn.commit()
    next_url = request.form.get('next') or request.args.get('next') or "/tickets"
    if not str(next_url).startswith('/'):
        next_url = '/tickets'
    return redirect(next_url)


@app.route("/tickets/<int:ticket_id>")
@login_required
def view_ticket(ticket_id):
    user = session.get("user")
    role = session.get("role")
    with get_db() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if not row:
        abort(404, "Ticket not found.")
    ticket = dict(row)
    if role == "manager":
        # Manager can view all tickets
        pass
    elif role == "agent":
        # Agent can view tickets assigned to them or submitted by them
        if ticket.get("assigned_to") != user and ticket.get("submitter") != user:
            abort(403)
    else:
        # Employee can only view tickets they submitted
        if ticket.get("submitter") != user:
            abort(403)
    return render_template(
        "ticket_detail.html",
        ticket=ticket,
        categories=CATEGORIES,
        priorities=PRIORITIES,
        status_flow=STATUS_FLOW,
        status_colors=STATUS_COLORS,
        priority_colors=PRIORITY_COLORS,
        category_colors=CATEGORY_COLORS,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, port=port)
