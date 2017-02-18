drop table if exists accounts;
create table account (
	netID text not null,
	password text not null,
	balance int not null
);

INSERT INTO user
(netID, password, balance)