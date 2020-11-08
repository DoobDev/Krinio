CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "k!",
    LogChannel text,
    CodeChannel text,
    ReadyUpChannel text,
    Ping text DEFAULT "@here"
);

CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS games(
    MessageID integer,
    GuildID integer,
    ReactionCount integer DEFAULT 1,
    PRIMARY KEY("MessageID", "GuildID")
)