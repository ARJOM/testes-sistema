CREATE TABLE genders(
	gender_id INTEGER,
	gender_name VARCHAR(20) NOT NULL,
	CONSTRAINT gender_pk PRIMARY KEY (gender_id)
);

CREATE TABLE users(
	email VARCHAR(80),
	user_name VARCHAR(80) NOT NULL,
	gender INTEGER NOT NULL,
	birthday DATE NOT NULL,
	password VARCHAR(255) NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (email),
	CONSTRAINT userGender_fk FOREIGN KEY (gender) REFERENCES genders(gender_id)
);

CREATE TABLE preferences(
	preference_id INTEGER,
	user_email VARCHAR(80) UNIQUE NOT NULL,
	min_age INTEGER,
	max_age INTEGER,
	gender INTEGER,
	CONSTRAINT preference_pk PRIMARY KEY (preference_id),
	CONSTRAINT preferenceUser_fk FOREIGN KEY (user_email) REFERENCES users(email),
	CONSTRAINT preferenceGender_fk FOREIGN KEY (gender) REFERENCES genders(gender_id),
	CONSTRAINT greater CHECK (max_age>=min_age)
);

CREATE VIEW users_preferences AS
    SELECT u.email, u.gender, u.birthday, p.gender as wanted_gender, p.min_age, p.max_age
    FROM users u JOIN preferences p ON u.email = p.user_email;

CREATE TABLE categorys(
	category_id INTEGER,
	category_name VARCHAR(80) UNIQUE NOT NULL,
	CONSTRAINT category_pk PRIMARY KEY (category_id)
);

CREATE TABLE items(
	item_id INTEGER,
	item_name VARCHAR(80) NOT NULL,
	category INTEGER NOT NULL,
	CONSTRAINT item_pk PRIMARY KEY (item_id),
	CONSTRAINT itemCategory_fk FOREIGN KEY (category) REFERENCES categorys(category_id)
);

CREATE TABLE rates(
	user_email VARCHAR(80),
	item INTEGER,
	rate FLOAT NOT NULL,
	CONSTRAINT rate_pk PRIMARY KEY (user_email, item),
	CONSTRAINT rate_interval CHECK (rate<=5.0 AND rate>=0.0),
	CONSTRAINT user_fk FOREIGN KEY (user_email) REFERENCES users(email),
	CONSTRAINT item_fk FOREIGN KEY (item) REFERENCES items(item_id)
);

INSERT INTO genders(gender_name) VALUES ('masculino');
INSERT INTO genders(gender_name) VALUES ('feminino');
INSERT INTO genders(gender_name) VALUES ('não informar')