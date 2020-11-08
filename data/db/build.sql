CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "k!",
    LogChannel text,
    CodeChannel text,
    ReadyUpChannel text
);

CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY
)