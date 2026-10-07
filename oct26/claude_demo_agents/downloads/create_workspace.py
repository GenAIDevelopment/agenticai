from pathlib import Path
import random
import string


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DOWNLOADS_DIR = Path("downloads/downloads")

MIN_FILES = 30
MAX_FILES = 60

MIN_FILE_SIZE_KB = 10
MAX_FILE_SIZE_KB = 5000


# ---------------------------------------------------------
# Sample file names
# ---------------------------------------------------------

FILE_NAMES = {
    ".pdf": [
        "invoice",
        "project_report",
        "meeting_notes",
        "user_manual",
        "bank_statement",
        "resume",
        "technical_document",
        "requirements",
        "monthly_report",
    ],
    ".docx": [
        "project_plan",
        "meeting_notes",
        "resume",
        "proposal",
        "requirements",
        "documentation",
        "training_material",
    ],
    ".xlsx": [
        "sales_report",
        "employee_data",
        "budget",
        "expenses",
        "inventory",
        "customer_data",
        "financial_report",
    ],
    ".pptx": [
        "project_presentation",
        "quarterly_review",
        "training",
        "company_overview",
        "architecture",
        "product_demo",
    ],
    ".jpg": [
        "IMG",
        "photo",
        "vacation",
        "screenshot",
        "profile",
        "image",
    ],
    ".png": [
        "screenshot",
        "diagram",
        "architecture",
        "logo",
        "image",
    ],
    ".zip": [
        "project",
        "backup",
        "source_code",
        "documents",
        "photos",
        "deployment",
    ],
    ".csv": [
        "customers",
        "orders",
        "products",
        "transactions",
        "employees",
        "sales",
    ],
    ".txt": [
        "notes",
        "todo",
        "passwords_backup",
        "commands",
        "readme",
    ],
    ".json": [
        "config",
        "data",
        "products",
        "customers",
        "settings",
    ],
    ".log": [
        "application",
        "server",
        "deployment",
        "error",
        "debug",
    ],
}


# ---------------------------------------------------------
# Random helpers
# ---------------------------------------------------------

def random_string(length=8):
    """Generate a random alphanumeric string."""
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choices(characters, k=length))


def random_date():
    """Generate a random date-like suffix."""
    year = random.randint(2023, 2026)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    return f"{year}-{month:02d}-{day:02d}"


def random_filename(extension):
    """Generate a realistic randomized filename."""
    base_name = random.choice(FILE_NAMES[extension])

    styles = [
        f"{base_name}_{random.randint(1, 999)}",
        f"{base_name}_{random_date()}",
        f"{base_name} ({random.randint(1, 5)})",
        f"{base_name}_{random_string(5)}",
        base_name,
    ]

    return random.choice(styles) + extension


# ---------------------------------------------------------
# File creation
# ---------------------------------------------------------

def create_file(path, size_kb):
    """Create a dummy file with the requested approximate size."""
    size_bytes = size_kb * 1024

    with path.open("wb") as file:
        remaining = size_bytes

        while remaining > 0:
            chunk_size = min(1024 * 1024, remaining)

            file.write(
                random.randbytes(chunk_size)
            )

            remaining -= chunk_size


def random_size():
    """Generate a somewhat realistic file size."""
    size_type = random.choice(
        [
            "tiny",
            "small",
            "medium",
            "large",
        ]
    )

    if size_type == "tiny":
        return random.randint(10, 100)

    if size_type == "small":
        return random.randint(100, 500)

    if size_type == "medium":
        return random.randint(500, 2000)

    return random.randint(2000, MAX_FILE_SIZE_KB)


# ---------------------------------------------------------
# Main logic
# ---------------------------------------------------------

def create_downloads_folder():
    """Create a randomized fake Downloads folder."""

    DOWNLOADS_DIR.mkdir(exist_ok=True)

    # Some folders commonly found inside Downloads
    folders = [
        DOWNLOADS_DIR,
        DOWNLOADS_DIR / "Documents",
        DOWNLOADS_DIR / "Images",
        DOWNLOADS_DIR / "Projects",
        DOWNLOADS_DIR / "Archives",
    ]

    # Randomly decide which folders should exist
    selected_folders = random.sample(
        folders,
        random.randint(2, len(folders)),
    )

    for folder in selected_folders:
        folder.mkdir(parents=True, exist_ok=True)

    total_files = random.randint(MIN_FILES, MAX_FILES)

    extensions = list(FILE_NAMES.keys())

    for _ in range(total_files):

        extension = random.choice(extensions)

        filename = random_filename(extension)

        folder = random.choice(selected_folders)

        file_path = folder / filename

        # Avoid duplicate filenames
        while file_path.exists():
            filename = random_filename(extension)
            file_path = folder / filename

        size_kb = random_size()

        create_file(
            file_path,
            size_kb,
        )

        print(
            f"Created: {file_path} "
            f"({size_kb:,} KB)"
        )

    print()
    print("=" * 50)
    print("Fake Downloads folder created!")
    print(f"Location: {DOWNLOADS_DIR.absolute()}")
    print(f"Files created: {total_files}")
    print("=" * 50)


if __name__ == "__main__":
    create_downloads_folder()