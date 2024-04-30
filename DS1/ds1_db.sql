CREATE TABLE Osoba
(
 uID INTEGER NOT NULL,
 jmeno VARCHAR2(30) NOT NULL,
 mesto VARCHAR2(30) NOT NULL,
 rok_narozeni INTEGER NULL,
 email VARCHAR2(30) NULL,
 zeme VARCHAR2(30) NOT NULL,
 status INTEGER NOT NULL,
 CONSTRAINT PK_osoba PRIMARY KEY (uID)
)
;
CREATE TABLE Zbozi
(
 zID INTEGER NOT NULL,
 kategorie INTEGER NOT NULL,
 nazev VARCHAR2(30) NOT NULL,
 rok_vyroby INTEGER NOT NULL,
 aktualni_cena INTEGER NOT NULL,
 CONSTRAINT PK_Zbozi PRIMARY KEY (zID)
)
;
CREATE TABLE Pobocka
(
 pID INTEGER NOT NULL,
 mesto VARCHAR2(30) NOT NULL,
 status INTEGER NOT NULL,
 CONSTRAINT PK_pobocka PRIMARY KEY (pID)
)
;
CREATE TABLE Zamestnanec
(
 zaID INTEGER NOT NULL,
 pID INTEGER NOT NULL,
 jmeno VARCHAR2(30) NOT NULL,
 datum_narozeni Date NOT NULL,
 platova_trida INTEGER NOT NULL,
 CONSTRAINT PK_zamestnanec PRIMARY KEY (zaID),
 CONSTRAINT FK_zamestnanec_pobocka FOREIGN KEY (pID) REFERENCES Pobocka(pID)
)
;
CREATE TABLE Objednavka
(
 oID INTEGER NOT NULL,
 uID INTEGER NOT NULL,
 vytvorena TIMESTAMP NOT NULL,
 potvrzena TIMESTAMP NULL,
 dorucena TIMESTAMP NULL,
 zaID INTEGER NOT NULL,
 CONSTRAINT PK_objednavka PRIMARY KEY (oID),
 CONSTRAINT FK_objednavka_osoba FOREIGN KEY (uID) REFERENCES Osoba(uID),
 CONSTRAINT FK_objednavka_zamestnanec FOREIGN KEY (zaID) REFERENCES Zamestnanec(zaID)
)
;
CREATE TABLE Polozka
(
 oID INTEGER NOT NULL,
 zID INTEGER NOT NULL,
 cena INTEGER NOT NULL,
 kusu INTEGER NOT NULL,
 CONSTRAINT PK_polozka PRIMARY KEY (oID,zID),
 CONSTRAINT FK_polozka_objednavka FOREIGN KEY (oID) REFERENCES Objednavka(oID),
 CONSTRAINT FK_polozka_zbozi FOREIGN KEY (zID) REFERENCES Zbozi(zID)
)
;
CREATE TABLE Sklad
(
 pID INTEGER NOT NULL,
 zID INTEGER NOT NULL,
 kusu INTEGER NOT NULL,
 CONSTRAINT PK_sklad PRIMARY KEY (pID,zID),
 CONSTRAINT FK_sklad_pobocka FOREIGN KEY (pID) REFERENCES Pobocka(pID),
 CONSTRAINT FK_sklad_zbozi FOREIGN KEY (zID) REFERENCES Zbozi(zID)
)
;