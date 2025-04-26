-- Sequences for Auto-incrementing Primary Keys

-- Sequence for Felhasznalok (Users)
CREATE SEQUENCE felhasznalok_seq
START WITH 100
INCREMENT BY 1
NOCACHE;

-- Sequence for Felhasznalo_kapcsolatok (User Connections) - this table does not need a sequence, as the primary key is a composite key
-- No sequence needed for Felhasznalo_kapcsolatok

-- Sequence for Csoportok (Groups)
CREATE SEQUENCE csoportok_seq
START WITH 100
INCREMENT BY 1
NOCACHE;

-- Sequence for Felhasznalo_Csoportok (User Groups) - No primary key auto-increment required for this table
-- No sequence needed for Felhasznalo_Csoportok

-- Sequence for Uzenetek (Messages)
CREATE SEQUENCE uzenetek_seq
START WITH 100
INCREMENT BY 1
NOCACHE;

-- Sequence for Bejegyzesek (Posts)
CREATE SEQUENCE bejegyzesek_seq
START WITH 100
INCREMENT BY 1
NOCACHE;

-- Sequence for Kommentek (Comments)
CREATE SEQUENCE kommentek_seq
START WITH 100
INCREMENT BY 1
NOCACHE;