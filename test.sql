CREATE TABLE IF NOT EXISTS 'av' (
	'av_id' BIGINT(20) unsigned NOT NULL,
	PRIMARY KEY('av_id')
) ENGINE = InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS 'detail' (
	't_id' BIGINT(30) unsigned not null auto_increment,
	'av_id' BIGINT(20) unsigned not null,
	'view' BIGINT(24) unsigned,
	'danmaku' BIGINT(20) unsigned,
	'favorite' BIGINT(20) unsigned,
	'coin' BIGINT(24) unsigned,
	'share' BIGINT(20) unsigned,
	'now_rank' BIGINT(20) unsigned,
	'his_rank' BIGINT(20) unsigned,
	PRIMARY KEY('t_id'),
	foreign key('av_id') references av('av_id')
) ENGINE = InnoDB DEFAULT CHARSET=utf8;
