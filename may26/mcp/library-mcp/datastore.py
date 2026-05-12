BOOKS: dict[str, dict] = {
    "B001": {
        "id": "B001",
        "title": "The C Programming Language",
        "author": "Brian W. Kernighan, Dennis M. Ritchie",
        "year": 1978,
        "available_copies": 2,
        "total_copies": 10,
        "genre": "Programming",
        "available": True,
        "active": True,
        "tags": ["programming", "C", "beginner"],
        "isbn": "9780131103627"
    },

    "B002": {
        "id": "B002",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "year": 2008,
        "available_copies": 4,
        "total_copies": 8,
        "genre": "Software Engineering",
        "available": True,
        "active": True,
        "tags": ["clean-code", "best-practices", "software-engineering"],
        "isbn": "9780132350884"
    },

    "B003": {
        "id": "B003",
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "year": 2009,
        "available_copies": 1,
        "total_copies": 5,
        "genre": "Algorithms",
        "available": True,
        "active": True,
        "tags": ["algorithms", "data-structures", "cs-core"],
        "isbn": "9780262033848"
    },

    "B004": {
        "id": "B004",
        "title": "Design Patterns",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "year": 1994,
        "available_copies": 3,
        "total_copies": 6,
        "genre": "Software Design",
        "available": True,
        "active": True,
        "tags": ["design-patterns", "oop", "architecture"],
        "isbn": "9780201633610"
    },

    "B005": {
        "id": "B005",
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "year": 2019,
        "available_copies": 5,
        "total_copies": 10,
        "genre": "Programming",
        "available": True,
        "active": True,
        "tags": ["python", "beginner", "hands-on"],
        "isbn": "9781593279288"
    },

    "B006": {
        "id": "B006",
        "title": "Computer Networking: A Top-Down Approach",
        "author": "James F. Kurose, Keith W. Ross",
        "year": 2021,
        "available_copies": 2,
        "total_copies": 7,
        "genre": "Networking",
        "available": True,
        "active": True,
        "tags": ["networking", "tcp-ip", "computer-networks"],
        "isbn": "9780136681557"
    },

    "B007": {
        "id": "B007",
        "title": "Operating System Concepts",
        "author": "Abraham Silberschatz",
        "year": 2018,
        "available_copies": 2,
        "total_copies": 6,
        "genre": "Operating Systems",
        "available": True,
        "active": True,
        "tags": ["os", "processes", "threads"],
        "isbn": "9781119456339"
    },

    "B008": {
        "id": "B008",
        "title": "Database System Concepts",
        "author": "Abraham Silberschatz, Henry F. Korth, S. Sudarshan",
        "year": 2019,
        "available_copies": 3,
        "total_copies": 6,
        "genre": "Databases",
        "available": True,
        "active": True,
        "tags": ["sql", "database", "dbms"],
        "isbn": "9780078022159"
    },

    "B009": {
        "id": "B009",
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "year": 2019,
        "available_copies": 4,
        "total_copies": 8,
        "genre": "Software Engineering",
        "available": True,
        "active": True,
        "tags": ["career", "software-development", "best-practices"],
        "isbn": "9780135957059"
    },

    "B010": {
        "id": "B010",
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell, Peter Norvig",
        "year": 2020,
        "available_copies": 1,
        "total_copies": 4,
        "genre": "Artificial Intelligence",
        "available": True,
        "active": True,
        "tags": ["ai", "machine-learning", "intelligent-systems"],
        "isbn": "9780134610993"
    },

    "B011": {
        "id": "B011",
        "title": "Atomic Habits",
        "author": "James Clear",
        "year": 2018,
        "available_copies": 6,
        "total_copies": 10,
        "genre": "Self Help",
        "available": True,
        "active": True,
        "tags": ["habits", "productivity", "motivation"],
        "isbn": "9780735211292"
    },

    "B012": {
        "id": "B012",
        "title": "Deep Work",
        "author": "Cal Newport",
        "year": 2016,
        "available_copies": 5,
        "total_copies": 9,
        "genre": "Productivity",
        "available": True,
        "active": True,
        "tags": ["focus", "productivity", "career"],
        "isbn": "9781455586691"
    },

    "B013": {
        "id": "B013",
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "year": 2015,
        "available_copies": 4,
        "total_copies": 7,
        "genre": "History",
        "available": True,
        "active": True,
        "tags": ["history", "humanity", "science"],
        "isbn": "9780062316097"
    },

    "B014": {
        "id": "B014",
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "year": 2020,
        "available_copies": 5,
        "total_copies": 8,
        "genre": "Finance",
        "available": True,
        "active": True,
        "tags": ["money", "finance", "investing"],
        "isbn": "9780857197689"
    },

    "B015": {
        "id": "B015",
        "title": "Zero to One",
        "author": "Peter Thiel",
        "year": 2014,
        "available_copies": 3,
        "total_copies": 6,
        "genre": "Business",
        "available": True,
        "active": True,
        "tags": ["startups", "business", "innovation"],
        "isbn": "9780804139298"
    }
}


STUDENTS: dict[str, dict] = {
    "S001": {
        "id": "S001",
        "name": "Rahul Sharma",
        "email": "rahul.sharma@example.com",
        "major": "Computer Science",
        "year": 2,
        "books_borrowed": ["B001", "B002"],
        "active": True
    },

    "S002": {
        "id": "S002",
        "name": "Priya Reddy",
        "email": "priya.reddy@example.com",
        "major": "Software Engineering",
        "year": 3,
        "books_borrowed": ["B003", "B004", "B005"],
        "active": True
    },

    "S003": {
        "id": "S003",
        "name": "Arjun Patel",
        "email": "arjun.patel@example.com",
        "major": "Data Science",
        "year": 1,
        "books_borrowed": ["B006", "B007"],
        "active": True
    },

    "S004": {
        "id": "S004",
        "name": "Sneha Verma",
        "email": "sneha.verma@example.com",
        "major": "Artificial Intelligence",
        "year": 4,
        "books_borrowed": ["B008", "B009", "B010"],
        "active": True
    },

    "S005": {
        "id": "S005",
        "name": "Kiran Kumar",
        "email": "kiran.kumar@example.com",
        "major": "Cybersecurity",
        "year": 2,
        "books_borrowed": ["B011", "B012"],
        "active": True
    }
}
