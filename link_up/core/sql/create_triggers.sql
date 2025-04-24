-- Triggers for Auto-incrementing Primary Keys

-- Trigger for Felhasznalok (Users)
CREATE OR REPLACE TRIGGER felhasznalok_trigger
BEFORE INSERT ON felhasznalok
FOR EACH ROW
BEGIN
  IF :NEW.id IS NULL THEN
    SELECT felhasznalok_seq.NEXTVAL INTO :NEW.id FROM dual;
  END IF;
END;
/

-- Trigger for Csoportok (Groups)
CREATE OR REPLACE TRIGGER csoportok_trigger
BEFORE INSERT ON csoportok
FOR EACH ROW
BEGIN
  IF :NEW.id IS NULL THEN
    SELECT csoportok_seq.NEXTVAL INTO :NEW.id FROM dual;
  END IF;
END;
/

-- Trigger for Uzenetek (Messages)
CREATE OR REPLACE TRIGGER uzenetek_trigger
BEFORE INSERT ON uzenetek
FOR EACH ROW
BEGIN
  IF :NEW.id IS NULL THEN
    SELECT uzenetek_seq.NEXTVAL INTO :NEW.id FROM dual;
  END IF;
END;
/

-- Trigger for Bejegyzesek (Posts)
CREATE OR REPLACE TRIGGER bejegyzesek_trigger
BEFORE INSERT ON bejegyzesek
FOR EACH ROW
BEGIN
  IF :NEW.id IS NULL THEN
    SELECT bejegyzesek_seq.NEXTVAL INTO :NEW.id FROM dual;
  END IF;
END;
/

-- Trigger for Kommentek (Comments)
CREATE OR REPLACE TRIGGER kommentek_trigger
BEFORE INSERT ON kommentek
FOR EACH ROW
BEGIN
  IF :NEW.id IS NULL THEN
    SELECT kommentek_seq.NEXTVAL INTO :NEW.id FROM dual;
  END IF;
END;
/