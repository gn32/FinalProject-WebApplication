CREATE DATABASE records;
use records;


CREATE TABLE IF NOT EXISTS tblrecords (
#     id INT NOT NULL AUTO_INCREMENT,
    Name VARCHAR(10) CHARACTER SET utf8,
    Sex VARCHAR(10) CHARACTER SET utf8,
    Age INT,
    Height_in INT,
    Weight_lbs INT
#     PRIMARY KEY (id)
);

INSERT INTO tblrecords (Name, Sex, Age, Height_in, Weight_lbs) VALUES
    ('Alex','M',   41,       74,      170),
    ('Bert','M',   42,       68,      166),
    ('Carl','M',   32,       70,      155),
    ('Dave','M',   39,       72,      167),
    ('Elly','F',   30,       66,      124),
    ('Fran','M',   33,       66,      115),
    ('Gwen','F',   26,       64,      121),
    ('Hank','M',   30,       71,      158),
    ('Ivan','F',   53,       72,      175),
    ('Jake','M',   32,       69,      143),
    ('Kate','F',   47,       69,      139),
    ('Luke','M',   34,       72,      163),
    ('Myra','F',   23,       62,       98),
    ('Neil','M',   36,       75,      160),
    ('Omar','M',   38,       70,      145),
    ('Page','F',   31,       67,      135),
    ('Quin','M',   29,       71,      176),
    ('Ruth','F',   28,       65,      131);
