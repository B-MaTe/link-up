-- Felhasznalok

INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (1, 'adam12', 'pbkdf2_sha256$870000$kBehxt8YZVmOoO82sJVbHY$M1atj6oaUuzpnLhB9ZbbJCeikjHB9xX9srAs7MyQ4is=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (2, 'bea93', 'pbkdf2_sha256$870000$75mYa9Nir8YWkcM5pFM3t6$WsoS56hieSHvE5FCWb6xYd3FNQN71uyWY2OvN/NorYg=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (3, 'csaba88', 'pbkdf2_sha256$870000$cKzPqhNS2W8OBkzPkuceXA$EvRVBXANrrIEwGXi/IyFLK0O1LSR3ylksEFUJeGBjns=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (4, 'dori77', 'pbkdf2_sha256$870000$dSNQb1nhN9XysZ20FqNeso$S61qgQyuM3Dyxsn66uRTXmSqqkAd7AOLqiV3GwM+KTI=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (5, 'erik21', 'pbkdf2_sha256$870000$juxpWlQOxJz6sszsn5PxRP$bQiHdejn4erK8eI1sA2AuVe3p9dbTaSPDR+oXCFe/uw=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (6, 'fanni01', 'pbkdf2_sha256$870000$PlQ2LFggiu8Leqi4HxaX8k$hdLXVHqId6lE1GgwTfGBqfeUQFB6fo2V1t2nAX7jy9M=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (7, 'gabor12', 'pbkdf2_sha256$870000$cKjdJqkfFJHIUCtukIPUEV$8nBa/jMSxC1/K0qerX+DMuCkIPsEFcg+9FtQjQrSiKA=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (8, 'hanna34', 'pbkdf2_sha256$870000$P8i0czPYCKv9ZyNhnE1lzk$a+Wj0VYKmwY8IKU8MqeIwZWWpgTGFt/OSESaorRcUsE=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (9, 'istvan45', 'pbkdf2_sha256$870000$T8sEdaPBzTv9YpWVrvZ6Z1$ORhGxt0/YFf3e7CSdUbvSsGpWt1yOgaPFFzSA/iR6zE=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (10, 'juli29', 'pbkdf2_sha256$870000$H8HIs1QYyvTs08Uhw811YA$oHjkdYjk7pbnWAh+wYTjWTuZNvNeeAxMSimRkd94Ew0=', 0, SYSTIMESTAMP, SYSTIMESTAMP);
INSERT INTO Felhasznalok (id, felhasznalonev, jelszo, admin, utolso_bejelentkezes, csatlakozas_ido) VALUES (11, 'admin', 'pbkdf2_sha256$870000$DBvLQE8iPMtayBn3XyHYh4$ApDixuuhsyHNipMdf3YWkn7Lcb+Dc4pD0eQINLBSVo8=', 1, SYSTIMESTAMP, SYSTIMESTAMP);


-- Felhasznalo_kapcsolatok

INSERT INTO Felhasznalo_kapcsolatok VALUES (1, 2, 'accepted');
INSERT INTO Felhasznalo_kapcsolatok VALUES (2, 3, 'pending');
INSERT INTO Felhasznalo_kapcsolatok VALUES (3, 4, 'accepted');
INSERT INTO Felhasznalo_kapcsolatok VALUES (4, 5, 'rejected');
INSERT INTO Felhasznalo_kapcsolatok VALUES (5, 6, 'accepted');
INSERT INTO Felhasznalo_kapcsolatok VALUES (6, 7, 'accepted');
INSERT INTO Felhasznalo_kapcsolatok VALUES (7, 8, 'pending');
INSERT INTO Felhasznalo_kapcsolatok VALUES (8, 9, 'accepted');
INSERT INTO Felhasznalo_kapcsolatok VALUES (9, 10, 'rejected');
INSERT INTO Felhasznalo_kapcsolatok VALUES (10, 1, 'accepted');


-- Csoportok
INSERT INTO Csoportok (id, felhasznalo_id, letrehozas_ido) VALUES (1, 1, SYSTIMESTAMP);
INSERT INTO Csoportok (id, felhasznalo_id, letrehozas_ido) VALUES (2, 2, SYSTIMESTAMP);
INSERT INTO Csoportok (id, felhasznalo_id, letrehozas_ido) VALUES (3, 3, SYSTIMESTAMP);
INSERT INTO Csoportok (id, felhasznalo_id, letrehozas_ido) VALUES (4, 4, SYSTIMESTAMP);
INSERT INTO Csoportok (id, felhasznalo_id, letrehozas_ido) VALUES (5, 5, SYSTIMESTAMP);

-- Felhasznalo_Csoportok

-- Minden csoporthoz 5 tag
INSERT INTO Felhasznalo_Csoportok VALUES (1, 1);
INSERT INTO Felhasznalo_Csoportok VALUES (1, 2);
INSERT INTO Felhasznalo_Csoportok VALUES (1, 3);
INSERT INTO Felhasznalo_Csoportok VALUES (1, 4);
INSERT INTO Felhasznalo_Csoportok VALUES (1, 5);

INSERT INTO Felhasznalo_Csoportok VALUES (2, 6);
INSERT INTO Felhasznalo_Csoportok VALUES (2, 7);
INSERT INTO Felhasznalo_Csoportok VALUES (2, 8);
INSERT INTO Felhasznalo_Csoportok VALUES (2, 9);
INSERT INTO Felhasznalo_Csoportok VALUES (2, 10);

INSERT INTO Felhasznalo_Csoportok VALUES (3, 1);
INSERT INTO Felhasznalo_Csoportok VALUES (3, 3);
INSERT INTO Felhasznalo_Csoportok VALUES (3, 5);
INSERT INTO Felhasznalo_Csoportok VALUES (3, 7);
INSERT INTO Felhasznalo_Csoportok VALUES (3, 9);

INSERT INTO Felhasznalo_Csoportok VALUES (4, 2);
INSERT INTO Felhasznalo_Csoportok VALUES (4, 4);
INSERT INTO Felhasznalo_Csoportok VALUES (4, 6);
INSERT INTO Felhasznalo_Csoportok VALUES (4, 8);
INSERT INTO Felhasznalo_Csoportok VALUES (4, 10);

INSERT INTO Felhasznalo_Csoportok VALUES (5, 1);
INSERT INTO Felhasznalo_Csoportok VALUES (5, 6);
INSERT INTO Felhasznalo_Csoportok VALUES (5, 7);
INSERT INTO Felhasznalo_Csoportok VALUES (5, 8);
INSERT INTO Felhasznalo_Csoportok VALUES (5, 9);

-- Uzenetek
BEGIN
  FOR i IN 1..30 LOOP
    INSERT INTO Uzenetek (id, felhasznalo_id, csoport_id, kuldesi_ido, tartalom)
    VALUES (
      i, MOD(i,10)+1, MOD(i,5)+1, SYSTIMESTAMP - INTERVAL '1' DAY * MOD(i,7),
      'Teszt üzenet' || i
    );
  END LOOP;
END;
/

-- Bejegyzesek
BEGIN
  FOR i IN 1..25 LOOP
    INSERT INTO Bejegyzesek (id, felhasznalo_id, feltoltott_kep, letrehozasi_ido, tartalom)
    VALUES (
      i, MOD(i,10)+1, 'kep' || i || '.jpg', SYSTIMESTAMP - INTERVAL '2' DAY * MOD(i,5),
      'Bejegyzes tartalom ' || i
    );
  END LOOP;
END;
/

-- Kommentek
BEGIN
  FOR i IN 1..50 LOOP
    INSERT INTO Kommentek (id, felhasznalo_id, bejegyzes_id, feltoltesi_ido, tartalom)
    VALUES (
      i, MOD(i,10)+1, MOD(i,25)+1, SYSTIMESTAMP - INTERVAL '3' HOUR * MOD(i,10),
      'Komment tartalom ' || i
    );
  END LOOP;
END;
/



