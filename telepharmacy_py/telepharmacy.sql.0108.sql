DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS pharmacist;
DROP TABLE IF EXISTS orders;

CREATE TABLE pharmacist (
  pharmacist_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  room_id TEXT NOT NULL UNIQUE,
  verification TEXT NOT NULL UNIQUE
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
  status TEXT NOT NULL,
  pharmacist_id TEXT NULL,
  FOREIGN KEY(pharmacist_id) REFERENCES pharmacist(pharmacist_id)
);

/*
CREATE TABLE account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL,
  date_of_birth DATE NOT NULL,
  type TEXT NOT NULL,
  status TEXT NOT NULL,
  pharmacist_id TEXT NULL,
  date_created DATETIME NULL,
  FOREIGN KEY(pharmacist_id) REFERENCES pharmacist(pharmacist_id)
);
*/

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NULL,
  order_id TEXT UNIQUE NOT NULL,
  symptoms TEXT NOT NULL,
  expiry_date TEXT NOT NULL,
  issue_date TEXT NOT NULL,
  FOREIGN KEY(username) REFERENCES account(username)
);

INSERT INTO pharmacist (pharmacist_id, name, email, room_id, verification) VALUES ("PT-0001", "Andy Tao", "andytaotest@gmail.com", "TCxvYpidzgTSfGEQvYXu", "135791");
INSERT INTO pharmacist (pharmacist_id, name, email, room_id, verification) VALUES ("PT-0002", "Mary Astor", "maryastortest@gmail.com", "00ZP3KvX9haK0bu26Ci0", "246802");
INSERT INTO pharmacist (pharmacist_id, name, email, room_id, verification) VALUES ("PT-0003", "Jason Smith", "jasonsmith@gmail.com", "testingroomid123", "123987");
INSERT INTO pharmacist (pharmacist_id, name, email, room_id, verification) VALUES ("PT-0004", "Esther Cheng", "esthercheng@gmail.com", "testingroomid456", "554400");
