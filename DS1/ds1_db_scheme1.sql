Osoba : uID ( INTEGER , PRIMARY KEY ) ,  jmeno ( VARCHAR2 ) ,  mesto ( VARCHAR2 ) ,  rok_narozeni ( INTEGER ) ,  email ( VARCHAR2 ) ,  zeme ( VARCHAR2 ) ,  status ( INTEGER ) | Zbozi : zID ( INTEGER , PRIMARY KEY ) ,  kategorie ( INTEGER ) ,  nazev ( VARCHAR2 ) ,  rok_vyroby ( INTEGER ) ,  aktualni_cena ( INTEGER ) | Pobocka : pID ( INTEGER , PRIMARY KEY ) ,  mesto ( VARCHAR2 ) ,  status ( INTEGER ) | Zamestnanec : zaID ( INTEGER , PRIMARY KEY ) ,  pID ( INTEGER , FOREIGN KEY (Pobocka.pID) ) ,  jmeno ( VARCHAR2 ) ,  datum_narozeni ( Date ) ,  platova_trida ( INTEGER ) | Objednavka : oID ( INTEGER , PRIMARY KEY ) ,  uID ( INTEGER , FOREIGN KEY (Osoba.uID) ) ,  vytvorena ( TIMESTAMP ) ,  potvrzena ( TIMESTAMP ) ,  dorucena ( TIMESTAMP ) ,  zaID ( INTEGER , FOREIGN KEY (Zamestnanec.zaID) ) | Polozka : oID ( INTEGER , FOREIGN KEY (Objednavka.oID) ) ,  zID ( INTEGER , FOREIGN KEY (Zbozi.zID) ) ,  cena ( INTEGER ) ,  kusu ( INTEGER ) | Sklad : pID ( INTEGER , FOREIGN KEY (Pobocka.pID) ) ,  zID ( INTEGER , FOREIGN KEY (Zbozi.zID) ) ,  kusu ( INTEGER )