DROP TABLE IF EXISTS areas;
DROP TABLE IF EXISTS discussions;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS friendlist;
DROP TABLE IF EXISTS directmessages;
CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    names TEXT UNIQUE,
    deleted BOOLEAN
);
CREATE TABLE discussions (
    id SERIAL PRIMARY KEY,
    names TEXT UNIQUE,
    area TEXT,
    starter TEXT,
    created_at TIMESTAMP,
    deleted BOOLEAN
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    writer TEXT,
    discussion TEXT,
    content TEXT,
    created_at TIMESTAMP,
    deleted BOOLEAN
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    names TEXT UNIQUE,
    passwords TEXT,
    admins BOOLEAN,
    deleted BOOLEAN
);
CREATE TABLE friendlist (
    id SERIAL PRIMARY KEY,
    user1 TEXT,
    user2 TEXT,
    UNIQUE (user1, user2),
    deleted BOOLEAN
);
CREATE TABLE directmessages (
    id SERIAL PRIMARY KEY,
    user1 TEXT,
    user2 TEXT,
    UNIQUE(user1,user2),
    messages TEXT,
    deleted BOOLEAN
);
INSERT INTO areas (names, deleted) VALUES ('Yleinen chatti', FALSE);
INSERT INTO users (names, passwords, admins, deleted) VALUES ('user', 'scrypt:32768:8:1$YreVQMZh7iqGMaJF$6024b6ad1e4889d964e834d770331b4743d0c2e00644fc8680190f2814af789225862a4c1bba78827f0cfbed817bca5ade255500dce64fe2bf610e2ea59de4fd', FALSE, FALSE);
INSERT INTO users (names, passwords, admins, deleted) VALUES ('admin', 'scrypt:32768:8:1$YreVQMZh7iqGMaJF$6024b6ad1e4889d964e834d770331b4743d0c2e00644fc8680190f2814af789225862a4c1bba78827f0cfbed817bca5ade255500dce64fe2bf610e2ea59de4fd', TRUE, FALSE);