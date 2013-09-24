update sqlite_master set sql=replace(sql, 'PRIMARY KEY,', 'PRIMARY KEY AUTOINCREMENT,') where name='reversion_revision';
