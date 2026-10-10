"""Codium Lab - Интерактивный тестовый стенд для VSCodium & Python 3.12."""

from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

console = Console()
DB_PATH = Path(__file__).parent / "lab.db"


@dataclass(frozen=True, slots=True)
class Developer:
    id: int
    username: str
    role: str
    github: str
    commits: int
    status: str


def init_database() -> None:
    """Создает SQLite базу данных lab.db с тестовыми данными для qwtel.sqlite-viewer."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS audit_log")
        cursor.execute("DROP TABLE IF EXISTS projects")
        cursor.execute("DROP TABLE IF EXISTS users")

        cursor.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL,
                github_handle TEXT NOT NULL,
                commits_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                stack TEXT NOT NULL,
                stars INTEGER DEFAULT 0,
                owner_id INTEGER,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                details TEXT
            )
            """
        )

        # Тестовые данные
        sample_users = [
            ("dimonjolo", "Lead Dev", "@dimonjolo", 342),
            ("alex_code", "Backend Eng", "@alexcode", 128),
            ("elena_ui", "Frontend Designer", "@elena-ui", 95),
            ("ai_agent", "Pair Programmer", "@antigravity", 1024),
        ]
        cursor.executemany(
            "INSERT INTO users (username, role, github_handle, commits_count) VALUES (?, ?, ?, ?)",
            sample_users,
        )

        sample_projects = [
            ("codium-lab", "Python 3.12, uv, Ruff, SQLite", 42, 1),
            ("shatterlab", "BeamNG Lua, Python MCP", 128, 1),
            ("telegram-beamng-mcp", "FastAPI, Telegram Bot, MCP", 77, 1),
            ("starship-terminal", "PowerShell, JetBrains Mono, Starship", 15, 1),
        ]
        cursor.executemany(
            "INSERT INTO projects (name, stack, stars, owner_id) VALUES (?, ?, ?, ?)",
            sample_projects,
        )

        cursor.execute(
            "INSERT INTO audit_log (action, timestamp, details) VALUES (?, ?, ?)",
            ("GH_AUTH_SUCCESS", datetime.now().isoformat(), "GitHub CLI authenticated as dimonjolo"),
        )
        conn.commit()


def fetch_developers() -> list[Developer]:
    """Извлекает разработчиков из SQLite базы данных."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, github_handle, commits_count FROM users ORDER BY commits_count DESC")
        rows = cursor.fetchall()
        return [
            Developer(
                id=r[0],
                username=r[1],
                role=r[2],
                github=r[3],
                commits=r[4],
                status="Active" if r[4] > 100 else "Junior",
            )
            for r in rows
        ]


def display_showcase() -> None:
    """Отображает интерактивный дашборд в терминале."""
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]✦ VSCodium Developer Lab ✦[/bold cyan]\n"
            "[dim]Python 3.12 • uv • SQLite Viewer • Git & gh • JetBrains Mono[/dim]",
            border_style="magenta",
            padding=(1, 4),
        )
    )

    with Progress(
        SpinnerColumn("dots", style="bright_cyan"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30, style="magenta", complete_style="green"),
        console=console,
        transient=True,
    ) as progress:
        task1 = progress.add_task("[cyan]Инициализация SQLite базы (lab.db)...", total=100)
        init_database()
        for _ in range(5):
            time.sleep(0.04)
            progress.advance(task1, 20)

    developers = fetch_developers()

    table = Table(
        title="[bold green]👥 Команда и активность (из lab.db)[/bold green]",
        box=box.ROUNDED,
        header_style="bold bright_blue",
        show_lines=True,
    )
    table.add_column("ID", justify="center", style="dim", width=4)
    table.add_column("Пользователь", style="bold white")
    table.add_column("Роль", style="yellow")
    table.add_column("GitHub", style="cyan")
    table.add_column("Коммиты", justify="right", style="green")
    table.add_column("Статус", justify="center")

    for dev in developers:
        status_tag = "[bold green]● Active[/bold green]" if dev.status == "Active" else "[dim]○ Ready[/dim]"
        table.add_row(
            str(dev.id),
            dev.username,
            dev.role,
            dev.github,
            f"{dev.commits:,}",
            status_tag,
        )

    console.print(table)
    console.print(
        f"[dim green]✓ База данных сохранена в [bold]{DB_PATH.name}[/bold]. Кликните по ней в VSCodium для GUI-просмотра![/dim green]\n"
    )


if __name__ == "__main__":
    display_showcase()
