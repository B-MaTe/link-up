-- Felhasználók
CREATE TABLE Felhasznalok (
    id NUMBER(10) PRIMARY KEY,
    felhasznalonev VARCHAR2(50) UNIQUE NOT NULL,
    jelszo VARCHAR2(128) NOT NULL,
    admin NUMBER(1) CHECK (admin IN (0, 1)),
    utolso_bejelentkezes TIMESTAMP,
    csatlakozas_ido TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Kapcsolatok
CREATE TABLE Felhasznalo_kapcsolatok (
    jelolo_id NUMBER(10),
    jelolt_id NUMBER(10),
    statusz VARCHAR2(11) CHECK (statusz IN ('pending', 'accepted', 'rejected')),
    PRIMARY KEY (jelolo_id, jelolt_id),
    FOREIGN KEY (jelolo_id) REFERENCES Felhasznalok(id) ON DELETE CASCADE,
    FOREIGN KEY (jelolt_id) REFERENCES Felhasznalok(id) ON DELETE CASCADE
);

-- Csoportok
CREATE TABLE Csoportok (
    id NUMBER(10) PRIMARY KEY,
    felhasznalo_id NUMBER(10),
    letrehozas_ido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (felhasznalo_id) REFERENCES Felhasznalok(id) ON DELETE SET NULL
);

-- Felhasználó Csoportok
CREATE TABLE Felhasznalo_Csoportok (
    csoport_id NUMBER(10),
    felhasznalo_id NUMBER(10),
    PRIMARY KEY (csoport_id, felhasznalo_id),
    FOREIGN KEY (csoport_id) REFERENCES Csoportok(id) ON DELETE CASCADE,
    FOREIGN KEY (felhasznalo_id) REFERENCES Felhasznalok(id) ON DELETE CASCADE
);

-- Üzenetek
CREATE TABLE Uzenetek (
    id NUMBER(10) PRIMARY KEY,
    felhasznalo_id NUMBER(10),
    csoport_id NUMBER(10),
    kuldesi_ido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tartalom VARCHAR2(1000),
    FOREIGN KEY (felhasznalo_id) REFERENCES Felhasznalok(id) ON DELETE SET NULL,
    FOREIGN KEY (csoport_id) REFERENCES Csoportok(id) ON DELETE SET NULL
);

-- Bejegyzések
CREATE TABLE Bejegyzesek (
    id NUMBER(10) PRIMARY KEY,
    felhasznalo_id NUMBER(10),
    feltoltott_kep VARCHAR2(128),
    letrehozasi_ido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tartalom VARCHAR2(1000),
    FOREIGN KEY (felhasznalo_id) REFERENCES Felhasznalok(id) ON DELETE CASCADE
);

-- Kommentek
CREATE TABLE Kommentek (
    id NUMBER(10) PRIMARY KEY,
    felhasznalo_id NUMBER(10),
    bejegyzes_id NUMBER(10),
    feltoltesi_ido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tartalom VARCHAR2(1000),
    FOREIGN KEY (felhasznalo_id) REFERENCES Felhasznalok(id) ON DELETE SET NULL,
    FOREIGN KEY (bejegyzes_id) REFERENCES Bejegyzesek(id) ON DELETE CASCADE
);





