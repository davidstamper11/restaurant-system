INSERT INTO reviewers (
    id,
    name,
    email,
    is_admin_yn,
    created_by,
    created_on,
    deleted_by,
    password
) VALUES (
    NULL,                     -- id (auto‑increment)
    'David Stamper',          -- name
    'david.stamper11@gmail.com',      -- email (unique, required)
    1,                        -- is_admin_yn (0 = false, 1 = true)
    1,                     -- created_by (FK to reviewers.id, nullable)
    datetime('now'),          -- created_on (timestamp)
    NULL,                     -- deleted_by (FK to reviewers.id, nullable)
    'foobar11'        -- password (nullable, store hashed in practice)
);