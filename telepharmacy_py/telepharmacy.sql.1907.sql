DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS pharmacist;

CREATE TABLE pharmacist (
  pharmacist_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  room_id TEXT UNIQUE,
  verification TEXT NOT NULL
  /*
  verification is hard coded for now, supposedly generated and sent through email and not stored
  also, verification should be for both pharmacist and patients, not just pharmacist
  */
);

CREATE TABLE account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL, 
  type TEXT NOT NULL,
  pharmacist_id TEXT NULL,
  FOREIGN KEY(pharmacist_id) REFERENCES pharmacist(pharmacist_id)
);

INSERT INTO pharmacist (pharmacist_id, name, email, room_id, verification) VALUES ("PT-0001", "Andy Tao", "andytaotest@gmail.com", "TCxvYpidzgTSfGEQvYXu", "2CibOX");
INSERT INTO pharmacist (pharmacist_id, name, email, room_id, verification) VALUES ("PT-0002", "Mary Astor", "maryastortest@gmail.com", "00ZP3KvX9haK0bu26Ci0", "3Hm7xB");
