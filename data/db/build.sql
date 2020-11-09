CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "k!",
    LogChannel text,
    CodeChannel text,
    ReadyUpChannel text,
    Ping text DEFAULT "None, set the ping by doing k!setping",
    MatchHistory text
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